/**
 * Extended question schema — production-ready for Next.js / FastAPI.
 *
 * Differences from the base Question type in types/index.ts:
 *   - difficulty is a 1-10 numeric scale (not enum)
 *   - solution is split into calculation + concept (LaTeX-friendly)
 *   - videoExplanation carries YouTube URL + timestamp for deep-link
 *   - spacedRepetition metadata embedded for frontend caching
 *   - syllabus traceability: learningObjective + syllabusWeight
 */

export interface QuestionV2 {
  id: string;                    // e.g. "P-042"
  exam: SOAExam;
  topicId: string;               // e.g. "conditional-probability" (slug)
  topicDbId?: number;            // numeric FK used by the API for video lookups
  topicName: string;             // human-readable
  syllabusSection: string;       // e.g. "Section 3B" from SOA syllabus PDF
  learningObjective: string;     // exact LO from SOA syllabus
  syllabusWeight: number;        // 0–1 approximate exam weight for this topic

  stem: string;                  // question text (KaTeX-ready LaTeX in $...$)
  choices: ChoiceV2[];
  difficulty: number;            // 1–10
  estimatedSeconds: number;      // expected time to solve

  solution: Solution;
  videoExplanation?: VideoExplanation;

  source: QuestionSource;
  tags: string[];                // e.g. ["poisson", "pgf", "generating-functions"]
  createdAt: string;             // ISO 8601
  updatedAt: string;
}

export interface ChoiceV2 {
  label: string;                 // "A" | "B" | "C" | "D" | "E"
  text: string;                  // KaTeX-ready
  correct: boolean;
  distractor?: string;           // why a student might (wrongly) pick this
}

export interface Solution {
  calculation: string;           // step-by-step worked solution (KaTeX)
  concept: string;               // underlying theorem/formula (KaTeX)
  commonMistakes?: string[];     // plain text
}

export interface VideoExplanation {
  videoId: string;               // YouTube video ID
  channelName: string;           // e.g. "The Infinite Actuary", "Coach Bora"
  url: string;                   // full YouTube URL
  timestampSeconds: number;      // deep-link to exact moment
  clipTitle: string;             // description of what's covered at that timestamp
  durationSeconds: number;       // length of relevant clip
}

export type SOAExam = 'P' | 'FM' | 'FAM' | 'ALTAM' | 'ASTAM' | 'SRM' | 'PA';

export interface QuestionSource {
  type: 'soa_official' | 'soa_sample' | 'generated' | 'community';
  reference?: string;            // e.g. "SOA Sample P Q#104", "SOA Nov 2019 #12"
  year?: number;
}

// ─── Database schema (PostgreSQL) ─────────────────────────────────────────────
//
// questions
//   id            CHAR(10)  PRIMARY KEY          -- "P-042"
//   exam          VARCHAR(6)                     -- 'P' | 'FM' ...
//   topic_id      UUID      REFERENCES topics(id)
//   stem          TEXT      NOT NULL             -- LaTeX string
//   difficulty    SMALLINT  CHECK (1..10)
//   est_seconds   SMALLINT
//   solution_calc TEXT
//   solution_conc TEXT
//   video_id      VARCHAR(20)                    -- YouTube video ID
//   video_ts      INT                            -- timestamp in seconds
//   source_type   VARCHAR(20)
//   source_ref    VARCHAR(100)
//   tags          TEXT[]
//   created_at    TIMESTAMPTZ DEFAULT now()
//
// choices
//   id            UUID      PRIMARY KEY
//   question_id   CHAR(10)  REFERENCES questions(id)
//   label         CHAR(1)
//   text          TEXT
//   correct       BOOLEAN
//   distractor    TEXT
//
// question_attempts
//   id            UUID      PRIMARY KEY
//   user_id       UUID      REFERENCES users(id)
//   question_id   CHAR(10)  REFERENCES questions(id)
//   session_id    UUID      REFERENCES sessions(id)
//   selected      CHAR(1)
//   correct       BOOLEAN
//   time_ms       INT
//   el_before     NUMERIC(4,2)
//   el_after      NUMERIC(4,2)
//   created_at    TIMESTAMPTZ DEFAULT now()
//
// sr_cards  (spaced repetition)
//   user_id       UUID
//   question_id   CHAR(10)
//   interval_days SMALLINT
//   ease_factor   NUMERIC(3,2)
//   repetitions   SMALLINT
//   due_date      TIMESTAMPTZ
//   last_reviewed TIMESTAMPTZ
//   PRIMARY KEY (user_id, question_id)
//
// user_el  (earned level per exam/topic)
//   user_id       UUID
//   exam          VARCHAR(6)
//   topic_id      UUID   NULLABLE    -- NULL = overall exam EL
//   el            NUMERIC(4,2)
//   total_answered INT
//   total_correct  INT
//   updated_at    TIMESTAMPTZ
//   PRIMARY KEY (user_id, exam, topic_id)
// ─────────────────────────────────────────────────────────────────────────────

