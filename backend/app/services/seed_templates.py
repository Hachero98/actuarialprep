"""
Expert Seed Content — Intelligent Content Layer
================================================
4 high-difficulty (Level 7+) question templates for Exam FM and Exam P.

Format contract
───────────────
Each template is a plain dict with:
  - variables_config      : {var: [min, max]} or {var: [v1, v2, ...]}
  - solution_steps_latex  : list[str] — ordered steps; each is KaTeX-safe
                            (double-backslash convention throughout)

All float literals are rounded to 4 decimal places.
All LaTeX uses double backslashes: "\\\\frac{1}{n}" not "\\frac{1}{n}".
"""

from __future__ import annotations

from typing import Any

Template = dict[str, Any]

# ══════════════════════════════════════════════════════════════════════════════
# FM TEMPLATE 01 — Redington Immunization (Full Three-Condition Derivation)
# Difficulty: 9  |  Topic: Duration & Immunization
# ══════════════════════════════════════════════════════════════════════════════

FM_TPL_01: Template = {
    "id": "FM-TPL-001",
    "exam_code": "FM",
    "topic": "Duration & Immunization",
    "subtopic_slug": "redington-immunization",
    "difficulty": 9,

    "template_text": (
        "A fund must meet liabilities of ${L1:,.0f} payable in {t1} years and "
        "${L2:,.0f} payable in {t2} years. "
        "The fund manager constructs a portfolio of two zero-coupon bonds with "
        "maturities {s1} years and {s2} years. "
        "At an annual effective interest rate of {i_pct}%, determine the face "
        "amounts $F_1$ and $F_2$ required to satisfy Redington's three immunization "
        "conditions, and verify that the convexity condition holds."
    ),

    "variables_config": {
        "L1": [100000, 500000],
        "L2": [120000, 600000],
        "t1": [3, 8],
        "t2": [10, 20],
        "i":  [0.03, 0.08],
        "s1": [1, "t1 - 1"],    # must be < D_L (enforced at generation)
        "s2": ["t2 + 1", 25],   # must be > D_L (enforced at generation)
    },

    "solution_steps_latex": [
        (
            "**Step 1 — Present value of liabilities**\n"
            "Let $v = (1+i)^{-1}$.  The total present value is\n"
            "$$P_L = L_1 \\cdot v^{t_1} + L_2 \\cdot v^{t_2}$$"
        ),
        (
            "**Step 2 — Macaulay duration of liabilities**\n"
            "$$D_L = \\frac{t_1 \\cdot L_1 v^{t_1} + t_2 \\cdot L_2 v^{t_2}}{P_L}$$\n"
            "This is the PV-weighted average payment time.  "
            "*Pitfall*: using nominal cash flows instead of present values."
        ),
        (
            "**Step 3 — Macaulay convexity of liabilities**\n"
            "$$\\mathcal{C}_L = \\frac{t_1^2 \\cdot L_1 v^{t_1} + t_2^2 \\cdot L_2 v^{t_2}}{P_L}$$"
        ),
        (
            "**Step 4 — Redington's three conditions**\n"
            "Write $x_j = F_j v^{s_j}$ (PV of bond $j$).  Conditions:\n"
            "$$\\text{(i)}\\quad x_1 + x_2 = P_L$$\n"
            "$$\\text{(ii)}\\quad s_1 x_1 + s_2 x_2 = D_L \\cdot P_L$$\n"
            "$$\\text{(iii)}\\quad s_1^2 x_1 + s_2^2 x_2 > \\mathcal{C}_L \\cdot P_L$$"
        ),
        (
            "**Step 5 — Solve the $2 \\times 2$ linear system**\n"
            "Subtract $s_2 \\times (\\text{i})$ from $\\text{(ii)}$:\n"
            "$$x_1 = \\frac{(D_L - s_2)\\,P_L}{s_1 - s_2}, "
            "\\qquad x_2 = P_L - x_1$$\n"
            "*Key constraint*: $s_1 < D_L < s_2$ is required so $x_1, x_2 > 0$."
        ),
        (
            "**Step 6 — Face amounts and convexity check**\n"
            "$$F_j = x_j \\cdot (1+i)^{s_j}$$\n"
            "Convexity of assets: $\\mathcal{C}_A = (s_1^2 x_1 + s_2^2 x_2)/P_L$.  "
            "The barbell structure guarantees $\\mathcal{C}_A > \\mathcal{C}_L$ "
            "whenever $s_1 < D_L < s_2$.  This is why the bond maturities must "
            "straddle the liability duration."
        ),
    ],

    "answer_formula": (
        "F_1 = \\\\frac{(D_L - s_2)\\\\,P_L}{(s_1 - s_2)\\\\,v^{s_1}},\\\\quad"
        "F_2 = \\\\frac{(s_1 - D_L)\\\\,P_L}{(s_1 - s_2)\\\\,v^{s_2}}"
    ),

    "common_pitfalls": [
        "Using nominal (undiscounted) cash flows when computing D_L.",
        "Forgetting that s_1 < D_L < s_2 is required for both face amounts to be positive.",
        "Conflating Macaulay duration with modified duration: D_mod = D_mac / (1+i).",
        "Verifying only conditions (i) and (ii) and omitting the convexity inequality (iii).",
    ],

    "tags": ["immunization", "duration", "convexity", "zero-coupon-bonds", "FM"],
}


