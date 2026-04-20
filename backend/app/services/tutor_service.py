"""
Socratic Tutor Service — Intelligent Content Layer
===================================================
Primary API:
    from app.services.tutor_service import generate_socratic_explanation

    card = await generate_socratic_explanation(
        template_id="FM-TPL-001",
        variables={"i": 0.045, "n": 20, "L1": 200000},
        user_answer="47,312",
        correct_answer="51,847",
    )

LLM Providers (TUTOR_LLM_PROVIDER env var):
    "anthropic"   — Anthropic SDK (claude-sonnet-4-6)
    "openai"      — OpenAI SDK (gpt-4o, JSON mode)
    "langchain"   — LangChain with ChatPromptTemplate
    (unset/no key) — deterministic template fallback

Double-Backslash Rule
─────────────────────
All LaTeX in output strings uses DOUBLE backslashes so the value
survives: Python → json.dumps → JavaScript → KaTeX.

    Python literal  : "\\\\frac{1}{n}"
    After json.loads: "\\frac{1}{n}"
    KaTeX input     : renders as \\frac{1}{n}

Answer-Diff Analysis
─────────────────────
When correct_answer is a numeric string, _analyze_answer_diff() detects
the likely actuarial error class (undiscounted, annuity_type, units, …)
so the LLM prompt can target the explanation precisely.
"""

from __future__ import annotations

import json
import logging
import os
import re
import textwrap
import time
from typing import Any, Optional, Union

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


def _log_llm(
    event: str,
    template_id: str,
    provider: str,
    elapsed_ms: float | None = None,
    hallucination_flag: bool = False,
    error: str | None = None,
) -> None:
    """Structured log entry for every LLM call — compatible with log aggregators."""
    logger.info(
        "tutor_llm",
        extra={
            "event":            event,          # "call_start" | "call_success" | "call_failure" | "fallback"
            "template_id":      template_id,
            "provider":         provider,
            "elapsed_ms":       round(elapsed_ms, 1) if elapsed_ms is not None else None,
            "hallucination":    hallucination_flag,
            "error":            error,
        },
    )


# ─── Pydantic v2 schemas ──────────────────────────────────────────────────────

class ConceptCard(BaseModel):
    """
    Concept Card — structured Socratic explanation returned by the tutor.

    Structure: Breakdown → Formula → Why → Steps → Error Analysis → Anchor → Follow-up

    All string fields are KaTeX-ready (double-backslash LaTeX, $...$ inline,
    $$...$$ display math).
    """
    model_config = {"populate_by_name": True}

    breakdown: str = Field(
        description="What concept / technique is being tested in this question, "
                    "stated as a Socratic opening question that leads the student "
                    "without giving the answer away."
    )
    formula: str = Field(
        description="The single most important formula for this problem, "
                    "as KaTeX display math, e.g. $$\\\\bar{a}_{\\\\overline{n}|} = "
                    "\\\\frac{1-v^n}{\\\\delta}$$"
    )
    why: str = Field(
        description="Structural reason this method applies here — not just WHAT it is "
                    "but WHY it fits this problem's constraints."
    )
    step_by_step: list[str] = Field(
        description="Ordered derivation steps; each is a self-contained KaTeX-ready string."
    )
    error_analysis: str = Field(
        description="For a wrong answer: the specific error class and the exact "
                    "calculation path that produces the student's number. "
                    "For a correct answer: 'Correct — see follow-up for a deeper test.'"
    )
    memory_anchor: str = Field(
        description="One-sentence mnemonic or structural analogy the student can "
                    "recall under exam pressure."
    )
    follow_up: str = Field(
        description="A deeper Socratic question that tests whether the student "
                    "understands the structure, not just the surface pattern."
    )
    latex_safe: bool = True


# Keep SocraticExplanation for backward compatibility with existing tutor.py router
class SocraticExplanation(BaseModel):
    """Legacy explanation schema — kept for backward compat with tutor.py router."""
    model_config = {"populate_by_name": True}

    socratic_hook: str = ""
    error_diagnosis: str = ""
    why_this_method: str = ""
    step_by_step: list[str] = Field(default_factory=list)
    key_formula: str = ""
    why_other_choices_wrong: list[dict[str, str]] = Field(default_factory=list)
    memory_anchor: str = ""
    follow_up_question: str = ""
    latex_safe: bool = True


