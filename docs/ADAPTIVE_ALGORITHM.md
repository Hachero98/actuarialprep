# Adaptive Testing Algorithm Documentation

This document provides comprehensive technical documentation of the adaptive testing algorithm used in the SOA exam prep platform.

---

## Overview

The adaptive algorithm dynamically adjusts question difficulty and content based on learner performance. It employs three key components:

1. **Item Response Theory (IRT) 3-Parameter Logistic Model** for question difficulty calibration
2. **Bayesian Knowledge Tracing (BKT)** for skill mastery estimation
3. **Maximum Fisher Information** for optimal question selection

This combination ensures learners practice questions at the appropriate difficulty level and receive targeted feedback on weak areas.

---

## Component 1: Item Response Theory (3PL Model)

### Overview

The 3-Parameter Logistic (3PL) model describes the probability that a learner with ability $\theta$ answers a particular question correctly:

$$P(\theta) = c + (1-c) \cdot \frac{e^{a(θ-b)}}{1 + e^{a(θ-b)}}$$

### Parameters

- $\theta$ = learner's ability (latent trait), typically on a scale of -3 to +3
- $a$ = discrimination parameter (slope), typically 0.5 to 2.5
  - Higher $a$ means the question better discriminates between high and low ability learners
  - A question where all abilities answer similarly has low discrimination
- $b$ = difficulty parameter, on the same scale as $\theta$
  - When $\theta = b$, the probability of correct answer is roughly 0.5 (for $c = 0$)
  - Higher $b$ values indicate harder questions
- $c$ = pseudo-guessing parameter, typically 0.1 to 0.25
  - Represents the probability a random guesser gets the question right
  - For 5-choice multiple choice, pure guessing is 0.2
  - We use 0.15 to account for informed guesses

### Simplified 3PL Model Formula

$$P(\theta) = c + (1-c) \cdot \frac{1}{1 + e^{-a(θ-b)}}$$

Using the logit form:
$$\log\left(\frac{P(\theta) - c}{1-P(\theta)}\right) = a(\theta - b)$$

### Parameter Estimation

When a learner answers a question, we update estimates of their ability $\theta$ using **Item Calibration Data**. The platform pre-calibrates all questions using:

1. Historical data from previous test takers
2. Classical test theory statistics (item difficulty, item discrimination index)
3. Differential item functioning (DIF) analysis to detect biased items

For new questions or during ongoing use, we employ **Bayesian updating**:

$$P(\theta | \text{response}) \propto P(\text{response} | \theta) \cdot P(\theta)$$

where:
- $P(\text{response} | \theta)$ is given by the 3PL model
- $P(\theta)$ is a prior distribution (often normal with mean 0, SD 1)

### Expected Information

The Fisher Information function for a single question is:

$$I(\theta) = a^2 \cdot \frac{(1-P(\theta))P(\theta) - c^2(1-c)^2}{[P(\theta) - c]^2(1-P(\theta))^2}$$

Higher information at a particular ability level means the question provides more precision in estimating that ability.

---

## Component 2: Bayesian Knowledge Tracing (BKT)

### Overview

BKT models the learner's knowledge of specific skills (topics) over time. It tracks four probabilities:

1. **$L_0$** = Prior probability learner already knows the skill before practice
2. **$T$** = Probability learner learns the skill on each attempt
3. **$G$** = Probability learner guesses correctly despite not knowing
4. **$S$** = Probability learner slips (makes a careless error despite knowing)

### State Variable

The system maintains a belief about whether the learner knows each skill:

$$P(\text{Know}_t) = \text{Probability learner knows skill at time } t$$

### BKT Update Rules

**Initial State:**
$$P(\text{Know}_0) = L_0$$

**After Observing a Response:**

If the learner answers correctly:
$$P(\text{Know}_{t+1}) = \frac{P(\text{correct} | \text{Know}_t) \cdot P(\text{Know}_t)}{P(\text{correct})}$$

where:
- $P(\text{correct} | \text{Know}_t) = P(\text{Know}_t) \cdot (1-S) + (1-P(\text{Know}_t)) \cdot G$
- $P(\text{correct}) = P(\text{correct} | \text{Know}_t) \cdot P(\text{Know}_t) + P(\text{correct} | \neg\text{Know}_t) \cdot (1-P(\text{Know}_t))$

If the learner answers incorrectly:
$$P(\text{Know}_{t+1}) = \frac{P(\text{incorrect} | \text{Know}_t) \cdot P(\text{Know}_t)}{P(\text{incorrect})}$$

where:
- $P(\text{incorrect} | \text{Know}_t) = P(\text{Know}_t) \cdot S + (1-P(\text{Know}_t)) \cdot (1-G)$