# ══════════════════════════════════════════════════════════════════════════════
# FM TEMPLATE 02 — Convexity of a Non-Level (Arithmetically Increasing) Annuity
# Difficulty: 8  |  Topic: Annuities — Duration & Convexity
# ══════════════════════════════════════════════════════════════════════════════

FM_TPL_02: Template = {
    "id": "FM-TPL-002",
    "exam_code": "FM",
    "topic": "Annuities",
    "subtopic_slug": "convexity-increasing-annuity",
    "difficulty": 8,

    "template_text": (
        "An annuity-immediate pays amounts $P$, $P+Q$, $P+2Q$, $\\ldots$, $P+(n-1)Q$ "
        "at the end of each year for $n = {n}$ years. "
        "The first payment is $P = {P}$ and the annual increase is $Q = {Q}$. "
        "At an annual effective rate $i = {i_pct}\\%$, compute:\n"
        "(a) the present value $\\mathrm{{PV}}$,\n"
        "(b) the Macaulay duration $D_{{\\mathrm{{mac}}}}$,\n"
        "(c) the convexity $\\mathcal{{C}}$, and\n"
        "(d) the approximate price change for a $+{dy_bps}$ bps parallel shift."
    ),

    "variables_config": {
        "P":  [500, 5000],
        "Q":  [50, 500],
        "n":  [5, 20],
        "i":  [0.03, 0.10],
        "dy": [0.0025, 0.02],   # interest rate shock
    },

    "solution_steps_latex": [
        (
            "**Step 1 — Decompose into level + increasing annuity**\n"
            "Payment at time $t$ is $C_t = P + (t-1)Q$.  Split:\n"
            "$$\\mathrm{PV} = P\\,a_{\\overline{n}|i} + Q\\,(I\\!a)_{\\overline{n}|i}$$\n"
            "where $a_{\\overline{n}|} = \\dfrac{1-v^n}{i}$ and "
            "$(I\\!a)_{\\overline{n}|} = \\dfrac{\\ddot{a}_{\\overline{n}|} - nv^n}{i}$."
        ),
        (
            "**Step 2 — Level and increasing annuity values**\n"
            "$$a_{\\overline{n}|} = \\frac{1-v^n}{i}, \\qquad "
            "\\ddot{a}_{\\overline{n}|} = (1+i)\\,a_{\\overline{n}|}$$\n"
            "$$\\Rightarrow (I\\!a)_{\\overline{n}|} = "
            "\\frac{(1+i)\\,a_{\\overline{n}|} - nv^n}{i}$$"
        ),
        (
            "**Step 3 — Macaulay duration**\n"
            "$$D_{\\mathrm{mac}} = "
            "\\frac{\\displaystyle\\sum_{t=1}^{n} t\\,C_t\\,v^t}{\\mathrm{PV}}$$\n"
            "Expand the numerator using the $(I\\!a)$ and $(I^2\\!a)$ annuity functions.  "
            "*Pitfall*: treating the increasing annuity as a level annuity (omitting the $Q$-component)."
        ),
        (
            "**Step 4 — Convexity**\n"
            "$$\\mathcal{C} = \\frac{1}{\\mathrm{PV}\\,(1+i)^2}"
            "\\sum_{t=1}^{n} t^2\\,C_t\\,v^t$$\n"
            "The $t(t+1)$ form is often more convenient computationally:\n"
            "$$\\mathcal{C} = \\frac{\\sum_{t=1}^n t(t+1)\\,C_t\\,v^{t+2}}{\\mathrm{PV}}$$"
        ),
        (
            "**Step 5 — Price change approximation**\n"
            "$$\\Delta\\mathrm{PV} \\approx "
            "-D_{\\mathrm{mod}} \\cdot \\mathrm{PV} \\cdot \\Delta i "
            "+ \\tfrac{1}{2}\\,\\mathcal{C} \\cdot \\mathrm{PV} \\cdot (\\Delta i)^2$$\n"
            "where $D_{\\mathrm{mod}} = D_{\\mathrm{mac}} / (1+i)$.  "
            "*Pitfall*: using $D_{\\mathrm{mac}}$ instead of $D_{\\mathrm{mod}}$; "
            "omitting the $\\tfrac{1}{2}$ factor."
        ),
    ],

    "answer_formula": (
        "\\\\mathrm{PV} = P\\\\,a_{\\\\overline{n}|} + Q\\\\,(I\\\\!a)_{\\\\overline{n}|},\\\\quad"
        "D_{\\\\mathrm{mod}} = \\\\frac{D_{\\\\mathrm{mac}}}{1+i}"
    ),

    "common_pitfalls": [
        "Using D_mac in the price-change formula instead of D_mod = D_mac / (1+i).",
        "Omitting the 1/2 factor in the convexity correction term.",
        "Computing (Ia) using the annuity-due formula when the problem states annuity-immediate.",
        "Ignoring the Q-component of duration (treating the increasing annuity as a level one).",
    ],

    "tags": ["increasing-annuity", "convexity", "modified-duration", "FM"],
}


