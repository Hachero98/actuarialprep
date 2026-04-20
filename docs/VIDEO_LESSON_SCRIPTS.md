# Video Lesson Scripts

Complete scripts for video lessons designed for SOA exam preparation. Each script is written as a full presentation that an instructor would deliver.

---

## Lesson 1: Exam P — Understanding Conditional Probability

**Duration:** 15 minutes
**Objectives:**
- Understand the definition and notation of conditional probability
- Apply Bayes' Theorem to real-world problems
- Distinguish between independent and dependent events
- Build intuition through practical insurance examples

---

### Script

**[OPENING - 0:00-1:00]**

Hello, and welcome to this lesson on conditional probability. This is one of the most important concepts in probability and statistics, and it appears frequently on Exam P.

Let me start with a question: If I tell you that it's raining outside, does that change the probability that someone is holding an umbrella? Intuitively, yes—it does. This is the essence of conditional probability. We're updating our beliefs based on new information.

Today, we're going to break down conditional probability into simple, understandable pieces, and by the end of this lesson, you'll not only understand it mathematically, but you'll develop an intuition for when and how to use it.

**[DEFINITION AND NOTATION - 1:00-4:30]**

Let's start with the formal definition. The conditional probability of event A given that event B has occurred is defined as:

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

where $P(B) > 0$.

Let me break this down with a simple analogy. Imagine you're at an insurance company that handles both car accidents and home burglaries. You have 1,000 customers total. Of these:
- 100 customers filed a car accident claim
- 80 customers filed a home burglary claim
- 15 customers filed both types of claims

Now, if I ask you: "Given that a customer filed a home burglary claim, what's the probability they also filed a car accident claim?"

This is $P(\text{Car Accident | Home Burglary})$.

Using our formula:
- $P(\text{Car Accident AND Home Burglary}) = 15/1000 = 0.015$
- $P(\text{Home Burglary}) = 80/1000 = 0.08$

So: $P(\text{Car Accident | Home Burglary}) = \frac{0.015}{0.08} = 0.1875$

Notice what happened here. Without the condition, the probability of a car accident is 100/1000 = 0.10. But given that someone filed a home burglary claim, the probability jumps to 0.1875. The condition changed our probability—that's the power of conditioning.

**[INTUITION BUILDING - 4:30-7:00]**

Think of conditional probability this way: when we condition on B, we're essentially saying, "Forget about the entire sample space. Now, the only universe that matters is the world where B happened."

Let me draw this out. Imagine a rectangle representing all possible outcomes.

[VISUAL CUE: Draw a rectangle labeled "All Outcomes" with P(All) = 1]

Inside this rectangle, we have region A and region B that overlap slightly.

[VISUAL CUE: Draw two overlapping circles inside the rectangle, labeled A and B]

When we compute $P(A|B)$, we're saying: "Given that we're in region B, what proportion of B also belongs to A?"

It's like zooming in on region B and asking: out of all the area in B, how much is shared with A?

That's literally what the formula does: $\frac{P(A \cap B)}{P(B)}$ divides the overlapping area by the area of B.

**[INDEPENDENCE - 7:00-9:30]**

Now, here's an important concept: independence. Two events A and B are independent if knowing that B occurred doesn't change the probability of A. Mathematically:

$$P(A|B) = P(A)$$

Or equivalently:
$$P(A \cap B) = P(A) \times P(B)$$

Let me give you an example. Suppose you roll a die and flip a coin. Are the outcomes independent? Yes. Knowing that the die came up a 4 doesn't tell you anything about whether the coin is heads or tails. Their probabilities don't affect each other.

But consider this insurance example: Are "the customer is age 25" and "the customer files a claim within 5 years" independent? Probably not. Younger customers might have different claim patterns than older customers.

One quick way to check independence in our earlier example: Is $P(\text{Car Accident | Home Burglary}) = P(\text{Car Accident})$?

We found $P(\text{Car Accident | Home Burglary}) = 0.1875$ and $P(\text{Car Accident}) = 0.10$.