**Learning Transition:**

After attempting a question, there's a probability $T$ that the learner acquires the skill:

$$P(\text{Know}_t) = P(\text{Know}_t) + T \cdot (1 - P(\text{Know}_t))$$

### Typical BKT Parameter Values

| Parameter | Symbol | Typical Range | Description |
|-----------|--------|---------------|-------------|
| Prior Knowledge | $L_0$ | 0.1 - 0.3 | Usually learners start with some background |
| Learning Rate | $T$ | 0.2 - 0.4 | Probability of learning from one attempt |
| Guessing | $G$ | 0.15 - 0.25 | For 5-choice multiple choice |
| Slipping | $S$ | 0.05 - 0.15 | Probability of careless error |

### Multi-Skill Modeling

For questions requiring multiple skills, BKT can be extended:

$$P(\text{correct}) = \prod_{i=1}^{k} P(\text{Know}_i)$$

assuming skills are independent. More sophisticated models account for skill dependencies.

---

## Component 3: Question Selection Strategy

### Maximum Fisher Information Criterion

After answering each question, we select the next question to maximize **Fisher Information** at the learner's current estimated ability:

$$\text{Next Question} = \arg\max_j I_j(\hat{\theta})$$

where $\hat{\theta}$ is the current ability estimate and $I_j(\theta)$ is the information function for question $j$.

### Algorithmic Steps

1. **Estimate current ability** using IRT 3PL model applied to all previous responses

2. **Compute Fisher Information** for all remaining questions at the current ability level

3. **Apply topic constraints** to ensure coverage:
   - Each topic must be represented proportionally
   - If a learner has mastered a topic (per BKT), reduce selection from that topic
   - If a learner is struggling (BKT < 0.3), increase selection from that topic

4. **Select question** with highest adjusted information

5. **Present question** to learner

### Adjusted Information Formula

To balance information maximization with topic coverage:

$$I^*_j(\theta) = I_j(\theta) \cdot w_j$$

where:

$$w_j = \begin{cases}
1.5 & \text{if } P(\text{Know}_j) < 0.3 \text{ (weak topic)} \\
1.0 & \text{if } 0.3 \leq P(\text{Know}_j) \leq 0.7 \text{ (moderate)} \\
0.6 & \text{if } P(\text{Know}_j) > 0.7 \text{ (mastered)}
\end{cases}$$

### Safety Constraints

To prevent unfair assessments:

- **Difficulty bounds:** Never select questions more than 2 ability units away from current $\hat{\theta}$
- **Minimum attempts per topic:** Ensure at least 3 questions per major topic before adaptive changes
- **Maximum difficulty:** Cap at $\theta + 1.5$ to avoid demotivation
- **Minimum difficulty:** Floor at $\theta - 1.5$ to ensure all questions are answerable

---

## Topic Mastery Calculation

### Definition

Topic mastery integrates IRT ability estimates with BKT knowledge probabilities:

$$M_{\text{topic}} = \left( P(\text{Know}) \right)^{0.4} \times \left( 1 - \frac{1}{1 + e^{2(\theta - b_{\text{avg}})}} \right)^{0.6}$$

This is a weighted geometric mean where:
- 40% weight comes from BKT skill knowledge probability
- 60% weight comes from IRT ability relative to average topic difficulty

### Interpretation

- **0.0 - 0.3:** Needs practice in this topic
- **0.3 - 0.6:** Developing competence; continue practice
- **0.6 - 0.85:** Proficient; ready for advanced material
- **0.85 - 1.0:** Mastered; focus on other areas

### Topic Category

The platform divides exams into topics such as:
- Exam P: Probability Distributions, Conditional Probability, Continuous Distributions, etc.
- Exam FM: Time Value of Money, Annuities, Bonds, etc.
- Exam FAM: Financial Statement Analysis, Risk Management, Life Contingencies, etc.

---

## Readiness Score Computation

### Definition

The Readiness Score estimates the learner's likelihood of passing the actual SOA exam:

$$R = 0.7 \times \bar{\theta} + 0.15 \times M_{\text{avg}} + 0.15 \times C$$

where:
- $\bar{\theta}$ = current ability estimate (IRT theta)
- $M_{\text{avg}}$ = average mastery across all topics
- $C$ = consistency metric (coefficient of variation in recent performance)

### Ability Calibration to Exam Score

The IRT ability scale is calibrated to exam percentile:

$$\text{Percentile} = 100 \times \Phi\left(\frac{\hat{\theta} + 0.5}{1.2}\right)$$

where $\Phi$ is the standard normal CDF and the offset/scaling are derived from historical SOA data.