# ══════════════════════════════════════════════════════════════════════════════
# P TEMPLATE 01 — Compound Poisson Aggregate Loss via MGF / PGF
# Difficulty: 8  |  Topic: Transforms & Aggregate Loss
# ══════════════════════════════════════════════════════════════════════════════

P_TPL_01: Template = {
    "id": "P-TPL-003",
    "exam_code": "P",
    "topic": "Transforms & Special Topics",
    "subtopic_slug": "aggregate-loss-pgf",
    "difficulty": 8,

    "template_text": (
        "The number of claims $N$ in one month follows a Poisson distribution "
        "with mean $\\lambda = {lam}$.  Each individual claim amount $X_i$ is "
        "independent of $N$ and follows an Exponential distribution with mean "
        "$\\theta = {theta}$.  Let $S = X_1 + \\cdots + X_N$ (with $S = 0$ when $N=0$).\n"
        "(a) Find $E[S]$ and $\\mathrm{{Var}}(S)$.\n"
        "(b) Verify (a) using the law of total expectation and total variance.\n"
        "(c) Derive $M_S(t)$, the MGF of $S$, and state its domain of validity."
    ),

    "variables_config": {
        "lam":   [1.0, 8.0],
        "theta": [500.0, 5000.0],
    },

    "solution_steps_latex": [
        (
            "**Step 1 — Compound distribution moments**\n"
            "For $S = \\sum_{i=1}^N X_i$ with $N$ independent of the $X_i$:\n"
            "$$E[S] = E[N]\\,E[X] = \\lambda\\,\\theta$$\n"
            "$$\\mathrm{Var}(S) = E[N]\\,\\mathrm{Var}(X) + \\mathrm{Var}(N)\\,(E[X])^2$$\n"
            "Since $N\\sim\\mathrm{Poisson}(\\lambda)$: $\\mathrm{Var}(N)=\\lambda$, and "
            "$\\mathrm{Var}(X)=\\theta^2$, so $\\mathrm{Var}(S) = 2\\lambda\\theta^2$."
        ),
        (
            "**Step 2 — Law of total variance verification**\n"
            "$$\\mathrm{Var}(S) = E[\\mathrm{Var}(S|N)] + \\mathrm{Var}(E[S|N])$$\n"
            "$$= E[N\\,\\theta^2] + \\mathrm{Var}(N\\,\\theta) "
            "= \\lambda\\theta^2 + \\theta^2\\lambda = 2\\lambda\\theta^2 \\;\\checkmark$$"
        ),
        (
            "**Step 3 — MGF via PGF composition**\n"
            "$$M_S(t) = E[e^{tS}] = E\\!\\left[(M_X(t))^N\\right] = G_N(M_X(t))$$\n"
            "where $G_N(z) = e^{\\lambda(z-1)}$ is the PGF of $N$ and "
            "$M_X(t) = (1-\\theta t)^{-1}$ for $t < 1/\\theta$.  Hence:\n"
            "$$M_S(t) = \\exp\\!\\left(\\lambda\\left(\\frac{1}{1-\\theta t}-1\\right)\\right), "
            "\\quad t < \\frac{1}{\\theta}$$"
        ),
        (
            "**Step 4 — Point mass and tail behaviour**\n"
            "$$P(S=0) = P(N=0) = e^{-\\lambda}$$\n"
            "For $S>0$, the distribution is a Gamma mixture.  "
            "For large $n$, CLT applies: $S \\approx N(\\lambda\\theta,\\,2\\lambda\\theta^2)$.  "
            "*Pitfall*: writing $M_S(t) = M_X(\\lambda t)$ — this is wrong; always use "
            "PGF composition $G_N(M_X(t))$."
        ),
    ],

    "answer_formula": (
        "E[S] = \\\\lambda\\\\theta,\\\\quad "
        "\\\\mathrm{Var}(S) = 2\\\\lambda\\\\theta^2,\\\\quad "
        "M_S(t) = \\\\exp\\\\!\\\\left(\\\\lambda\\\\Bigl(\\\\tfrac{1}{1-\\\\theta t}-1\\\\Bigr)\\\\right)"
    ),

    "common_pitfalls": [
        "Forgetting Var(N)*(E[X])^2 term — using only E[N]*Var(X).",
        "Writing M_S(t) = M_X(lambda*t) instead of the correct G_N(M_X(t)) composition.",
        "Forgetting P(S=0) = exp(-lambda) when the domain includes S=0.",
        "Using Exponential variance as theta instead of theta^2.",
    ],

    "tags": ["aggregate-loss", "compound-Poisson", "MGF", "PGF", "law-of-total-variance", "P"],
}


