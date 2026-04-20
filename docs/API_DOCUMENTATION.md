# API Documentation

Complete API reference for the SOA Exam Prep Platform.

Base URL: `https://api.soa-prep.com/v1`

---

## Authentication Endpoints

### Register User

Creates a new user account.

**Method:** `POST`
**Path:** `/auth/register`
**Auth Required:** No

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "exam_targets": ["P", "FM"],
  "experience_level": "beginner"
}
```

**Response Body (201 Created):**
```json
{
  "user_id": "usr_1a2b3c4d5e",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2026-04-15T10:30:00Z",
  "exam_targets": ["P", "FM"],
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_expires_in": 3600
}
```

**Possible Errors:**
- `400 Bad Request`: Invalid email format or weak password
- `409 Conflict`: Email already registered
- `422 Unprocessable Entity`: Missing required fields

---

### Login

Authenticates user and returns access token.

**Method:** `POST`
**Path:** `/auth/login`
**Auth Required:** No

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response Body (200 OK):**
```json
{
  "user_id": "usr_1a2b3c4d5e",
  "email": "user@example.com",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_expires_in": 3600
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid credentials
- `404 Not Found`: User not found
- `429 Too Many Requests`: Too many login attempts

---

### Refresh Token

Obtains a new access token using a refresh token.

**Method:** `POST`
**Path:** `/auth/refresh`
**Auth Required:** No

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response Body (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_expires_in": 3600
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or expired refresh token
- `400 Bad Request`: Missing token

---

## Question Endpoints

### Get Next Question

Retrieves the next adaptive question for the learner.

**Method:** `GET`
**Path:** `/questions/next`
**Auth Required:** Yes (Bearer token)

**Query Parameters:**
```
exam_id: string (required) - "P", "FM", "FAM", "ALTAM", "ASTAM", "SRM", or "PA"
session_id: string (required) - Current session identifier
```

**Response Body (200 OK):**
```json
{
  "question_id": "q_5f9a3c1b2e8d",
  "exam_id": "P",
  "topic": "Conditional Probability",
  "difficulty": 0.5,
  "question_text": "A health insurance company analyzes claims data...",
  "choices": [
    {
      "choice_id": "A",
      "text": "0.105"
    },
    {
      "choice_id": "B",
      "text": "0.35"
    },
    {
      "choice_id": "C",
      "text": "0.467"
    },
    {
      "choice_id": "D",
      "text": "0.70"
    },
    {
      "choice_id": "E",
      "text": "0.85"
    }
  ],
  "estimated_time_seconds": 180,
  "question_number": 15,
  "total_questions_in_session": 40
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Session not found
- `422 Unprocessable Entity`: Invalid exam_id

---

### Submit Question Response

Submits learner's answer and receives feedback.

**Method:** `POST`
**Path:** `/questions/submit`
**Auth Required:** Yes (Bearer token)

**Request Body:**
```json
{
  "question_id": "q_5f9a3c1b2e8d",
  "session_id": "sess_7k9l2m5n8o",
  "chosen_answer": "C",
  "time_spent_seconds": 125,
  "is_flagged": false
}
```

**Response Body (200 OK):**
```json
{
  "question_id": "q_5f9a3c1b2e8d",
  "correct": true,
  "correct_answer": "C",
  "explanation": "Using Bayes' Theorem: P(P|F) = P(F|P) × P(P) / P(F) ≈ 0.467",
  "detailed_solution": "Step 1: Calculate P(F) using total probability...",
  "learner_theta": 0.45,
  "learner_theta_change": 0.12,
  "topic_mastery": 0.62,
  "readiness_score": 0.58,
  "hint_available": false,
  "similar_questions_available": true,
  "video_reference": "lesson_conditional_probability_01"
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Question or session not found
- `409 Conflict`: Question already answered
- `422 Unprocessable Entity`: Invalid answer choice

---

### Get Question Explanation

Retrieves detailed explanation for a question.

**Method:** `GET`
**Path:** `/questions/{question_id}/explanation`
**Auth Required:** Yes (Bearer token)

**Response Body (200 OK):**
```json
{
  "question_id": "q_5f9a3c1b2e8d",
  "correct_answer": "C",
  "explanation_short": "Using Bayes' Theorem to reverse conditional probabilities.",
  "explanation_detailed": "Bayes' Theorem states that P(A|B) = P(B|A) × P(A) / P(B)...",
  "step_by_step_solution": [
    {
      "step": 1,
      "description": "Identify what we know",
      "details": "P(P) = 0.15, P(F|P) = 0.70"
    },
    {
      "step": 2,
      "description": "Calculate total probability of F",
      "details": "P(F) = P(F|P)×P(P) + P(F|¬P)×P(¬P) = 0.105 + 0.085 = 0.19"
    }
  ],
  "common_mistakes": [
    "Confusing P(F|P) with P(P|F)",
    "Forgetting to divide by P(F)"
  ],
  "topic_tags": ["conditional_probability", "bayes_theorem"],
  "difficulty_rating": 6,
  "related_topics": ["total_probability", "independence"]
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Question not found

---

## Adaptive State Endpoints

### Get Session State

Retrieves current session state and learner progress.

**Method:** `GET`
**Path:** `/adaptive/state`
**Auth Required:** Yes (Bearer token)

**Query Parameters:**
```
session_id: string (required) - Current session identifier
```

**Response Body (200 OK):**
```json
{
  "session_id": "sess_7k9l2m5n8o",
  "exam_id": "P",
  "user_id": "usr_1a2b3c4d5e",
  "started_at": "2026-04-15T10:30:00Z",
  "current_question_number": 15,
  "total_questions": 40,
  "estimated_questions_remaining": 25,
  "time_elapsed_minutes": 45,
  "estimated_time_remaining_minutes": 55,
  "current_ability_theta": 0.45,
  "readiness_score": 0.58,
  "pass_likelihood_percent": 68,
  "topic_progress": {
    "Probability Distributions": {
      "mastery": 0.72,
      "questions_attempted": 8,
      "average_accuracy": 0.875
    },
    "Conditional Probability": {
      "mastery": 0.58,
      "questions_attempted": 5,
      "average_accuracy": 0.60
    },
    "Continuous Distributions": {
      "mastery": 0.35,
      "questions_attempted": 2,
      "average_accuracy": 0.50
    }
  },
  "session_statistics": {
    "questions_correct": 10,
    "questions_incorrect": 5,
    "accuracy_percent": 66.7,
    "average_time_per_question_seconds": 180,
    "questions_flagged": 2
  }
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Session not found
- `422 Unprocessable Entity`: Invalid session_id

---

### Get Next Question Recommendation

Returns the recommended next question without presenting it yet.

**Method:** `GET`
**Path:** `/adaptive/next`
**Auth Required:** Yes (Bearer token)

**Query Parameters:**
```
session_id: string (required)
exam_id: string (required)
```

**Response Body (200 OK):**
```json
{
  "recommended_question_id": "q_2e8d5f9a3c",
  "topic": "Conditional Probability",
  "estimated_difficulty": 0.48,
  "rationale": "This question addresses your weak area (Conditional Probability with 58% mastery) and is optimally difficult for your ability level.",
  "fisher_information_score": 0.892,
  "topic_coverage_reason": "Only 5 questions answered in this topic; we're increasing exposure.",
  "preview_available": true
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Session not found

---

### Start New Session

Creates a new testing session.

**Method:** `POST`
**Path:** `/adaptive/sessions`
**Auth Required:** Yes (Bearer token)

**Request Body:**
```json
{
  "exam_id": "P",
  "session_type": "practice",
  "target_questions": 40,
  "difficulty_preset": "adaptive"
}
```

**Response Body (201 Created):**
```json
{
  "session_id": "sess_7k9l2m5n8o",
  "user_id": "usr_1a2b3c4d5e",
  "exam_id": "P",
  "session_type": "practice",
  "status": "active",
  "started_at": "2026-04-15T10:30:00Z",
  "target_questions": 40,
  "questions_completed": 0,
  "session_token": "st_9z8y7x6w5v",
  "estimated_duration_minutes": 120
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `400 Bad Request`: Invalid exam_id or session_type
- `409 Conflict`: Active session already exists

---

### End Session

Completes a testing session and generates final report.

**Method:** `POST`
**Path:** `/adaptive/sessions/{session_id}/end`
**Auth Required:** Yes (Bearer token)

**Request Body:**
```json
{
  "session_id": "sess_7k9l2m5n8o",
  "reason": "completed"
}
```

**Response Body (200 OK):**
```json
{
  "session_id": "sess_7k9l2m5n8o",
  "status": "completed",
  "completed_at": "2026-04-15T12:30:00Z",
  "duration_minutes": 120,
  "questions_completed": 38,
  "questions_correct": 26,
  "accuracy_percent": 68.4,
  "final_theta": 0.52,
  "final_readiness_score": 0.61,
  "exam_pass_likelihood_percent": 72,
  "recommendation": "You are ready to take the exam. Focus on reviewing Continuous Distributions before test day.",
  "topic_mastery_summary": {
    "Probability Distributions": 0.78,
    "Conditional Probability": 0.64,
    "Continuous Distributions": 0.42
  }
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Session not found
- `409 Conflict`: Session already ended

---

## Analytics Endpoints

### Get Progress Report

Retrieves learner's overall progress across all sessions.

**Method:** `GET`
**Path:** `/analytics/progress`
**Auth Required:** Yes (Bearer token)

**Query Parameters:**
```
days_back: integer (optional, default 30) - Number of days to include
exam_id: string (optional) - Filter to specific exam
```

**Response Body (200 OK):**
```json
{
  "user_id": "usr_1a2b3c4d5e",
  "summary": {
    "total_sessions": 12,
    "total_questions_attempted": 480,
    "total_correct": 328,
    "overall_accuracy_percent": 68.3,
    "average_session_duration_minutes": 95,
    "days_active": 25,
    "streak_days": 7
  },
  "exam_progress": [
    {
      "exam_id": "P",
      "status": "in_progress",
      "current_theta": 0.52,
      "readiness_score": 0.61,
      "pass_likelihood_percent": 72,
      "sessions_completed": 8,
      "total_questions": 320,
      "topic_mastery_average": 0.64
    },
    {
      "exam_id": "FM",
      "status": "not_started",
      "current_theta": null,
      "readiness_score": null,
      "pass_likelihood_percent": null,
      "sessions_completed": 0,
      "total_questions": 0,
      "topic_mastery_average": null
    }
  ],
  "trending": {
    "last_7_days_accuracy": 0.71,
    "last_30_days_accuracy": 0.68,
    "improvement_percent": 4.4
  }
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token

---

### Get Readiness Report

Detailed readiness assessment for a specific exam.

**Method:** `GET`
**Path:** `/analytics/readiness/{exam_id}`
**Auth Required:** Yes (Bearer token)

**Response Body (200 OK):**
```json
{
  "exam_id": "P",
  "user_id": "usr_1a2b3c4d5e",
  "readiness_score": 0.61,
  "readiness_level": "ready_with_review",
  "pass_likelihood_percent": 72,
  "last_updated": "2026-04-15T12:30:00Z",
  "components": {
    "ability_theta": {
      "score": 0.52,
      "weight": 0.70,
      "contribution": 0.364,
      "interpretation": "Solid understanding of material"
    },
    "topic_mastery_average": {
      "score": 0.64,
      "weight": 0.15,
      "contribution": 0.096,
      "interpretation": "Competent across topics"
    },
    "consistency": {
      "score": 0.82,
      "weight": 0.15,
      "contribution": 0.123,
      "interpretation": "Consistent performance"
    }
  },
  "weak_topics": [
    {
      "topic": "Continuous Distributions",
      "mastery": 0.42,
      "questions_attempted": 12,
      "recommended_action": "Focus practice on uniform and normal distributions"
    },
    {
      "topic": "Conditional Probability",
      "mastery": 0.64,
      "questions_attempted": 18,
      "recommended_action": "Review Bayes' Theorem applications"
    }
  ],
  "strong_topics": [
    {
      "topic": "Probability Distributions",
      "mastery": 0.78,
      "questions_attempted": 24
    }
  ],
  "recommendation": "You are ready to sit for Exam P. Your pass likelihood is 72%. Before test day, review Continuous Distributions with focused practice.",
  "days_until_recommended_ready": 0,
  "estimated_questions_to_mastery": 45
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Exam not found or no progress on exam

---

### Get Weak Areas

Returns detailed analysis of weak areas and improvement recommendations.

**Method:** `GET`
**Path:** `/analytics/weaknesses`
**Auth Required:** Yes (Bearer token)

**Query Parameters:**
```
exam_id: string (required)
threshold: number (optional, default 0.6) - Mastery level below which topics are considered weak
```

**Response Body (200 OK):**
```json
{
  "exam_id": "P",
  "weak_areas": [
    {
      "topic": "Continuous Distributions",
      "mastery": 0.42,
      "confidence_interval": [0.35, 0.49],
      "questions_answered": 12,
      "correct_answers": 5,
      "accuracy_percent": 41.7,
      "item_difficulty_average": 0.55,
      "learner_theta_average": 0.52,
      "error_patterns": [
        "Confusing exponential and gamma distributions (3 errors)",
        "Incorrect CDF calculations (2 errors)",
        "Misunderstanding parameter relationships (1 error)"
      ],
      "recommended_resources": [
        {
          "type": "video_lesson",
          "title": "Understanding Exponential and Gamma Distributions",
          "duration_minutes": 25,
          "difficulty": "intermediate"
        },
        {
          "type": "practice_set",
          "title": "CDF and PDF Calculations",
          "estimated_time_minutes": 45,
          "question_count": 15
        }
      ]
    }
  ],
  "priority_ranking": [
    "Continuous Distributions",
    "Conditional Probability",
    "Order Statistics"
  ],
  "improvement_plan": {
    "estimated_hours_needed": 12,
    "recommended_daily_practice_minutes": 60,
    "days_to_mastery": 20
  }
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Exam not found

---

## Study Plan Endpoints

### Get Personalized Study Plan

Generates a customized study plan based on current progress.

**Method:** `GET`
**Path:** `/study-plan/{exam_id}`
**Auth Required:** Yes (Bearer token)

**Query Parameters:**
```
target_date: string (optional, ISO 8601) - Desired exam date
daily_hours_available: number (optional, default 2) - Hours available per day
```

**Response Body (200 OK):**
```json
{
  "exam_id": "P",
  "plan_id": "plan_4m7n2p5q8r",
  "created_at": "2026-04-15T10:00:00Z",
  "target_exam_date": "2026-06-15",
  "days_remaining": 61,
  "estimated_hours_needed": 48,
  "daily_commitment_hours": 2,
  "feasibility": "on_track",
  "phases": [
    {
      "phase": 1,
      "title": "Foundation Review",
      "duration_days": 14,
      "topics": [
        "Probability Distributions",
        "Basic Probability Rules"
      ],
      "daily_study_minutes": 90,
      "daily_practice_questions": 15,
      "milestones": [
        {
          "day": 7,
          "milestone": "Complete video lessons on distributions",
          "assessment": "15-question quiz"
        }
      ]
    },
    {
      "phase": 2,
      "title": "Targeted Weakness Training",
      "duration_days": 21,
      "focus_topics": [
        "Continuous Distributions",
        "Conditional Probability"
      ],
      "daily_study_minutes": 120,
      "daily_practice_questions": 20
    },
    {
      "phase": 3,
      "title": "Comprehensive Review and Practice Exams",
      "duration_days": 21,
      "daily_study_minutes": 120,
      "practice_full_exams": 4,
      "targeted_practice_sets": 8
    },
    {
      "phase": 4,
      "title": "Final Polish",
      "duration_days": 5,
      "daily_study_minutes": 90,
      "focus": "Review weak question types and refine test-taking strategy"
    }
  ],
  "weekly_breakdown": [
    {
      "week": 1,
      "daily_commitment_minutes": 90,
      "focus": "Probability Distributions and basic rules",
      "questions_to_complete": 105,
      "estimated_completion_date": "2026-04-21"
    }
  ]
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Exam not found or no progress record

---

### Update Study Plan

Modifies an existing study plan based on new constraints or progress.

**Method:** `PUT`
**Path:** `/study-plan/{plan_id}`
**Auth Required:** Yes (Bearer token)

**Request Body:**
```json
{
  "target_date": "2026-07-01",
  "daily_hours_available": 1.5,
  "adjust_for_pace": true
}
```

**Response Body (200 OK):**
```json
{
  "plan_id": "plan_4m7n2p5q8r",
  "updated_at": "2026-04-15T14:00:00Z",
  "new_target_date": "2026-07-01",
  "new_days_remaining": 77,
  "feasibility": "achievable_with_effort",
  "adjustments_made": [
    "Extended timeline from 61 to 77 days",
    "Reduced daily commitment to 1.5 hours",
    "Maintained all phase content"
  ]
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Study plan not found

---

## Video Lesson Endpoints

### List Video Lessons

Retrieves available video lessons for an exam.

**Method:** `GET`
**Path:** `/lessons/video`
**Auth Required:** Yes (Bearer token)

**Query Parameters:**
```
exam_id: string (required)
topic: string (optional) - Filter by topic
difficulty: string (optional) - "beginner", "intermediate", "advanced"
```

**Response Body (200 OK):**
```json
{
  "exam_id": "P",
  "total_lessons": 24,
  "lessons": [
    {
      "lesson_id": "vid_1a2b3c4d5e",
      "title": "Understanding Conditional Probability",
      "topic": "Conditional Probability",
      "description": "Learn how to calculate and interpret conditional probability with real-world examples.",
      "duration_minutes": 15,
      "difficulty": "intermediate",
      "created_at": "2026-01-15T00:00:00Z",
      "instructor": "Dr. Jane Smith",
      "learning_objectives": [
        "Understand the definition and notation of conditional probability",
        "Apply Bayes' Theorem to real-world problems",
        "Distinguish between independent and dependent events"
      ],
      "estimated_completion_time": 20,
      "prerequisite_topics": ["Basic Probability"],
      "related_questions_count": 18
    }
  ]
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Exam not found

---

### Get Video Lesson Details

Retrieves full details of a specific video lesson.

**Method:** `GET`
**Path:** `/lessons/video/{lesson_id}`
**Auth Required:** Yes (Bearer token)

**Response Body (200 OK):**
```json
{
  "lesson_id": "vid_1a2b3c4d5e",
  "title": "Understanding Conditional Probability",
  "topic": "Conditional Probability",
  "description": "Learn how to calculate and interpret conditional probability with real-world examples.",
  "duration_minutes": 15,
  "difficulty": "intermediate",
  "video_url": "https://videos.soa-prep.com/lesson_cp_001.mp4",
  "transcript": "Welcome to this lesson on conditional probability...",
  "learning_objectives": [
    "Understand the definition and notation",
    "Apply Bayes' Theorem",
    "Distinguish independence"
  ],
  "sections": [
    {
      "timestamp": "0:00",
      "title": "Introduction",
      "content": "Opening motivation for conditional probability"
    },
    {
      "timestamp": "1:30",
      "title": "Definition and Notation",
      "content": "Formal definition of P(A|B)"
    }
  ],
  "related_questions": [
    {
      "question_id": "q_5f9a3c1b2e8d",
      "title": "Medical test example",
      "difficulty": 0.6
    }
  ],
  "user_progress": {
    "watched": true,
    "watched_at": "2026-04-14T15:30:00Z",
    "duration_watched_minutes": 15,
    "completion_percent": 100
  }
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Lesson not found

---

## Admin Endpoints

### Get All Users (Admin)

Lists all users in the system.

**Method:** `GET`
**Path:** `/admin/users`
**Auth Required:** Yes (Bearer token with admin role)

**Query Parameters:**
```
page: integer (optional, default 1)
limit: integer (optional, default 50, max 500)
exam_id: string (optional) - Filter by target exam
active_days: integer (optional) - Show users active in last N days
```

**Response Body (200 OK):**
```json
{
  "total_count": 1247,
  "page": 1,
  "limit": 50,
  "users": [
    {
      "user_id": "usr_1a2b3c4d5e",
      "email": "user@example.com",
      "first_name": "John",
      "created_at": "2026-03-15T00:00:00Z",
      "last_active": "2026-04-15T12:30:00Z",
      "exam_targets": ["P", "FM"],
      "total_questions": 320,
      "accuracy_percent": 68.3,
      "current_readiness": 0.61
    }
  ]
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Not authorized as admin

---

### Get Question Analytics (Admin)

Retrieves performance data for a specific question.

**Method:** `GET`
**Path:** `/admin/questions/{question_id}/analytics`
**Auth Required:** Yes (Bearer token with admin role)

**Response Body (200 OK):**
```json
{
  "question_id": "q_5f9a3c1b2e8d",
  "title": "Conditional Probability Example",
  "exam_id": "P",
  "topic": "Conditional Probability",
  "calibrated_parameters": {
    "difficulty": 0.48,
    "discrimination": 1.2,
    "guessing": 0.15
  },
  "statistics": {
    "times_answered": 245,
    "correct_answers": 158,
    "difficulty_index": 0.645,
    "discrimination_index": 0.42,
    "point_biserial_correlation": 0.38
  },
  "performance_by_ability": [
    {
      "ability_range": "[-3.0, -1.0]",
      "learners": 12,
      "correct": 2,
      "accuracy_percent": 16.7
    },
    {
      "ability_range": "[0.0, 1.0]",
      "learners": 78,
      "correct": 64,
      "accuracy_percent": 82.1
    }
  ],
  "common_wrong_answers": [
    {
      "answer": "A",
      "count": 35,
      "percent": 14.3,
      "likely_misconception": "Forgot to divide by total probability"
    }
  ],
  "item_fit": "good",
  "flag_for_review": false
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Not authorized as admin
- `404 Not Found`: Question not found

---

### Create Question (Admin)

Adds a new question to the item bank.

**Method:** `POST`
**Path:** `/admin/questions`
**Auth Required:** Yes (Bearer token with admin role)

**Request Body:**
```json
{
  "exam_id": "P",
  "topic": "Conditional Probability",
  "question_text": "A patient tests positive for a rare disease...",
  "choices": [
    {"choice": "A", "text": "0.05"},
    {"choice": "B", "text": "0.10"}
  ],
  "correct_answer": "A",
  "explanation": "Using Bayes' Theorem...",
  "difficulty_estimate": 0.6,
  "source": "original",
  "author": "admin_user_id"
}
```

**Response Body (201 Created):**
```json
{
  "question_id": "q_new_123abc",
  "exam_id": "P",
  "topic": "Conditional Probability",
  "created_at": "2026-04-15T15:00:00Z",
  "status": "pending_calibration"
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Not authorized as admin
- `400 Bad Request`: Invalid question format
- `422 Unprocessable Entity`: Missing required fields

---

### Update Question (Admin)

Modifies an existing question.

**Method:** `PUT`
**Path:** `/admin/questions/{question_id}`
**Auth Required:** Yes (Bearer token with admin role)

**Request Body:**
```json
{
  "explanation": "Updated explanation with more detail...",
  "difficulty_estimate": 0.65
}
```

**Response Body (200 OK):**
```json
{
  "question_id": "q_5f9a3c1b2e8d",
  "updated_at": "2026-04-15T15:30:00Z",
  "changes": ["explanation", "difficulty_estimate"]
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Not authorized as admin
- `404 Not Found`: Question not found

---

### Get System Analytics (Admin)

High-level platform analytics and statistics.

**Method:** `GET`
**Path:** `/admin/analytics`
**Auth Required:** Yes (Bearer token with admin role)

**Query Parameters:**
```
date_from: string (optional, ISO 8601)
date_to: string (optional, ISO 8601)
```

**Response Body (200 OK):**
```json
{
  "period": {
    "start": "2026-04-01T00:00:00Z",
    "end": "2026-04-15T23:59:59Z"
  },
  "users": {
    "total_users": 1247,
    "new_users": 142,
    "active_users": 856,
    "daily_active_average": 612
  },
  "questions": {
    "total_questions_attempted": 125480,
    "total_correct": 87234,
    "platform_accuracy_percent": 69.5
  },
  "sessions": {
    "total_sessions": 3245,
    "average_session_duration_minutes": 98,
    "average_questions_per_session": 38.6
  },
  "exams": [
    {
      "exam_id": "P",
      "active_learners": 342,
      "average_readiness": 0.58,
      "estimated_pass_rate_percent": 71
    }
  ]
}
```

**Possible Errors:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Not authorized as admin

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing authentication token",
    "status": 401,
    "timestamp": "2026-04-15T15:30:00Z",
    "request_id": "req_7a8b9c0d1e"
  }
}
```

---

## Rate Limiting

The API implements rate limiting:

- **Authenticated users:** 1000 requests per hour
- **Unauthenticated users:** 100 requests per hour
- **Admin endpoints:** 500 requests per hour

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1713189000
```

---

## Pagination

List endpoints support pagination:

**Query Parameters:**
```
page: integer (default: 1)
limit: integer (default: 20, max: 500)
sort: string (optional) - Field to sort by
sort_order: string (optional) - "asc" or "desc"
```

**Response includes:**
```json
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_count": 847,
    "total_pages": 43,
    "has_next": true,
    "has_previous": false
  }
}
```

---

This API documentation is current as of April 2026 and covers all major endpoints for the SOA Exam Prep Platform.