// ─── Mock question (full schema example) ─────────────────────────────────────
export const MOCK_QUESTION: QuestionV2 = {
  id: 'P-042',
  exam: 'P',
  topicId: 'conditional-probability',
  topicName: 'Conditional Probability & Bayes',
  syllabusSection: 'Section 3',
  learningObjective:
    'Calculate and interpret conditional probabilities using Bayes\u2019 theorem and the law of total probability.',
  syllabusWeight: 0.14,

  stem: 'An insurance company classifies drivers as Low-risk ($L$) or High-risk ($H$). '
    + '70\\% are Low-risk with annual claim probability $0.05$; '
    + '30\\% are High-risk with annual claim probability $0.40$. '
    + 'A randomly selected driver files a claim. '
    + 'Find $P(\\text{High-risk} \\mid \\text{claim filed})$.',
  difficulty: 4,
  estimatedSeconds: 180,

  choices: [
    {
      label: 'A',
      text: '$0.7742$',
      correct: true,
    },
    {
      label: 'B',
      text: '$0.3000$',
      correct: false,
      distractor: 'This is the prior $P(H)$, ignoring the claim evidence.',
    },
    {
      label: 'C',
      text: '$0.4000$',
      correct: false,
      distractor: 'This is $P(\\text{claim}\\mid H)$, not the posterior.',
    },
    {
      label: 'D',
      text: '$0.5455$',
      correct: false,
      distractor: 'Incorrect denominator — total probability not applied correctly.',
    },
    {
      label: 'E',
      text: '$0.1200$',
      correct: false,
      distractor: '$P(H)\\times P(\\text{claim}\\mid H) = 0.12$, but this is the joint, not conditional.',
    },
  ],

  solution: {
    calculation:
      '$P(\\text{claim}) = P(\\text{claim}\\mid L)P(L) + P(\\text{claim}\\mid H)P(H) '
      + '= 0.05 \\times 0.70 + 0.40 \\times 0.30 = 0.035 + 0.120 = 0.155$\\n\\n'
      + '$P(H \\mid \\text{claim}) = \\dfrac{P(\\text{claim}\\mid H)\\,P(H)}{P(\\text{claim})} '
      + '= \\dfrac{0.120}{0.155} \\approx 0.7742$',
    concept:
      "Bayes' theorem: $P(A\\mid B) = \\dfrac{P(B\\mid A)\\,P(A)}{P(B)}$. "
      + 'Denominator computed via the Law of Total Probability: $P(B) = \\sum_i P(B\\mid A_i)P(A_i)$.',
    commonMistakes: [
      'Using the prior P(H) = 0.30 directly without updating on the claim.',
      'Forgetting to compute the marginal P(claim) in the denominator.',
    ],
  },

  videoExplanation: {
    videoId: 'HZGCoVF3YvM',
    channelName: 'The Infinite Actuary',
    url: 'https://www.youtube.com/watch?v=HZGCoVF3YvM&t=432',
    timestampSeconds: 432,
    clipTitle: "Bayes' Theorem in Insurance — High-Risk Driver Example",
    durationSeconds: 480,
  },

  source: {
    type: 'soa_sample',
    reference: 'SOA Sample P Q#104',
    year: 2023,
  },

  tags: ['bayes-theorem', 'law-of-total-probability', 'insurance', 'posterior'],
  createdAt: '2024-01-15T00:00:00Z',
  updatedAt: '2024-04-01T00:00:00Z',
};