class AnswerChoice(BaseModel):
    label: str
    text: str
    correct: bool = False


class QuestionTemplate(BaseModel):
    """Legacy template model — kept for TutorService shim."""
    template_text: str
    topic_name: str = "Actuarial Mathematics"
    exam_code: str = "P"
    difficulty: int = Field(default=5, ge=1, le=10)
    correct_answer_label: str = "A"
    correct_answer_text: str = ""
    solution_calculation: str = ""
    solution_concept: str = ""
    common_mistakes: list[str] = Field(default_factory=list)
    choices: list[AnswerChoice] = Field(default_factory=list)


# ─── Error-class taxonomy ─────────────────────────────────────────────────────

_ERROR_CLASSES: dict[str, str] = {
    "undiscounted":  "Forgot the discount factor $v^t = (1+i)^{-t}$.",
    "accumulated":   "Accumulated instead of discounted — used $(1+i)^t$ instead of $v^t$.",
    "annuity_type":  "Confused annuity-immediate with annuity-due: they differ by $(1+i)$.",
    "off_by_n":      "Missed a factor of $n$ — check whether to divide or multiply by the period count.",
    "units":         "Units mismatch: off by 1{,}000 or 12 (monthly/annual conversion).",
    "sign":          "Sign error — check whether the exponent on $v$ should be positive or negative.",
    "wrong_rate":    "Used the nominal rate instead of the effective periodic rate.",
    "generic":       "Review the setup: identify the correct formula before substituting.",
}


def _analyze_answer_diff(
    user_answer: str,
    correct_answer: str,
    variables: dict[str, Any],
) -> str:
    """Return an error-class key by examining the ratio of user vs. correct numeric value."""
    try:
        u = float(re.sub(r"[^0-9.\-+eE]", "", user_answer or "0") or 0)
        c = float(re.sub(r"[^0-9.\-+eE]", "", correct_answer or "0") or 0)
    except ValueError:
        return "generic"

    if c == 0 or u == 0:
        return "generic"

    ratio = u / c
    i = float(variables.get("i", variables.get("rate", 0.05)))
    n = float(variables.get("n", variables.get("num_periods", 10)))
    v = 1.0 / (1.0 + i)

    def close(a: float, b: float, tol: float = 0.02) -> bool:
        return abs(a - b) < tol * max(abs(b), 1e-9)

    if close(ratio, 1.0 + i):      return "undiscounted"
    if close(ratio, v):             return "accumulated"
    if close(ratio, n):             return "off_by_n"
    if close(ratio, 1.0 / n):      return "off_by_n"
    if close(ratio, 1000.0):        return "units"
    if close(ratio, 0.001):         return "units"
    if close(ratio, 12.0):          return "units"
    if close(ratio, 1.0 / 12.0):   return "units"
    if ratio < 0:                   return "sign"
    return "generic"


# ─── Prompt builders ──────────────────────────────────────────────────────────

_SYSTEM_PROMPT = textwrap.dedent("""
    You are a senior actuary and exam mentor (SOA/CAS).
    You explain concepts the way an expert explains them to a bright student
    who is close to understanding — Socratic, precise, never condescending.

    CRITICAL OUTPUT RULES
    ─────────────────────
    1. Return ONLY valid JSON — no markdown fences, no prose before/after.
    2. Use DOUBLE backslashes for ALL LaTeX commands.
       json.loads() will parse your output; strings then go to KaTeX.
       Correct  : "$$\\\\frac{1-v^n}{i}$$"
       Incorrect: "$$\\frac{1-v^n}{i}$$"
    3. Inline math: $...$ — Display math: $$...$$
    4. Max 120 words per field. Tone: precise and encouraging.
    5. Do NOT repeat the question stem verbatim. Guide, don't spoonfeed.
""").strip()