Approximate mapping:
- $\theta = -2.0$ → Percentile ~5, Pass unlikely
- $\theta = -0.5$ → Percentile ~30, Below passing
- $\theta = 0.0$ → Percentile ~50, Near average
- $\theta = 0.5$ → Percentile ~66, Passing likely
- $\theta = 1.5$ → Percentile ~90, Strong performance

### Readiness Thresholds

- **R < 0.50:** Not ready; recommend more practice
- **0.50 ≤ R < 0.65:** Ready for exam but elevated risk; consider targeted review
- **0.65 ≤ R < 0.80:** Ready for exam; pass likely
- **R ≥ 0.80:** Well-prepared; ready to sit for exam

### Consistency Metric

$$C = 1 - \text{CV}_{\text{recent}}$$

where:

$$\text{CV}_{\text{recent}} = \frac{\text{StdDev}(\text{last 20 scores})}{\text{Mean}(\text{last 20 scores})}$$

CV close to 0 = consistent performance (good); CV close to 1 = highly variable (concerning).

---

## Comparison with SOA ADAPT System

### SOA ADAPT Approach

The official SOA ADAPT system uses:

1. **Item Response Theory (IRT)** for question difficulty and learner ability
2. **Fixed topic coverage** with adaptive sequencing
3. **Feedback on topics** but not detailed explanations
4. **Limited item bank** that repeats across sessions
5. **Linear progression** difficulty (generally increases over time)

### Our Platform Improvements

| Aspect | ADAPT | Our Platform |
|--------|-------|--------------|
| Skill Tracking | None | Bayesian Knowledge Tracing |
| Topic Mastery | Aggregate only | Individual skill estimates |
| Question Selection | Difficulty-based | Fisher Information maximization |
| Topic Coverage | Fixed | Adaptive weighting by mastery |
| Learning Feedback | Topic-level | Skill-level with explanations |
| Consistency Checking | No | Yes (readiness score) |
| Deferred Learning | Not modeled | Yes (via BKT learning rate) |

### Key Advantages

1. **More personalized:** BKT tracks learning at the skill level, not just topic level
2. **Better efficiency:** Fisher Information targeting minimizes questions needed
3. **Fairer assessment:** Consistency metric prevents flukes from determining readiness
4. **Better feedback:** Pinpoint weak skills rather than broad topic categories
5. **Replay value:** Item bank larger and questions sequenced uniquely per learner

---

## Algorithm Pseudocode

### Initialization