# ══════════════════════════════════════════════════════════════════════════════
# P TEMPLATE 02 — Order Statistics: PDF, Moments, and Covariance
# Difficulty: 7  |  Topic: Multivariate & Order Statistics
# ══════════════════════════════════════════════════════════════════════════════

P_TPL_02: Template = {
    "id": "P-TPL-004",
    "exam_code": "P",
    "topic": "Multivariate Distributions",
    "subtopic_slug": "order-statistics",
    "difficulty": 7,

    "template_text": (
        "Let $X_1, X_2, \\ldots, X_n$ be i.i.d. $\\mathrm{{Uniform}}(0,\\theta)$ "
        "with $n = {n}$ and $\\theta = {theta}$.  "
        "Let $X_{{(k)}}$ denote the $k$-th order statistic ($k={k}$).\n"
        "(a) Find the PDF of $X_{{(k)}}$ and identify its distribution family.\n"
        "(b) Compute $E[X_{{(k)}}]$ and $\\mathrm{{Var}}(X_{{(k)}})$.\n"
        "(c) For $j = {j} < k$, compute $\\mathrm{{Cov}}(X_{{(j)}}, X_{{(k)}})$ "
        "and $\\rho(X_{{(j)}}, X_{{(k)}})$."
    ),

    "variables_config": {
        "n":     [4, 12],
        "theta": [1, 100],
        "k":     [2, "n - 1"],
        "j":     [1, "k - 1"],
    },

    "solution_steps_latex": [
        (
            "**Step 1 — PDF of the $k$-th order statistic**\n"
            "For i.i.d. $X_i \\sim F$ with density $f$:\n"
            "$$f_{(k)}(x) = \\frac{n!}{(k-1)!(n-k)!}\\,[F(x)]^{k-1}[1-F(x)]^{n-k}f(x)$$\n"
            "For $\\mathrm{Uniform}(0,\\theta)$: $f(x)=\\theta^{-1}$, $F(x)=x/\\theta$,\n"
            "$$f_{(k)}(x) = \\frac{n!}{(k-1)!(n-k)!}\\,\\frac{x^{k-1}(\\theta-x)^{n-k}}{\\theta^n}$$\n"
            "This is a $\\mathrm{Beta}(k,\\,n-k+1)$ distribution scaled by $\\theta$."
        ),
        (
            "**Step 2 — Mean and variance from Beta moments**\n"
            "Since $X_{(k)}/\\theta \\sim \\mathrm{Beta}(k,\\,n-k+1)$:\n"
            "$$E[X_{(k)}] = \\frac{k\\,\\theta}{n+1}$$\n"
            "$$\\mathrm{Var}(X_{(k)}) = \\frac{k(n-k+1)\\,\\theta^2}{(n+1)^2(n+2)}$$\n"
            "*Pitfall*: using $k/n$ for the mean instead of $k/(n+1)$."
        ),
        (
            "**Step 3 — Covariance of $X_{(j)}$ and $X_{(k)}$ for $j < k$**\n"
            "Using the joint density of $(X_{(j)}, X_{(k)})$:\n"
            "$$\\mathrm{Cov}(X_{(j)}, X_{(k)}) = \\frac{j(n-k+1)\\,\\theta^2}{(n+1)^2(n+2)}$$\n"
            "Derivation: $E[X_{(j)}X_{(k)}] = \\theta^2 j(k+1)/[(n+1)(n+2)]$, subtract $E[X_{(j)}]E[X_{(k)}]$."
        ),
        (
            "**Step 4 — Correlation**\n"
            "$$\\rho(X_{(j)}, X_{(k)}) = \\sqrt{\\frac{j(n-k+1)}{k(n-j+1)}}$$\n"
            "Note: $\\rho > 0$ always (order statistics are positively correlated) "
            "and $\\rho$ depends only on ranks $j, k, n$ — not on $\\theta$.  "
            "*Pitfall*: assuming $X_{(j)} \\perp X_{(k)}$ because they are 'different' statistics."
        ),
    ],

    "answer_formula": (
        "E[X_{{(k)}}] = \\\\dfrac{{k\\\\theta}}{{n+1}},\\\\quad"
        "\\\\mathrm{{Cov}}(X_{{(j)}},X_{{(k)}}) = "
        "\\\\dfrac{{j(n-k+1)\\\\theta^2}}{{(n+1)^2(n+2)}}"
    ),

    "common_pitfalls": [
        "Using k/n for E[X_(k)] instead of k/(n+1).",
        "Forgetting (k-1)!(n-k)! in the denominator of the order-statistic PDF.",
        "Treating X_(j) and X_(k) as independent — they have positive covariance.",
        "Confusing Beta(k, n-k+1) with Beta(k, n-k) in the identification step.",
    ],

    "tags": ["order-statistics", "Beta-distribution", "covariance", "uniform", "P"],
}