def _build_concept_card_prompt(
    template_id: str,
    template_data: dict[str, Any],
    variables: dict[str, Any],
    user_answer: str,
    correct_answer: str,
    error_class: str,
) -> str:
    rounded_vars = {
        k: round(v, 4) if isinstance(v, float) else v
        for k, v in variables.items()
    }
    is_correct = error_class == "correct"
    situation = (
        f"Student answered **{user_answer}** (INCORRECT). "
        f"Correct answer: **{correct_answer}**. "
        f"Likely error class: **{error_class}** — {_ERROR_CLASSES.get(error_class, '')}"
        if not is_correct else
        f"Student answered **{user_answer}** (CORRECT). "
        "Deepen understanding beyond surface pattern-matching."
    )

    pitfalls = "\n".join(
        f"  • {p}" for p in template_data.get("common_pitfalls", [])
    ) or "  (none provided)"

    schema = json.dumps({
        "breakdown":     "<Socratic opening: what concept is being tested and why it matters>",
        "formula":       "$$<core display LaTeX formula>$$",
        "why":           "<structural reason this method applies to THIS problem>",
        "step_by_step":  ["<step 1 with KaTeX>", "<step 2>", "..."],
        "error_analysis":"<precise error path that produces the student's number, or 'Correct'>",
        "memory_anchor": "<one-sentence mnemonic or analogy>",
        "follow_up":     "<deeper Socratic question that tests structural understanding>",
    }, indent=2)

    return textwrap.dedent(f"""
        ## Template
        ID: {template_id}
        Exam: {template_data.get("exam_code", "?")} | Topic: {template_data.get("topic", "?")}
        Difficulty: {template_data.get("difficulty", "?")} / 10

        ## Variable values (rounded to 4 d.p.)
        {json.dumps(rounded_vars, indent=2)}

        ## Situation
        {situation}

        ## Known pitfalls for this question type:
        {pitfalls}

        ## Task
        Produce a Concept Card.
        Breakdown: ask WHY this technique (not another) applies.
        Formula: give the single most important formula in display LaTeX.
        Why: explain the structural reason this formula fits.
        Step-by-step: 3-6 KaTeX steps — concise but complete.
        Error analysis: if wrong, trace the EXACT path from the student's mistake to their number.
        Memory anchor: one sentence the student can recall under pressure.
        Follow-up: a variation that distinguishes deep from surface understanding.

        Respond with ONLY this JSON (no fences, no extra keys):
        {schema}
    """).strip()


# ─── LaTeX safety post-processor ─────────────────────────────────────────────

_SINGLE_BS = re.compile(
    r'(?<!\\)\\(?!\\)'
    r'(?:frac|sqrt|sum|int|prod|lim|infty|alpha|beta|gamma|delta|epsilon|'
    r'mu|sigma|lambda|theta|phi|psi|omega|Phi|Gamma|Delta|Sigma|Pi|'
    r'text|mathrm|mathbb|mathbf|mathcal|binom|left|right|cdot|times|'
    r'approx|leq|geq|neq|in|notin|subset|cup|cap|sim|bar|hat|tilde|'
    r'vec|overline|underline|begin|end|quad|qquad|dfrac|tfrac|partial|'
    r'nabla|forall|exists|Rightarrow|Leftarrow|rightarrow|leftarrow|'
    r'iff|ldots|cdots|vdots|ddots|pm|mp|div|ast|circ|bullet|'
    r'ddot|dot|acute|grave|check|breve|widetilde|widehat|'
    r'oplus|otimes|oint|iint|iiint|underbrace|overbrace|'
    r'stackrel|overset|underset|xrightarrow)\b'
)


def _fix_backslashes(obj: Any) -> Any:
    """Recursively double any single-backslash LaTeX commands that survived json.loads."""
    if isinstance(obj, str):
        return _SINGLE_BS.sub(lambda m: m.group(0).replace("\\", "\\\\"), obj)
    if isinstance(obj, list):
        return [_fix_backslashes(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _fix_backslashes(v) for k, v in obj.items()}
    return obj


# ─── LLM adapters ─────────────────────────────────────────────────────────────

async def _call_raw_anthropic(system: str, user: str) -> str:
    try:
        import anthropic  # type: ignore
    except ImportError:
        raise RuntimeError("pip install anthropic")
    client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1400,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


async def _call_raw_openai(system: str, user: str) -> str:
    try:
        from openai import AsyncOpenAI  # type: ignore
    except ImportError:
        raise RuntimeError("pip install openai")
    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = await client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1400,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    )
    return resp.choices[0].message.content or ""