```
FUNCTION Initialize(learner_id):
    theta[learner_id] = 0.0  // Standard normal
    FOR each topic in exam:
        P_Know[topic] = L_0  // Prior knowledge
    question_history = []
    
FUNCTION SelectQuestion(learner_id, exam_id):
    // Estimate current ability
    theta_hat = EstimateAbility(question_history)
    
    // Get available questions
    available = GetUnusedQuestions(exam_id)
    
    // Compute Fisher Information for each
    best_info = -infinity
    best_question = null
    
    FOR each question in available:
        // Compute base information
        info = FisherInformation(question, theta_hat)
        
        // Apply topic mastery weighting
        topic_mastery = M[question.topic]
        weight = GetTopicWeight(topic_mastery)
        
        // Apply difficulty constraint
        IF ABS(question.difficulty - theta_hat) > 2.0:
            CONTINUE  // Skip out-of-range questions
        
        // Select highest weighted information
        IF info * weight > best_info:
            best_info = info * weight
            best_question = question
    
    RETURN best_question

FUNCTION UpdateBeliefs(learner_id, question_id, response_correct):
    q = GetQuestion(question_id)
    
    // Update IRT ability estimate
    theta[learner_id] = UpdateIRTAbility(
        theta[learner_id],
        q.parameters,
        response_correct
    )
    
    // Update BKT for each skill in question
    FOR each skill in q.skills:
        P_Know_old = P_Know[skill]
        
        // Likelihood of response
        p_correct = ComputeResponseProbability(
            P_Know_old,
            response_correct,
            q.guess,
            q.slip
        )
        
        // Bayesian update
        P_Know[skill] = UpdateBKT(
            P_Know_old,
            p_correct,
            response_correct
        )
        
        // Learning transition
        P_Know[skill] += T * (1 - P_Know[skill])
    
    // Update mastery for this topic
    M[q.topic] = ComputeTopicMastery(
        theta[learner_id],
        P_Know[all skills in topic],
        q.topic_avg_difficulty
    )
    
    // Compute readiness score
    readiness[learner_id] = ComputeReadinessScore(
        theta[learner_id],
        M,
        ConsistencyMetric(question_history)
    )
    
    // Log for history
    question_history.append({
        question_id: question_id,
        correct: response_correct,
        theta_before: theta_old,
        theta_after: theta[learner_id],
        mastery_after: M[q.topic]
    })

FUNCTION UpdateIRTAbility(theta_old, q_params, correct):
    // Likelihood function
    likelihood = IRTProbability(theta_old, q_params, correct)
    
    // Log-likelihood
    ll = LOG(likelihood) - LOG(1 - likelihood)
    
    // Gradient ascent step (simplified)
    eta = 0.5  // Learning rate
    theta_new = theta_old + eta * q_params.discrimination * ll
    
    // Constraint to reasonable range
    theta_new = CLAMP(theta_new, -3.0, 3.0)
    
    RETURN theta_new

FUNCTION UpdateBKT(P_Know_old, p_correct, correct):
    IF correct:
        numerator = p_correct * P_Know_old
        denominator = p_correct
    ELSE:
        numerator = (1 - p_correct) * P_Know_old
        denominator = (1 - p_correct)
    
    P_Know_new = numerator / denominator
    RETURN P_Know_new

FUNCTION ComputeResponseProbability(P_Know, correct, guess, slip):
    p_correct_if_know = 1 - slip
    p_correct_if_not_know = guess
    
    p_correct = P_Know * p_correct_if_know + 
                (1 - P_Know) * p_correct_if_not_know
    
    IF correct:
        RETURN p_correct
    ELSE:
        RETURN 1 - p_correct

FUNCTION ConsistencyMetric(history, window=20):
    IF LENGTH(history) < window:
        window = LENGTH(history)
    
    recent_scores = history[-(window):].correctness
    
    mean = MEAN(recent_scores)
    stdev = STDEV(recent_scores)
    
    IF mean == 0:
        RETURN 1.0  // All wrong = high inconsistency
    
    cv = stdev / mean
    RETURN 1 - MIN(cv, 1.0)  // Clamp at 1

FUNCTION ComputeReadinessScore(theta, M, consistency):
    M_avg = MEAN(M.values())
    
    readiness = 0.7 * NormalizeTheta(theta) + 
                0.15 * M_avg + 
                0.15 * consistency
    
    RETURN CLAMP(readiness, 0.0, 1.0)

FUNCTION NormalizeTheta(theta):
    // Map theta to 0-1 scale (0 = failing, 1 = excellent)
    normalized = Phi((theta + 0.5) / 1.2)  // CDF of standard normal
    RETURN normalized
```

### Main Testing Loop

```
PROCEDURE AdaptiveTestSession(learner_id, exam_id, max_questions):
    Initialize(learner_id)
    
    FOR i = 1 TO max_questions:
        question = SelectQuestion(learner_id, exam_id)
        
        IF question == null:
            BREAK  // No more available questions
        
        PresentQuestion(question)
        response_correct = GetResponse()
        
        UpdateBeliefs(learner_id, question, response_correct)
        
        // Optional: early stopping if readiness is clear
        IF i >= min_questions AND IsReadinessClear(readiness):
            BREAK
    
    // Final report
    DISPLAY RecommendationReport(
        readiness[learner_id],
        M,  // Topic mastery
        theta[learner_id]
    )
```

---

## Implementation Considerations

### Computational Efficiency

- **Pre-compute Fisher Information:** Calculate for all questions before session
- **Caching:** Store IRT parameters and BKT values in Redis
- **Parallel updates:** Update belief states asynchronously
- **Question pool size:** Maintain 500-1000 questions per exam for good coverage

### Numerical Stability

- **Logit transformation:** Work in log-odds space to avoid underflow
- **Constraint bounds:** Keep $\theta \in [-3, 3]$ and $P(\text{Know}) \in [0.01, 0.99]$
- **Regularization:** Use Bayesian priors to prevent overconfident estimates

### Validity Concerns

- **Item exposure:** Rotate questions across learners to maintain security
- **Cheating detection:** Flag unusual patterns (e.g., suddenly jumping from 20% to 95% success)
- **Test equating:** Ensure tests of equal difficulty across exam windows

---

## Validation Metrics

The platform tracks:

1. **Discrimination index:** Difference in success rate (high ability - low ability)
2. **Difficulty calibration:** Actual success rates vs. predicted by IRT
3. **Readiness prediction accuracy:** Correlation between readiness score and exam pass rate
4. **Test reliability:** Cronbach's alpha for internal consistency
5. **Learner satisfaction:** Surveys on difficulty appropriateness

---

This documentation provides the complete technical foundation for the adaptive testing system. Implementation details may be refined based on empirical data collection and learner feedback.