# ══════════════════════════════════════════════════════════════════════════════
# P TEMPLATE 03 — Jacobian Transformation for Bivariate Distributions
# Difficulty: 9  |  Topic: Multivariate Distributions / Change of Variables
# ══════════════════════════════════════════════════════════════════════════════

P_TPL_03: Template = {
    "id": "P-TPL-005",
    "exam_code": "P",
    "topic": "Multivariate Distributions",
    "subtopic_slug": "jacobian-transformation",
    "difficulty": 9,

    "template_text": (
        "Let $X$ and $Y$ be independent random variables where "
        "$X \\sim \\mathrm{{Exponential}}(\\lambda_1)$ with mean $1/\\lambda_1 = {mean_x}$ "
        "and $Y \\sim \\mathrm{{Exponential}}(\\lambda_2)$ with mean $1/\\lambda_2 = {mean_y}$.\n"
        "Define the transformation $U = X + Y$ and $V = \\dfrac{{X}}{{X+Y}}$.\n"
        "(a) Find the joint density $f_{{U,V}}(u, v)$ using the Jacobian method.\n"
        "(b) Show that $U$ and $V$ are independent and identify their marginal distributions.\n"
        "(c) Compute $P(U > {u_threshold})$ and $E[V]$."
    ),

    "variables_config": {
        "mean_x":       [1.0, 5.0],
        "mean_y":       [1.0, 5.0],
        "u_threshold":  [2.0, 10.0],
    },

    "solution_steps_latex": [
        (
            "**Step 1 — Identify the inverse transformation**\n"
            "From $U = X+Y,\\ V = X/(X+Y)$, solve:\n"
            "$$X = UV, \\qquad Y = U(1-V)$$\n"
            "Support: $U > 0$, $V \\in (0,1)$."
        ),
        (
            "**Step 2 — Compute the Jacobian**\n"
            "$$\\mathbf{J} = \\frac{\\partial(x,y)}{\\partial(u,v)} = "
            "\\begin{vmatrix} v & u \\\\\\\\ 1-v & -u \\end{vmatrix} = "
            "-uv - u(1-v) = -u$$\n"
            "$$|J| = u$$"
        ),
        (
            "**Step 3 — Joint density transformation**\n"
            "$$f_{X,Y}(x,y) = \\lambda_1 e^{-\\lambda_1 x}\\cdot\\lambda_2 e^{-\\lambda_2 y}$$\n"
            "Substitute $x = uv$, $y = u(1-v)$:\n"
            "$$f_{U,V}(u,v) = \\lambda_1\\lambda_2\\, u\\, "
            "e^{-(\\lambda_1 v + \\lambda_2(1-v))u}$$"
        ),
        (
            "**Step 4 — Factor into marginals (independence)**\n"
            "$$f_{U,V}(u,v) = \\underbrace{(\\lambda_1 v + \\lambda_2(1-v))^2 u\\, "
            "e^{-(\\lambda_1 v + \\lambda_2(1-v))u}}_{\\text{Gamma}(2, \\lambda_1 v + \\lambda_2(1-v))} "
            "\\cdot \\underbrace{\\frac{\\lambda_1\\lambda_2}{(\\lambda_1 v + "
            "\\lambda_2(1-v))^2}}_{\\text{Beta density in }v}$$\n"
            "When $\\lambda_1 = \\lambda_2 = \\lambda$: $U \\sim \\mathrm{Gamma}(2,\\lambda)$ "
            "and $V \\sim \\mathrm{Uniform}(0,1)$, independent."
        ),
        (
            "**Step 5 — Requested probabilities**\n"
            "$$P(U > u_0) = \\int_{u_0}^{\\infty} f_U(u)\\,du$$\n"
            "For the equal-rate case: $P(U>u_0) = (1+\\lambda u_0)e^{-\\lambda u_0}$.\n"
            "$$E[V] = E\\!\\left[\\frac{X}{X+Y}\\right] = \\frac{\\lambda_2}{\\lambda_1+\\lambda_2}$$\n"
            "*Pitfall*: computing $E[X]/E[X+Y]$ instead of $E[X/(X+Y)]$ — these are not equal."
        ),
    ],

    "answer_formula": (
        "E[V] = \\\\frac{\\\\lambda_2}{\\\\lambda_1+\\\\lambda_2},\\\\quad"
        "P(U>u_0) = (1+\\\\lambda u_0)e^{-\\\\lambda u_0}\\;(\\\\text{equal rates})"
    ),

    "validation_python_fn": """
def validate(variables, user_answer):
    import math
    lam1 = round(1.0 / variables["mean_x"], 4)
    lam2 = round(1.0 / variables["mean_y"], 4)
    u0   = round(variables["u_threshold"], 4)
    ev   = round(lam2 / (lam1 + lam2), 4)
    # P(U > u0) for general case using gamma CDF complement
    # For simplicity validate E[V]
    try:
        ans = round(float(str(user_answer).replace(",", "")), 4)
        return abs(ans - ev) < 0.005
    except Exception:
        return False
""",

    "common_pitfalls": [
        "Confusing numerator and denominator in the Jacobian — always compute |∂(x,y)/∂(u,v)|.",
        "Computing E[X]/E[X+Y] instead of E[X/(X+Y)] — Jensen's inequality makes these unequal.",
        "Forgetting to verify the support (U > 0, V ∈ (0,1)) after the transformation.",
        "Missing the factor |J| = u when multiplying through f_{X,Y}.",
    ],

    "tags": ["Jacobian", "change-of-variables", "bivariate", "exponential", "P"],
}