async def _call_langchain(system: str, user: str) -> str:
    try:
        from langchain_core.prompts import ChatPromptTemplate  # type: ignore
    except ImportError:
        raise RuntimeError("pip install langchain-core langchain-anthropic langchain-openai")

    provider = os.environ.get("TUTOR_LLM_PROVIDER", "langchain-anthropic").lower()
    if "openai" in provider:
        try:
            from langchain_openai import ChatOpenAI  # type: ignore
            llm = ChatOpenAI(model="gpt-4o", temperature=0,
                             openai_api_key=os.environ["OPENAI_API_KEY"])
        except ImportError:
            raise RuntimeError("pip install langchain-openai")
    else:
        try:
            from langchain_anthropic import ChatAnthropic  # type: ignore
            llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0,
                                anthropic_api_key=os.environ["ANTHROPIC_API_KEY"])
        except ImportError:
            raise RuntimeError("pip install langchain-anthropic")

    prompt = ChatPromptTemplate.from_messages([("system", "{system}"), ("human", "{user}")])
    chain = prompt | llm
    result = await chain.ainvoke({"system": system, "user": user})
    return result.content  # type: ignore[union-attr]


# ─── Fallback (no LLM key) ────────────────────────────────────────────────────

def _fallback_card(
    template_id: str,
    template_data: dict[str, Any],
    variables: dict[str, Any],
    error_class: str,
) -> ConceptCard:
    """Deterministic Concept Card — works without any API key."""
    topic = template_data.get("topic", "Actuarial Mathematics")
    exam  = template_data.get("exam_code", "P")
    steps = template_data.get("solution_steps_latex", ["See solution guide."])
    formula = template_data.get("answer_formula", "")
    pitfalls = template_data.get("common_pitfalls", [])

    return ConceptCard(
        breakdown=(
            f"Before calculating, ask yourself: what property of **{topic}** "
            "determines which formula applies to this problem structure?"
        ),
        formula=f"$${formula}$$" if formula and "$$" not in formula else (formula or ""),
        why=(
            f"The {topic} framework applies because the problem satisfies "
            "the required structural conditions — identify each condition explicitly "
            "before substituting parameter values."
        ),
        step_by_step=[s.strip() for s in steps if s.strip()],
        error_analysis=(
            f"{error_class}: {_ERROR_CLASSES.get(error_class, 'Review the setup.')}"
            if error_class != "correct"
            else "Correct — see follow-up for a deeper test."
        ),
        memory_anchor=(
            f"Exam {exam} — {topic}: "
            + (pitfalls[0] if pitfalls else "identify the correct technique first.")
        ),
        follow_up=(
            f"What happens to the answer if you change "
            f"{next(iter(variables), 'the key parameter')} to an extreme value? "
            "Reason about the limit before computing."
        ),
        latex_safe=True,
    )


# ─── Primary public API ───────────────────────────────────────────────────────