These are different, so the events are NOT independent.

**[BAYES' THEOREM - 9:30-12:00]**

Now, let's talk about Bayes' Theorem, which is one of the most powerful tools in probability. Bayes' Theorem allows us to reverse conditional probabilities.

Sometimes we know $P(B|A)$ but want to find $P(A|B)$. Bayes' Theorem is:

$$P(A|B) = \frac{P(B|A) \times P(A)}{P(B)}$$

Let me show you why this works. We know that:
$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

and also:
$$P(B|A) = \frac{P(A \cap B)}{P(A)}$$

From the second equation: $P(A \cap B) = P(B|A) \times P(A)$

Substituting into the first equation: $P(A|B) = \frac{P(B|A) \times P(A)}{P(B)}$

There's Bayes' Theorem!

Let me show you a practical example. Imagine a medical test for a rare disease.

The disease affects 0.1% of the population: $P(\text{Disease}) = 0.001$.

The test is quite good: if you have the disease, it correctly detects it 99% of the time: $P(\text{Positive Test | Disease}) = 0.99$.

But it's not perfect: if you don't have the disease, it gives a false positive 2% of the time: $P(\text{Positive Test | No Disease}) = 0.02$.

Now, here's the question: You take the test and it's positive. What's the probability you actually have the disease?

Many people would say 99%, but that's wrong! We need Bayes' Theorem.

First, let's find $P(\text{Positive Test})$ using the law of total probability:
$$P(\text{Positive}) = P(\text{Positive|Disease}) \times P(\text{Disease}) + P(\text{Positive|No Disease}) \times P(\text{No Disease})$$

$$= 0.99 \times 0.001 + 0.02 \times 0.999 = 0.00099 + 0.01998 = 0.02097$$

Now apply Bayes:
$$P(\text{Disease | Positive}) = \frac{P(\text{Positive|Disease}) \times P(\text{Disease})}{P(\text{Positive})}$$

$$= \frac{0.99 \times 0.001}{0.02097} = \frac{0.00099}{0.02097} \approx 0.047$$

Only about 4.7%! Even though the test is 99% accurate, a positive result means there's only a ~5% chance you have the disease. Why? Because the disease is so rare that false positives are more common than true positives.

**[WORKED EXAMPLE 1 - 12:00-14:00]**

Let's do another worked example together. An insurance company has three underwriters: Alice, Bob, and Carol. They write 40%, 35%, and 25% of all policies, respectively.

The claim rates for each underwriter are different:
- Alice's policies: 8% claim rate
- Bob's policies: 12% claim rate  
- Carol's policies: 6% claim rate

A random policy is selected, and a claim is filed. What's the probability that Alice wrote this policy?

This is asking for $P(\text{Alice | Claim})$.

**Step 1:** Find the total probability of a claim using the law of total probability:
$$P(\text{Claim}) = P(\text{Claim|Alice}) \times P(\text{Alice}) + P(\text{Claim|Bob}) \times P(\text{Bob}) + P(\text{Claim|Carol}) \times P(\text{Carol})$$

$$= 0.08 \times 0.40 + 0.12 \times 0.35 + 0.06 \times 0.25$$

$$= 0.032 + 0.042 + 0.015 = 0.089$$

**Step 2:** Apply Bayes' Theorem:
$$P(\text{Alice | Claim}) = \frac{P(\text{Claim|Alice}) \times P(\text{Alice})}{P(\text{Claim})}$$

$$= \frac{0.08 \times 0.40}{0.089} = \frac{0.032}{0.089} \approx 0.360$$

So there's about a 36% chance Alice wrote the policy.

**[WORKED EXAMPLE 2 - 14:00-15:00]**

Quick second example. A customer visits an insurance website. The probability they download a brochure is 30%. If they download, the probability they call for a quote is 60%. If they don't download, the probability they call is 5%.

What's the probability someone who called for a quote had downloaded the brochure?

Let D = downloaded brochure, C = called for quote.

We want $P(D|C)$.

$P(C) = P(C|D) \times P(D) + P(C|D^c) \times P(D^c)$
$= 0.60 \times 0.30 + 0.05 \times 0.70 = 0.18 + 0.035 = 0.215$

$P(D|C) = \frac{0.60 \times 0.30}{0.215} = \frac{0.18}{0.215} \approx 0.837$

So about 83.7% of people who called had downloaded the brochure first.

**[COMMON MISTAKES - 15:00-15:45]**

Before we wrap up, let me highlight the most common mistakes students make with conditional probability:

**Mistake 1: Confusing $P(A|B)$ with $P(B|A)$.** These are NOT the same! In our disease example, $P(\text{Positive|Disease}) = 99\%$ but $P(\text{Disease|Positive}) \approx 5\%$. The order matters tremendously.

**Mistake 2: Forgetting to divide by $P(B)$.** A lot of students compute $P(A \cap B)$ and call it done. But conditional probability requires that division by $P(B)$.

**Mistake 3: Assuming events are independent when they're not.** Just because something isn't explicitly stated to be dependent doesn't mean it is independent. Think carefully about the context.

**Mistake 4: Misapplying the law of total probability.** Make sure your conditions partition the sample space completely and don't overlap.

**[SUMMARY CHECKPOINT - 15:45-16:00]**

Let me give you three things to remember:

1. **Conditional probability** answers: "Given X happened, what's the probability Y happens?" The formula is $P(A|B) = \frac{P(A \cap B)}{P(B)}$.

2. **Bayes' Theorem** lets you reverse conditional probabilities: $P(A|B) = \frac{P(B|A) \times P(A)}{P(B)}$. Use it when you know P(B|A) but need P(A|B).

3. **The law of total probability** is your friend: decompose complex probabilities into simpler conditional pieces.

These three ideas form the foundation of everything you'll see on Exam P. Practice with as many problems as you can, and you'll develop an intuition for when and how to apply these concepts.

Thank you for watching, and good luck on your exam!

---

---

## Lesson 2: Exam FM — Annuities: Present and Future Value

**Duration:** 20 minutes
**Objectives:**
- Understand the distinction between ordinary annuities and annuities-due
- Calculate present and future values of annuities
- Apply annuity concepts to real-world financial scenarios
- Recognize and solve variations (annuities-certain, deferred annuities, perpetuities)

---

### Script

**[OPENING - 0:00-1:30]**

Welcome to our lesson on annuities. This is one of the core topics on Exam FM, and understanding annuities deeply will help you solve a huge variety of problems.

So what is an annuity? At its heart, an annuity is simply a series of equal payments made at regular intervals. Think about retirement income, mortgage payments, or lease payments. These are all annuities.

But here's the key: the timing of those payments matters enormously. A $1 payment you receive today is worth more than a $1 payment you receive a year from now—because you can invest today's money. That's the principle behind calculating present and future values of annuities.

By the end of this lesson, you'll understand how to value any sequence of equal cash flows, and you'll see how this applies to real financial products.

**[ANNUITY BASICS - 1:30-4:30]**

Let's establish some notation and terminology. An annuity consists of:
- A series of equal payments
- Made at regular intervals
- For a specified period

Let me define the key symbols we'll use:
- $i$ = interest rate per period (e.g., annual interest rate)
- $n$ = number of periods
- $PMT$ = the payment amount (constant)
- $PV$ = present value
- $FV$ = future value

There are two fundamental types of annuities:

**Ordinary Annuity (Annuity-Immediate):** Payments occur at the END of each period.

Think of it this way: You take out a loan today and start making payments at the end of this month, next month, and so on.

**Annuity-Due:** Payments occur at the BEGINNING of each period.

Think of it this way: You rent an apartment and pay at the start of each month.

Let me visualize this for you.

[VISUAL CUE: Timeline for ordinary annuity]
```
Time:    0        1        2        3        4
         |--------|--------|--------|--------|
Payments:        PMT      PMT      PMT      PMT
```

[VISUAL CUE: Timeline for annuity-due]
```
Time:    0        1        2        3        4
         |--------|--------|--------|--------|
Payments: PMT      PMT      PMT      PMT
```

See the difference? For an ordinary annuity, the first payment is at time 1. For an annuity-due, the first payment is at time 0.

**[PRESENT VALUE OF ORDINARY ANNUITY - 4:30-8:30]**

Let's start with the present value of an ordinary annuity. We want to know: if I'm going to receive n equal payments of PMT at the end of each period, and the interest rate is i, what is this stream worth in today's dollars?

Let's think about this intuitively. Each payment gets discounted back to today.

- Payment 1 (made at time 1): Discounted for 1 period: $\frac{PMT}{(1+i)^1}$
- Payment 2 (made at time 2): Discounted for 2 periods: $\frac{PMT}{(1+i)^2}$
- Payment 3 (made at time 3): Discounted for 3 periods: $\frac{PMT}{(1+i)^3}$
- ... and so on ...
- Payment n (made at time n): Discounted for n periods: $\frac{PMT}{(1+i)^n}$

The present value is the sum of all these:
$$PV = PMT \left[ \frac{1}{(1+i)^1} + \frac{1}{(1+i)^2} + \cdots + \frac{1}{(1+i)^n} \right]$$

This is a geometric series, and there's a closed-form formula for it:
$$PV = PMT \times \frac{1 - (1+i)^{-n}}{i}$$

We write this as:
$$PV = PMT \times a_{\overline{n}|i}$$

where $a_{\overline{n}|i} = \frac{1 - (1+i)^{-n}}{i}$ is called the "present value annuity factor" or "discount factor."

Let me give you a concrete example. Suppose you'll receive $100 at the end of each year for 5 years, and the interest rate is 6%.

$$PV = 100 \times a_{\overline{5}|6\%}$$

$$a_{\overline{5}|6\%} = \frac{1 - (1.06)^{-5}}{0.06} = \frac{1 - 0.7473}{0.06} = \frac{0.2527}{0.06} = 4.2124$$

$$PV = 100 \times 4.2124 = 421.24$$

So a stream of $100 annual payments for 5 years is worth $421.24 today, assuming 6% interest.

**[FUTURE VALUE OF ORDINARY ANNUITY - 8:30-11:30]**

Now let's flip the question: instead of asking what future payments are worth today, let's ask what today's payments will grow to in the future.

Suppose you invest $100 at the end of each year for 5 years at 6% interest. What's the total value at the end of year 5?

Let's think about each payment:
- The payment at the end of year 1 will grow for 4 years: $PMT \times (1+i)^{4}$
- The payment at the end of year 2 will grow for 3 years: $PMT \times (1+i)^{3}$
- The payment at the end of year 3 will grow for 2 years: $PMT \times (1+i)^{2}$
- The payment at the end of year 4 will grow for 1 year: $PMT \times (1+i)^{1}$
- The payment at the end of year 5 grows for 0 years: $PMT \times (1+i)^{0} = PMT$

[VISUAL CUE: Timeline showing growth of each payment]

Summing these up:
$$FV = PMT \left[ (1+i)^{n-1} + (1+i)^{n-2} + \cdots + (1+i)^1 + 1 \right]$$

Again, using the geometric series formula:
$$FV = PMT \times \frac{(1+i)^n - 1}{i}$$

We write this as:
$$FV = PMT \times s_{\overline{n}|i}$$

where $s_{\overline{n}|i} = \frac{(1+i)^n - 1}{i}$ is the "future value annuity factor" or "accumulation factor."

For our example:
$$FV = 100 \times s_{\overline{5}|6\%}$$

$$s_{\overline{5}|6\%} = \frac{(1.06)^5 - 1}{0.06} = \frac{1.3382 - 1}{0.06} = \frac{0.3382}{0.06} = 5.6371$$

$$FV = 100 \times 5.6371 = 563.71$$

So your $100 annual investments will grow to $563.71 after 5 years.

Notice something interesting: The present value was $421.24 and the future value is $563.71. If we grow $421.24 at 6% for 5 years:
$$421.24 \times (1.06)^5 = 421.24 \times 1.3382 = 563.71$$

Perfect! This demonstrates the fundamental relationship: the future value of the annuity equals the future value of its present value. That's just common sense applying the time value of money.

**[ANNUITIES-DUE - 11:30-14:30]**

Now, remember I mentioned annuities-due? Where payments happen at the beginning of each period?

The key insight is this: an annuity-due is just an ordinary annuity where each payment is made one period earlier. So each payment has one extra period to grow (for future value) or one fewer period to discount (for present value).

For present value of an annuity-due:
$$PV_{due} = PMT \times \ddot{a}_{\overline{n}|i}$$

where $\ddot{a}_{\overline{n}|i} = a_{\overline{n}|i} \times (1+i)$

The relationship is simple: **multiply the ordinary annuity factor by $(1+i)$**.

For future value of an annuity-due:
$$FV_{due} = PMT \times \ddot{s}_{\overline{n}|i}$$

where $\ddot{s}_{\overline{n}|i} = s_{\overline{n}|i} \times (1+i)$

Again, **multiply by $(1+i)$**.

Let's use our previous example. If you pay $100 at the BEGINNING of each year for 5 years:

Present value:
$$PV_{due} = 100 \times 4.2124 \times 1.06 = 100 \times 4.4650 = 446.50$$

This is higher than the ordinary annuity ($421.24) because you're receiving the money earlier.

Future value:
$$FV_{due} = 100 \times 5.6371 \times 1.06 = 100 \times 5.9753 = 597.53$$

Again higher than the ordinary annuity ($563.71) because each payment has more time to grow.

**[WORKED EXAMPLE 1 - 14:30-17:00]**

Let's do a practical example together. A person takes out a 30-year mortgage for $300,000 at an annual interest rate of 5%. What is the monthly payment?

**Step 1:** Convert to monthly terms.
- Monthly interest rate: $i = 5\% / 12 = 0.4167\%$ per month
- Number of months: $n = 30 \times 12 = 360$
- Loan amount (present value): $PV = 300,000$

**Step 2:** The mortgage is paid with monthly payments at the end of each month, so it's an ordinary annuity.

$$PV = PMT \times a_{\overline{n}|i}$$

$$300,000 = PMT \times a_{\overline{360}|0.4167\%}$$

**Step 3:** Calculate the annuity factor.
$$a_{\overline{360}|0.004167} = \frac{1 - (1.004167)^{-360}}{0.004167}$$

Let's compute $(1.004167)^{-360}$:
$$(1.004167)^{360} = (1 + 0.05/12)^{360} \approx e^{0.05 \times 30} = e^{1.5} \approx 4.4817$$

So $(1.004167)^{-360} \approx 1/4.4817 = 0.2233$

$$a_{\overline{360}|0.004167} = \frac{1 - 0.2233}{0.004167} = \frac{0.7767}{0.004167} \approx 186.28$$

**Step 4:** Solve for PMT.
$$PMT = \frac{300,000}{186.28} \approx 1,610$$

So the monthly payment is approximately $1,610.

This makes intuitive sense: you're borrowing $300,000 and paying it back over 360 months, with interest. A simple (wrong) estimate would be $300,000 / 360 = $833 per month without interest. With interest, it's higher.

**[WORKED EXAMPLE 2 - 17:00-19:00]**

Here's another scenario. A retiree has $500,000 in savings and wants to withdraw equal amounts every quarter for the next 20 years. Interest rates are 4% annually (1% quarterly). What is the maximum quarterly withdrawal?

This is asking: given that the present value is $500,000, what is the quarterly payment?

$$PV = PMT \times a_{\overline{n}|i}$$

$$500,000 = PMT \times a_{\overline{80}|1\%}$$

Note: 20 years × 4 quarters/year = 80 quarters.

$$a_{\overline{80}|1\%} = \frac{1 - (1.01)^{-80}}{0.01}$$

$(1.01)^{80} \approx e^{0.01 \times 80} = e^{0.8} \approx 2.2255$

So $(1.01)^{-80} \approx 0.4492$

$$a_{\overline{80}|1\%} = \frac{1 - 0.4492}{0.01} = \frac{0.5508}{0.01} = 55.08$$

$$PMT = \frac{500,000}{55.08} \approx 9,076$$

So the retiree can withdraw about $9,076 each quarter (or roughly $36,304 per year).

**[COMMON MISTAKES - 19:00-19:45]**

Before we wrap up, let me highlight common mistakes:

**Mistake 1: Confusing ordinary annuities with annuities-due.** Read the problem carefully. Does the problem say payments are made "at the beginning" or "at the end" of periods? Or "in advance"? These indicate annuities-due.

**Mistake 2: Using annual interest rates for non-annual periods.** If you have monthly payments, use monthly interest rates. If you have quarterly payments, convert to quarterly rates. Mismatch here will give wildly incorrect answers.

**Mistake 3: Miscounting periods.** If you have payments every month for 3 years, that's 36 periods, not 12.

**Mistake 4: Forgetting that the present value of an annuity at time 0 equals the future value discounted back to time 0.** These two methods should give the same answer.

**[SUMMARY CHECKPOINT - 19:45-20:00]**

Here are the key takeaways:

1. An **ordinary annuity** has payments at the END of periods. Use $a_{\overline{n}|i}$ for present value and $s_{\overline{n}|i}$ for future value.

2. An **annuity-due** has payments at the BEGINNING of periods. Multiply the ordinary annuity factors by $(1+i)$.

3. Always **match your interest rate period to your payment period**. Monthly payments require monthly interest rates.

4. The **relationship between present and future value** is: FV = PV × $(1+i)^n$

These concepts form the foundation of bond pricing, mortgage calculations, and pension accounting. Master these, and you'll excel on Exam FM.

Good luck with your studies!

---

---

## Lesson 3: Exam FAM — Survival Models and Life Tables

**Duration:** 15 minutes
**Objectives:**
- Understand the structure and interpretation of life tables
- Distinguish between age-based and duration-based calculations
- Apply survival models to life contingency calculations
- Calculate life expectancy and force of mortality from life tables

---

### Script

**[OPENING - 0:00-1:15]**

Welcome to our lesson on survival models and life tables. This is one of the foundational topics in actuarial science and appears prominently on Exam FAM.

Life tables are remarkable because they give us a probabilistic picture of human mortality. They answer questions like: "Of 100,000 babies born today, how many will survive to age 65?" and "What is the life expectancy of a 50-year-old?"

These aren't just academic questions—insurance companies use life tables every single day to price products, manage risk, and calculate reserves. By the end of this lesson, you'll understand how to read and work with life tables, and you'll appreciate why they're so crucial to actuarial work.

**[LIFE TABLE STRUCTURE - 1:15-4:30]**

Let me show you what a life table looks like. Here's a simplified example:

| Age (x) | $l_x$ | $d_x$ | $p_x$ | $q_x$ |
|---------|-------|-------|-------|-------|
| 0       | 100,000 | 500 | 0.9950 | 0.0050 |
| 1       | 99,500 | 100 | 0.9990 | 0.0010 |
| 50      | 98,200 | 200 | 0.9980 | 0.0020 |
| 65      | 97,500 | 500 | 0.9949 | 0.0051 |
| 80      | 95,000 | 2,000 | 0.9789 | 0.0211 |

[VISUAL CUE: Display table clearly and explain each column]

Let me explain what each column represents:

**Column 1: Age (x).** This is straightforward—it's the age of the cohort being tracked.

**Column 2: $l_x$ (number of lives).** This is the number of people alive at age x, starting from a cohort of, say, 100,000 newborns. Notice how $l_x$ decreases as x increases—people are dying.

**Column 3: $d_x$ (number of deaths).** This is the number of people who die between age x and age x+1. Notice that $d_x = l_x - l_{x+1}$.

**Column 4: $p_x$ (probability of survival).** This is the probability that someone age x survives to age x+1. It's calculated as:
$$p_x = \frac{l_{x+1}}{l_x}$$

For example, at age 0: $p_0 = \frac{99,500}{100,000} = 0.9950$. This means a newborn has a 99.5% chance of surviving to age 1.

**Column 5: $q_x$ (probability of death).** This is the probability that someone age x dies before reaching age x+1. It's calculated as:
$$q_x = 1 - p_x = \frac{d_x}{l_x}$$

For example: $q_0 = 1 - 0.9950 = 0.0050$. A newborn has a 0.5% chance of dying within the year.

**[RELATIONSHIPS AND INTUITION - 4:30-7:30]**

There are some powerful relationships in life tables. Let me show you:

**Relationship 1: Compounded Survival**

The probability of surviving from age x to age x+n is:
$$_np_x = p_x \times p_{x+1} \times p_{x+2} \times \cdots \times p_{x+n-1} = \frac{l_{x+n}}{l_x}$$

Think about this intuitively: to survive from age 50 to 65, you have to survive from 50 to 51, AND 51 to 52, AND ... AND 64 to 65. That's a chain of independent events, so we multiply probabilities.

For example, the probability a 50-year-old survives to 65 (15 years) is:
$$_{15}p_{50} = \frac{l_{65}}{l_{50}} = \frac{97,500}{98,200} = 0.9929$$

About 99.3% of 50-year-olds reach 65.

**Relationship 2: Force of Mortality**

The "force of mortality" or "hazard rate," denoted $\mu_x$, describes the instantaneous death rate. In the continuous model:
$$\mu_x = -\frac{d}{dx} \ln(l_x)$$

And the survival probability can be expressed as:
$$_tp_x = \exp\left(-\int_0^t \mu_{x+s} ds\right)$$

For discrete life tables (which are step-wise), we often approximate:
$$\mu_x \approx -\ln(p_x)$$

If $p_x = 0.9950$, then $\mu_x \approx -\ln(0.9950) \approx 0.005012$.

The force of mortality typically increases with age—mortality risk is higher for elderly people.

**[CALCULATING LIFE EXPECTANCY - 7:30-10:15]**

One of the most practically important calculations from a life table is life expectancy. There are two types:

**Type 1: Life Expectancy at Birth ($e_0$).**

This is the average number of years a newborn is expected to live.

$$e_0 = \sum_{x=0}^{\infty} \, _xp_0 = \sum_{x=0}^{\infty} \frac{l_x}{l_0}$$

Actually, a better formula (accounting for the timing of deaths within each year) is:
$$e_x = \frac{1}{l_x} \sum_{k=0}^{\infty} l_{x+k} \approx \frac{1}{l_x} \sum_{k=1}^{\infty} l_{x+k}$$

Or using continuous approximation:
$$e_x = \int_0^{\infty} \, _tp_x \, dt$$

**Type 2: Life Expectancy at Age x ($e_x$).**

This is the average number of additional years a person age x is expected to live.

$$e_x = \sum_{k=0}^{\infty} \, _kp_x$$

Let me compute an example. Using our life table:
$$e_{50} = \, _0p_{50} + \, _1p_{50} + \, _2p_{50} + \cdots$$

The first term $\, _0p_{50} = 1$ (they're alive at age 50 with probability 1).

The second term $\, _1p_{50} = \frac{l_{51}}{l_{50}}$ (probability of surviving to 51).

And so on.

If we sum these up (which in practice requires summing many terms), we might get something like $e_{50} = 32.4$ years. This means a 50-year-old is expected to live another 32.4 years on average, reaching age 82.4.

[VISUAL CUE: Timeline showing life expectancy concept]

**[WORKED EXAMPLE 1 - 10:15-12:30]**

Let's work through a practical example together.

Suppose an insurance company provides a 15-year term life insurance policy for a 50-year-old. They want to estimate how many of their 10,000 policyholders are expected to file claims during the 15-year period.

Using the life table:
- $l_{50} = 98,200$
- $l_{65} = 97,500$
- Number expected to die between 50 and 65: $98,200 - 97,500 = 700$ (from the original cohort)

But we need the expected number out of 10,000 policyholders:
$$\text{Expected deaths} = 10,000 \times \frac{700}{98,200} = 10,000 \times 0.00713 = 71.3$$

So they expect about 71 of their 10,000 policyholders to pass away during the 15-year term, resulting in 71 claim payments.

This is key information for pricing the insurance premium.

**[WORKED EXAMPLE 2 - 12:30-14:30]**

Here's another scenario. An insurance company is pricing an immediate life annuity for a 65-year-old who will receive $10,000 per year as long as they live. The company's discount rate is 4% annually.

The present value of this annuity is:
$$PV = 10,000 \times \ddot{a}_{65}$$

where $\ddot{a}_{65} = \sum_{k=0}^{\infty} \, _kp_{65} \times (1.04)^{-k}$

Let me compute this step-by-step:
- Year 0 (age 65): Probability 1 of being alive, discount factor $(1.04)^0 = 1$. Contribution: $1 \times 1 = 1$.
- Year 1 (age 66): Probability $p_{65} = 0.9949$, discount factor $(1.04)^{-1} = 0.9615$. Contribution: $0.9949 \times 0.9615 \approx 0.9562$.
- Year 2 (age 67): Probability $\, _2p_{65} = p_{65} \times p_{66}$, discount factor $(1.04)^{-2} = 0.9246$. Contribution: roughly $0.9908 \times 0.9246 \approx 0.9165$.

We'd continue this calculation for many decades, summing contributions that get progressively smaller (both because mortality increases and discount factors shrink).

A typical result might be $\ddot{a}_{65} \approx 15.5$ for a healthy population.

So the present value is:
$$PV = 10,000 \times 15.5 = 155,000$$

The insurance company would price the annuity at roughly $155,000. For every $155,000 paid, they expect to pay out $10,000 per year, and the math works out.

**[COMMON MISTAKES - 14:30-15:00]**

Let me point out common mistakes:

**Mistake 1: Confusing $p_x$ (survival probability) with $q_x$ (death probability).** They sum to 1. If 99% survive, 1% die.

**Mistake 2: Miscalculating multi-year survival probabilities.** Remember: $\, _np_x = \frac{l_{x+n}}{l_x}$. Don't just use the one-year rates.

**Mistake 3: Forgetting to discount when calculating present values.** Life tables give you probabilities, but when pricing insurance products, you also need to discount for time value of money.

**Mistake 4: Assuming life tables are constant.** Real life tables vary by population, gender, smoking status, and other factors. Always check which table applies to your problem.

**[SUMMARY CHECKPOINT - 15:00-15:00]**

Key takeaways:

1. **Life tables** organize mortality data. The key columns are $l_x$, $d_x$, $p_x$, and $q_x$.

2. **Multi-year survival:** Use $\, _np_x = \frac{l_{x+n}}{l_x}$ to find the probability of surviving from age x to age x+n.

3. **Life expectancy:** The expected additional lifespan is $e_x = \sum_{k=0}^{\infty} \, _kp_x$.

4. **In practice,** actuaries combine life tables with interest rates to price products and calculate reserves. Always apply both mortality and discounting.

This is foundational material—master it, and you'll be well-prepared for the life contingency topics on Exam FAM.

Thank you for watching, and best of luck on your exam!

---

---

This completes three full video lesson scripts designed for SOA exam preparation. Each script is detailed, includes worked examples, and addresses common misconceptions.