# ══════════════════════════════════════════════════════════════════════════════
# FM TEMPLATE 03 — Convexity of a Geometrically Increasing Annuity-Due
# Difficulty: 8  |  Topic: Annuities — Duration & Convexity
# ══════════════════════════════════════════════════════════════════════════════

FM_TPL_03: Template = {
    "id": "FM-TPL-006",
    "exam_code": "FM",
    "topic": "Annuities",
    "subtopic_slug": "convexity-geometric-annuity-due",
    "difficulty": 8,

    "template_text": (
        "An annuity-due pays $C$ at time $0$, $C(1+g)$ at time $1$, "
        "$C(1+g)^2$ at time $2$, $\\ldots$, $C(1+g)^{{n-1}}$ at time $n-1$, "
        "where $C = {C}$, $g = {g_pct}\\%$ (annual growth rate), "
        "$n = {n}$ payments, and the annual effective rate $i = {i_pct}\\%$.\n"
        "Let $j = (i-g)/(1+g)$ be the adjusted rate.\n"
        "(a) Find the present value $\\mathrm{{PV}}$.\n"
        "(b) Compute the Macaulay duration $D_{{\\mathrm{{mac}}}}$.\n"
        "(c) Compute the convexity $\\mathcal{{C}}$ and the approximate price change "
        "for a $+{dy_bps}$ bps shift."
    ),

    "variables_config": {
        "C":   [500, 5000],
        "g":   [0.01, 0.05],
        "n":   [5, 25],
        "i":   [0.04, 0.10],
        "dy":  [0.0025, 0.02],
    },

    "solution_steps_latex": [
        (
            "**Step 1 — Adjusted rate and geometric annuity-due PV**\n"
            "Define $j = (i-g)/(1+g)$ (requires $i \\neq g$).\n"
            "The present value of a geometric annuity-due is:\n"
            "$$\\mathrm{PV} = C\\,(1+g)^{-1}\\cdot"
            "\\ddot{a}_{\\overline{n}|j}\\cdot(1+g) = "
            "C\\cdot\\ddot{a}_{\\overline{n}|j}$$\n"
            "where $\\ddot{a}_{\\overline{n}|j} = \\dfrac{1-\\left(\\frac{1+g}{1+i}\\right)^n}{i-g}$.\n"
            "*Pitfall*: using $a_{\\overline{n}|j}$ (annuity-immediate) — annuity-due has payments at $t=0,1,\\ldots,n-1$."
        ),
        (
            "**Step 2 — Discount factor and effective PV factor**\n"
            "Let $w = (1+g)/(1+i)$ (the \"growth-discounted\" factor, $w < 1$ when $i > g$).\n"
            "$$\\mathrm{PV} = C\\cdot\\frac{1-w^n}{i-g}$$\n"
            "Each payment $C(1+g)^t$ at time $t$ has present value $C\\cdot w^t$."
        ),
        (
            "**Step 3 — Macaulay duration**\n"
            "$$D_{\\mathrm{mac}} = \\frac{\\sum_{t=0}^{n-1} t \\cdot C w^t}{\\mathrm{PV}} = "
            "\\frac{C\\,w\\,\\frac{d}{dw}\\left(\\sum_{t=0}^{n-1} w^t\\right)}{\\mathrm{PV}}$$\n"
            "Using the geometric-series derivative:\n"
            "$$D_{\\mathrm{mac}} = \\frac{w}{1-w} - \\frac{n w^n}{1-w^n}$$\n"
            "*Pitfall*: summing from $t=1$ instead of $t=0$ (annuity-due starts at $t=0$)."
        ),
        (
            "**Step 4 — Convexity**\n"
            "$$\\mathcal{C} = \\frac{1}{(1+i)^2\\,\\mathrm{PV}}"
            "\\sum_{t=0}^{n-1} t(t+1)\\,C w^t$$\n"
            "Compute using the second derivative of the geometric series:\n"
            "$$\\sum_{t=0}^{n-1}t(t+1)w^t = "
            "\\frac{2w^2(1-w^{n-1})}{(1-w)^3} - "
            "\\frac{2(n-1)nw^{n+1}}{(1-w)^2} + \\cdots$$"
        ),
        (
            "**Step 5 — Price-change approximation**\n"
            "$$\\Delta\\mathrm{PV} \\approx "
            "-D_{\\mathrm{mod}}\\cdot\\mathrm{PV}\\cdot\\Delta i "
            "+ \\tfrac{1}{2}\\mathcal{C}\\cdot\\mathrm{PV}\\cdot(\\Delta i)^2$$\n"
            "where $D_{\\mathrm{mod}} = D_{\\mathrm{mac}}/(1+i)$.\n"
            "*Pitfall*: using $D_{\\mathrm{mac}}$ (not $D_{\\mathrm{mod}}$) in the first-order term; "
            "omitting $\\tfrac{1}{2}$ in the convexity term."
        ),
    ],

    "answer_formula": (
        "\\\\mathrm{PV} = C\\\\cdot\\\\frac{1-w^n}{i-g},\\\\quad"
        "D_{\\\\mathrm{mac}} = \\\\frac{w}{1-w} - \\\\frac{nw^n}{1-w^n}"
    ),

    "validation_python_fn": """
def validate(variables, user_answer):
    C  = round(variables["C"], 4)
    g  = round(variables["g"], 4)
    n  = int(variables["n"])
    i  = round(variables["i"], 4)
    w  = round((1 + g) / (1 + i), 8)
    pv = round(C * (1 - w**n) / (i - g), 4)
    try:
        ans = round(float(str(user_answer).replace(",", "")), 4)
        return abs(ans - pv) / max(abs(pv), 1) < 0.005
    except Exception:
        return False
""",

    "common_pitfalls": [
        "Using a_{n|j} (annuity-immediate) instead of ä_{n|j} (annuity-due) — shift payments by one period.",
        "Using D_mac in the price-change formula instead of D_mod = D_mac / (1+i).",
        "Forgetting the 1/2 factor in the convexity correction term.",
        "Summing duration from t=1 instead of t=0 for an annuity-due.",
    ],

    "tags": ["geometric-annuity-due", "convexity", "modified-duration", "FM"],
}


# ─── Registry ─────────────────────────────────────────────────────────────────

SEED_TEMPLATES: list[Template] = [FM_TPL_01, FM_TPL_02, P_TPL_01, P_TPL_02, P_TPL_03, FM_TPL_03]

_BY_ID: dict[str, Template] = {t["id"]: t for t in SEED_TEMPLATES}


def get_template_by_id(template_id: str) -> Template | None:
    return _BY_ID.get(template_id)


def get_templates_by_exam(exam_code: str) -> list[Template]:
    return [t for t in SEED_TEMPLATES if t["exam_code"] == exam_code]


def get_templates_by_subtopic(subtopic_slug: str) -> list[Template]:
    return [t for t in SEED_TEMPLATES if t.get("subtopic_slug") == subtopic_slug]