async def generate_socratic_explanation(
    template_id: str,
    variables: dict[str, Any],
    user_answer: str,
    correct_answer: str,
) -> ConceptCard:
    """
    Generate a Concept Card (Breakdown → Formula → Why → Steps → …) for a
    student who just answered a question.

    Parameters
    ──────────
    template_id    : Registry ID, e.g. "FM-TPL-001".  Used to load the full
                     template dict from seed_templates.get_template_by_id().
    variables      : Resolved variable values {name: value}.
                     Floats are rounded to 4 d.p. in display.
    user_answer    : The label or value the student submitted (e.g. "47,312").
    correct_answer : The correct answer string (e.g. "51,847" or "B").

    Returns
    ───────
    ConceptCard — all string fields are KaTeX-ready (double-backslash LaTeX).
    """
    from app.services.seed_templates import get_template_by_id  # local import avoids circular

    template_data: dict[str, Any] = get_template_by_id(template_id) or {
        "id": template_id,
        "exam_code": "P",
        "topic": "Actuarial Mathematics",
        "difficulty": 5,
    }

    is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
    error_class = (
        "correct"
        if is_correct
        else _analyze_answer_diff(user_answer, correct_answer, variables)
    )

    provider = os.environ.get("TUTOR_LLM_PROVIDER", "").lower()
    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_openai    = bool(os.environ.get("OPENAI_API_KEY"))

    if not provider or (not has_anthropic and not has_openai):
        _log_llm("fallback", template_id, "none")
        return _fallback_card(template_id, template_data, variables, error_class)

    system_prompt = _SYSTEM_PROMPT
    user_prompt   = _build_concept_card_prompt(
        template_id, template_data, variables, user_answer, correct_answer, error_class
    )

    active_provider = (
        "langchain" if provider.startswith("langchain")
        else "openai" if (provider == "openai" and has_openai)
        else "anthropic"
    )
    _log_llm("call_start", template_id, active_provider)
    t0 = time.monotonic()

    try:
        if provider.startswith("langchain"):
            raw = await _call_langchain(system_prompt, user_prompt)
        elif provider == "openai" and has_openai:
            raw = await _call_raw_openai(system_prompt, user_prompt)
        elif has_anthropic:
            raw = await _call_raw_anthropic(system_prompt, user_prompt)
        else:
            raw = await _call_raw_openai(system_prompt, user_prompt)

        elapsed = (time.monotonic() - t0) * 1000

        raw = re.sub(r'^```(?:json)?\s*', '', raw.strip())
        raw = re.sub(r'\s*```$', '', raw)

        data = _fix_backslashes(json.loads(raw))

        # Hallucination check: required keys must be present and non-empty strings
        required = ("breakdown", "formula", "why", "step_by_step",
                    "error_analysis", "memory_anchor", "follow_up")
        missing = [k for k in required if not data.get(k)]
        hallucination_flag = bool(missing)
        if hallucination_flag:
            logger.warning("LLM response missing fields: %s", missing)

        _log_llm("call_success", template_id, active_provider,
                 elapsed_ms=elapsed, hallucination_flag=hallucination_flag)

        return ConceptCard(
            breakdown     = data.get("breakdown", ""),
            formula       = data.get("formula", ""),
            why           = data.get("why", ""),
            step_by_step  = data.get("step_by_step", []),
            error_analysis= data.get("error_analysis", error_class),
            memory_anchor = data.get("memory_anchor", ""),
            follow_up     = data.get("follow_up", ""),
            latex_safe    = not hallucination_flag,
        )

    except json.JSONDecodeError as exc:
        elapsed = (time.monotonic() - t0) * 1000
        _log_llm("call_failure", template_id, active_provider,
                 elapsed_ms=elapsed, error=f"JSONDecodeError: {exc}")
        return _fallback_card(template_id, template_data, variables, error_class)
    except Exception as exc:
        elapsed = (time.monotonic() - t0) * 1000
        _log_llm("call_failure", template_id, active_provider,
                 elapsed_ms=elapsed, error=f"{type(exc).__name__}: {exc}")
        return _fallback_card(template_id, template_data, variables, error_class)


# ─── Render helper (shared utility) ──────────────────────────────────────────

def _render_template(template_text: str, variables: dict[str, Any]) -> str:
    safe = {
        k: (f"{v:.4f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v))
        for k, v in variables.items()
    }
    try:
        return template_text.format(**safe)
    except (KeyError, ValueError):
        return template_text


# ─── Legacy class shim (backward compat with existing tutor.py router) ────────

class TutorService:
    """Thin wrapper so the existing tutor.py router continues to work."""

    def __init__(self) -> None:
        self.provider = os.environ.get("TUTOR_LLM_PROVIDER", "anthropic")

    async def explain(self, req: Any) -> SocraticExplanation:
        template_id = getattr(req, "template_id", None) or "unknown"
        variables   = getattr(req, "user_variables", {})
        user_answer = getattr(req, "user_answer_label", "—")
        correct     = getattr(req, "correct_answer_text", "")

        card = await generate_socratic_explanation(
            template_id    = template_id,
            variables      = variables,
            user_answer    = user_answer,
            correct_answer = correct,
        )
        return SocraticExplanation(
            socratic_hook      = card.breakdown,
            error_diagnosis    = card.error_analysis,
            why_this_method    = card.why,
            step_by_step       = card.step_by_step,
            key_formula        = card.formula,
            memory_anchor      = card.memory_anchor,
            follow_up_question = card.follow_up,
            latex_safe         = True,
        )

    def render_template(self, template_text: str, variables: dict[str, Any]) -> str:
        return _render_template(template_text, variables)
