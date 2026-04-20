import random
import math
from typing import Dict, List
from datetime import datetime


class ExamFMGenerator:
    """FM Exam Question Generator - Generates randomized questions across all FM topics."""

    def __init__(self, seed=None):
        if seed:
            random.seed(seed)

    # ===== TOPIC 1: TIME VALUE OF MONEY (15+ methods) =====

    def simple_interest(self) -> Dict:
        """Generate simple interest question: A = P(1 + rt)"""
        principal = round(random.uniform(1000, 50000), 2)
        rate = round(random.uniform(0.02, 0.12), 4)
        time = random.randint(1, 10)

        correct_amount = round(principal * (1 + rate * time), 2)

        q_id = f"tv_simple_int_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${correct_amount:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(principal * (1 + rate)**time, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(principal + rate * time, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(principal * (1 + rate * time / 2), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(principal * rate * time, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Simple Interest",
            "difficulty": 1,
            "question_text": f"An investment of ${principal:,.2f} earns simple interest at a rate of {rate*100:.2f}% per year. What is the accumulated value after {time} years?",
            "choices": choices,
            "solution": f"A = P(1 + rt) = {principal} × (1 + {rate} × {time}) = ${correct_amount:,.2f}",
            "explanation": "Simple interest grows linearly: A = P(1 + rt). Common mistake: using compound interest formula instead."
        }

    def compound_interest_fv(self) -> Dict:
        """Generate compound interest FV question: FV = PV(1 + i)^n"""
        pv = round(random.uniform(1000, 100000), 2)
        annual_rate = round(random.uniform(0.01, 0.10), 4)
        compounds_per_year = random.choice([1, 2, 4, 12])
        years = random.randint(1, 20)

        periods = years * compounds_per_year
        periodic_rate = annual_rate / compounds_per_year
        fv = round(pv * (1 + periodic_rate) ** periods, 2)

        q_id = f"tv_compound_fv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${fv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(pv * (1 + annual_rate)**years, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(pv * (1 + periodic_rate*periods), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(pv + periodic_rate*periods*pv, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv * (1 + annual_rate/compounds_per_year)**years, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Compound Interest - Future Value",
            "difficulty": 1,
            "question_text": f"${pv:,.2f} is invested for {years} years at {annual_rate*100:.2f}% annual interest, compounded {compounds_per_year} times per year. What is the future value?",
            "choices": choices,
            "solution": f"FV = PV(1 + i)^n = {pv} × (1 + {periodic_rate:.6f})^{periods} = ${fv:,.2f}",
            "explanation": f"With compounding {compounds_per_year} times/year: periodic rate = {annual_rate*100:.2f}% / {compounds_per_year} = {periodic_rate*100:.4f}%, n = {years} × {compounds_per_year} = {periods} periods."
        }

    def compound_interest_pv(self) -> Dict:
        """Generate compound interest PV question: PV = FV / (1 + i)^n"""
        fv = round(random.uniform(5000, 100000), 2)
        annual_rate = round(random.uniform(0.01, 0.10), 4)
        compounds_per_year = random.choice([1, 2, 4, 12])
        years = random.randint(1, 20)

        periods = years * compounds_per_year
        periodic_rate = annual_rate / compounds_per_year
        pv = round(fv / (1 + periodic_rate) ** periods, 2)

        q_id = f"tv_compound_pv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(fv / (1 + annual_rate)**years, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(fv * periodic_rate * periods, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(fv - periodic_rate*periods*fv, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(fv / (1 + annual_rate), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Compound Interest - Present Value",
            "difficulty": 1,
            "question_text": f"What present value will grow to ${fv:,.2f} in {years} years at {annual_rate*100:.2f}% annual interest, compounded {compounds_per_year} times per year?",
            "choices": choices,
            "solution": f"PV = FV / (1 + i)^n = {fv} / (1 + {periodic_rate:.6f})^{periods} = ${pv:,.2f}",
            "explanation": f"Discount using the compound interest formula. Periodic rate = {periodic_rate*100:.4f}%, total periods = {periods}."
        }

    def nominal_to_effective_rate(self) -> Dict:
        """Convert nominal to effective annual rate: i = (1 + j/m)^m - 1"""
        nominal_rate = round(random.uniform(0.01, 0.15), 4)
        compounds_per_year = random.choice([2, 4, 12])

        effective_rate = round((1 + nominal_rate / compounds_per_year) ** compounds_per_year - 1, 6)

        q_id = f"tv_nom_to_eff_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{effective_rate*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{nominal_rate*100:.2f}%", "is_correct": False},
            {"label": "C", "text": f"{round((1 + nominal_rate/compounds_per_year)*compounds_per_year - 1, 6)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round(nominal_rate * compounds_per_year, 6)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round(nominal_rate / compounds_per_year * 100, 4)}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Nominal to Effective Rate",
            "difficulty": 2,
            "question_text": f"Find the effective annual rate equivalent to {nominal_rate*100:.2f}% nominal annual interest compounded {compounds_per_year} times per year.",
            "choices": choices,
            "solution": f"i = (1 + j/m)^m - 1 = (1 + {nominal_rate:.4f}/{compounds_per_year})^{compounds_per_year} - 1 = {effective_rate*100:.4f}%",
            "explanation": f"The effective rate accounts for compounding. (1 + {nominal_rate/compounds_per_year:.6f})^{compounds_per_year} = {1 + effective_rate:.6f}"
        }

    def effective_to_nominal_rate(self) -> Dict:
        """Convert effective to nominal rate: j = m[(1 + i)^(1/m) - 1]"""
        effective_rate = round(random.uniform(0.01, 0.15), 6)
        compounds_per_year = random.choice([2, 4, 12])

        nominal_rate = round(compounds_per_year * ((1 + effective_rate) ** (1 / compounds_per_year) - 1), 6)

        q_id = f"tv_eff_to_nom_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{nominal_rate*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{effective_rate*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{round((1 + effective_rate)**(1/compounds_per_year) - 1, 6)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round(effective_rate / compounds_per_year, 6)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round((1 + effective_rate) * compounds_per_year - 1, 6)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Effective to Nominal Rate",
            "difficulty": 2,
            "question_text": f"Find the nominal annual interest rate compounded {compounds_per_year} times per year equivalent to {effective_rate*100:.4f}% effective annual rate.",
            "choices": choices,
            "solution": f"j = m[(1 + i)^(1/m) - 1] = {compounds_per_year}[(1 + {effective_rate:.6f})^(1/{compounds_per_year}) - 1] = {nominal_rate*100:.4f}%",
            "explanation": f"Backing out the nominal rate from effective. (1 + {effective_rate:.6f})^(1/{compounds_per_year}) = {(1 + effective_rate)**(1/compounds_per_year):.6f}"
        }

    def continuous_compounding(self) -> Dict:
        """Continuous compounding: FV = PV * e^(δt)"""
        pv = round(random.uniform(1000, 50000), 2)
        force_of_interest = round(random.uniform(0.01, 0.12), 4)
        years = random.randint(1, 15)

        fv = round(pv * math.exp(force_of_interest * years), 2)

        q_id = f"tv_continuous_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${fv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(pv * (1 + force_of_interest)**years, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(pv + force_of_interest * years, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(pv * math.exp(force_of_interest + years), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv * math.exp(force_of_interest / years), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Continuous Compounding",
            "difficulty": 2,
            "question_text": f"${pv:,.2f} is invested for {years} years at a force of interest of {force_of_interest*100:.2f}%. Find the accumulated value using continuous compounding.",
            "choices": choices,
            "solution": f"A(t) = Pe^(δt) = {pv} × e^({force_of_interest}×{years}) = {pv} × e^{force_of_interest*years:.4f} = ${fv:,.2f}",
            "explanation": f"Continuous compounding uses e^(δt) where δ is the force of interest. e^{force_of_interest*years:.4f} ≈ {math.exp(force_of_interest*years):.6f}"
        }

    def discount_rate_vs_interest_rate(self) -> Dict:
        """Relationship: d = i/(1+i), or i = d/(1-d)"""
        interest_rate = round(random.uniform(0.01, 0.20), 4)
        discount_rate = round(interest_rate / (1 + interest_rate), 4)

        q_id = f"tv_discount_vs_int_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{discount_rate*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{interest_rate*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{round(interest_rate / 2, 4)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round(interest_rate * (1 + interest_rate), 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round((1 - interest_rate) / interest_rate, 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Discount Rate vs Interest Rate",
            "difficulty": 2,
            "question_text": f"What is the annual discount rate equivalent to an annual interest rate of {interest_rate*100:.4f}%?",
            "choices": choices,
            "solution": f"d = i/(1+i) = {interest_rate:.4f} / (1 + {interest_rate:.4f}) = {discount_rate:.4f} = {discount_rate*100:.4f}%",
            "explanation": f"Discount rate d is related to interest rate i by: d = i/(1+i). Also: i = d/(1-d). These represent equivalent rates of return."
        }

    def force_of_interest(self) -> Dict:
        """Force of interest: δ(t) or constant δ. a(t) = e^(∫δ dt)"""
        force = round(random.uniform(0.02, 0.15), 4)
        years = random.randint(1, 20)
        pv = round(random.uniform(1000, 50000), 2)

        fv = round(pv * math.exp(force * years), 2)

        q_id = f"tv_force_int_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${fv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(pv * (1 + force)**years, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(pv * (1 + force*years), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(pv * math.exp(force + years), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv + force * years, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Force of Interest",
            "difficulty": 2,
            "question_text": f"${pv:,.2f} accumulates at a constant force of interest δ = {force*100:.2f}% for {years} years. What is the accumulated value?",
            "choices": choices,
            "solution": f"a(t) = e^(δt) = e^({force}×{years}) ≈ {math.exp(force*years):.6f}, so A = {pv} × {math.exp(force*years):.6f} = ${fv:,.2f}",
            "explanation": f"The accumulation function with constant force of interest is a(t) = e^(δt). This is equivalent to continuous compounding."
        }

    def equivalent_rates(self) -> Dict:
        """Two rates are equivalent if they produce same FV from same PV over same period"""
        rate1 = round(random.uniform(0.01, 0.15), 4)
        compounds1 = random.choice([1, 2, 4, 12])
        years = random.randint(2, 10)

        # Find equivalent rate with different compounding
        compounds2 = random.choice([c for c in [1, 2, 4, 12] if c != compounds1])

        # Effective rate must be same
        effective = (1 + rate1 / compounds1) ** compounds1 - 1
        rate2 = round(compounds2 * ((1 + effective) ** (1 / compounds2) - 1), 4)

        q_id = f"tv_equiv_rates_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{rate2*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{rate1*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{round(rate1 * compounds2 / compounds1, 4)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round((1 + rate1)**compounds2 - 1, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round(rate1 / (compounds2/compounds1), 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Equivalent Rates",
            "difficulty": 2,
            "question_text": f"Find the nominal rate compounded {compounds2} times per year equivalent to {rate1*100:.4f}% compounded {compounds1} times per year.",
            "choices": choices,
            "solution": f"Both must have same effective rate. i_eff = (1 + {rate1/compounds1:.6f})^{compounds1} - 1 = {effective:.6f}. Then j₂ = {compounds2}[(1.{effective:.6f})^(1/{compounds2}) - 1] = {rate2*100:.4f}%",
            "explanation": f"Equivalent rates produce the same effective annual rate. Both rates compounded over 1 year yield {(1+effective)*100:.4f}% increase."
        }

    def accumulation_function(self) -> Dict:
        """Accumulation function a(t): shows growth of $1 from time 0 to t"""
        annual_rate = round(random.uniform(0.02, 0.12), 4)
        compounds_per_year = random.choice([1, 2, 4, 12])
        time_period = random.randint(1, 10)
        initial_amount = round(random.uniform(100, 10000), 2)

        periods = time_period * compounds_per_year
        periodic_rate = annual_rate / compounds_per_year
        accumulation = round((1 + periodic_rate) ** periods, 6)
        final_amount = round(initial_amount * accumulation, 2)

        q_id = f"tv_accum_func_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${final_amount:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(initial_amount * (1 + annual_rate)**time_period, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(initial_amount * (1 + periodic_rate*periods), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(initial_amount * accumulation / compounds_per_year, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(initial_amount + initial_amount * accumulation, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Accumulation Function",
            "difficulty": 2,
            "question_text": f"If ${initial_amount:,.2f} is invested at {annual_rate*100:.2f}% annual interest compounded {compounds_per_year} times per year for {time_period} years, what is the final amount? (Note: a(t) = (1+i)^t for compound interest)",
            "choices": choices,
            "solution": f"a({time_period}) = (1 + {periodic_rate:.6f})^{periods} = {accumulation:.6f}. Amount = ${initial_amount:,.2f} × {accumulation:.6f} = ${final_amount:,.2f}",
            "explanation": f"The accumulation function a(t) shows how $1 grows. Here a({time_period}) = {accumulation:.6f}, so $1 becomes ${accumulation:.6f}."
        }

    def varying_interest_rates(self) -> Dict:
        """When interest rates vary: a(t) = exp(∫₀ᵗ δ(s) ds)"""
        pv = round(random.uniform(1000, 50000), 2)
        rate1 = round(random.uniform(0.01, 0.08), 4)
        rate2 = round(random.uniform(0.02, 0.12), 4)
        years1 = random.randint(1, 5)
        years2 = random.randint(1, 5)
        compounds = random.choice([1, 2, 4])

        periods1 = years1 * compounds
        periods2 = years2 * compounds
        periodic_rate1 = rate1 / compounds
        periodic_rate2 = rate2 / compounds

        after_period1 = round(pv * (1 + periodic_rate1) ** periods1, 2)
        final_amount = round(after_period1 * (1 + periodic_rate2) ** periods2, 2)

        q_id = f"tv_varying_rates_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${final_amount:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(pv * (1 + rate1 + rate2)**(years1 + years2), 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(pv * (1 + rate1)**years1 * (1 + rate2)**years2, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(after_period1 * (1 + periodic_rate2*periods2), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv * (1 + (rate1+rate2)/2)**(years1+years2), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Varying Interest Rates",
            "difficulty": 3,
            "question_text": f"${pv:,.2f} is invested for {years1} years at {rate1*100:.2f}% annual (compounded {compounds}x/year), then for {years2} more years at {rate2*100:.2f}% annual (compounded {compounds}x/year). What is the final amount?",
            "choices": choices,
            "solution": f"After {years1} yr: {pv} × (1 + {periodic_rate1:.6f})^{periods1} = ${after_period1:,.2f}. Then: ${after_period1:,.2f} × (1 + {periodic_rate2:.6f})^{periods2} = ${final_amount:,.2f}",
            "explanation": f"Apply compound interest formula separately for each period with its respective rate. First accumulate at rate1, then the resulting amount accumulates at rate2."
        }

    def dollar_weighted_return(self) -> Dict:
        """Dollar-weighted return (internal rate of return): solves for i in equation of value"""
        initial_investment = round(random.uniform(10000, 50000), 2)
        cash_flow_month = random.randint(3, 9)
        cash_flow_amount = round(random.uniform(1000, 10000), 2)
        final_value = round(random.uniform(15000, 80000), 2)

        # Approximate dollar-weighted return (simplified)
        net_gain = final_value - initial_investment - cash_flow_amount
        avg_balance = initial_investment + cash_flow_amount * (12 - cash_flow_month) / 12
        approx_dwr = round(net_gain / avg_balance, 4)

        q_id = f"tv_dwr_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{approx_dwr*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{round(net_gain / initial_investment, 4)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{round((final_value / initial_investment - 1), 4)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round(net_gain / final_value, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round((final_value - cash_flow_amount) / initial_investment, 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Dollar-Weighted Return",
            "difficulty": 3,
            "question_text": f"An investment account starts with ${initial_investment:,.2f}. After {cash_flow_month} months, ${cash_flow_amount:,.2f} is added. At the end of the year, the account value is ${final_value:,.2f}. Find the dollar-weighted return (to 4 decimal places).",
            "choices": choices,
            "solution": f"Approx DWR ≈ (Gain) / (Weighted Balance) ≈ ({net_gain:,.2f}) / ({avg_balance:,.2f}) ≈ {approx_dwr:.4f} = {approx_dwr*100:.4f}%",
            "explanation": f"Dollar-weighted return weights cash flows by how long they're invested. Initial amount in account for full year; additional ${cash_flow_amount:,.2f} for {12-cash_flow_month} months."
        }

    def time_weighted_return(self) -> Dict:
        """Time-weighted return: geometric mean of subperiod returns"""
        initial_value = round(random.uniform(10000, 50000), 2)
        value_after_cf = round(random.uniform(5000, initial_value * 1.3), 2)
        cash_flow = round(random.uniform(1000, 15000), 2)
        final_value = round(random.uniform(value_after_cf * 0.8, value_after_cf * 1.5), 2)

        return1 = (value_after_cf - cash_flow) / initial_value
        return2 = final_value / value_after_cf
        twr = round((return1 * return2) ** 0.5 - 1, 4)

        q_id = f"tv_twr_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{twr*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{round((final_value / initial_value - 1), 4)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{round((return1 + return2) / 2, 4)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round((final_value - cash_flow) / initial_value - 1, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round(((final_value / initial_value) ** 0.5 - 1), 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Time-Weighted Return",
            "difficulty": 3,
            "question_text": f"Portfolio value: ${initial_value:,.2f} initially. After 6 months: ${value_after_cf:,.2f}, then ${cash_flow:,.2f} is withdrawn. After 6 more months: ${final_value:,.2f}. Find time-weighted return.",
            "choices": choices,
            "solution": f"Return1 = ({value_after_cf:,.2f} - {cash_flow:,.2f}) / {initial_value:,.2f} = {return1:.6f}. Return2 = {final_value:,.2f} / {value_after_cf:,.2f} = {return2:.6f}. TWR = √({return1:.6f} × {return2:.6f}) - 1 = {twr:.4f} = {twr*100:.4f}%",
            "explanation": f"Time-weighted return eliminates impact of cash flows by computing geometric mean of subperiod returns. Removes timing discretion."
        }

    def inflation_adjusted_return(self) -> Dict:
        """Real return: (1 + nominal) / (1 + inflation) - 1"""
        nominal_return = round(random.uniform(0.01, 0.15), 4)
        inflation_rate = round(random.uniform(0.01, 0.08), 4)

        real_return = round((1 + nominal_return) / (1 + inflation_rate) - 1, 4)

        q_id = f"tv_inflation_adj_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{real_return*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{(nominal_return - inflation_rate)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{nominal_return*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round((1 + nominal_return) * (1 + inflation_rate) - 1, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{inflation_rate*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Inflation-Adjusted Return",
            "difficulty": 2,
            "question_text": f"An investment earns a nominal return of {nominal_return*100:.2f}%. If inflation is {inflation_rate*100:.2f}%, what is the real (inflation-adjusted) return?",
            "choices": choices,
            "solution": f"Real return = (1 + {nominal_return:.4f}) / (1 + {inflation_rate:.4f}) - 1 = {1+nominal_return:.6f} / {1+inflation_rate:.6f} - 1 = {real_return:.4f} = {real_return*100:.4f}%",
            "explanation": f"Real return accounts for purchasing power. The Fisher equation: (1 + r) = (1 + i) / (1 + π), where r is real, i is nominal, π is inflation."
        }

    def equation_of_value(self) -> Dict:
        """Equation of value at a focal date: sum of PV of cash flows = 0"""
        payment1 = round(random.uniform(1000, 10000), 2)
        years1 = random.randint(1, 3)
        payment2 = round(random.uniform(1000, 10000), 2)
        years2 = random.randint(4, 7)
        rate = round(random.uniform(0.02, 0.12), 4)

        pv_at_t0 = round(payment1 / (1 + rate)**years1 + payment2 / (1 + rate)**years2, 2)

        q_id = f"tv_eq_of_value_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv_at_t0:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment1 + payment2, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round((payment1 + payment2) / (1 + rate)**(years1 + years2), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment1 * (1 + rate)**years1 + payment2 * (1 + rate)**years2, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(payment1 / years1 + payment2 / years2, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Time Value of Money",
            "subtopic": "Equation of Value",
            "difficulty": 2,
            "question_text": f"Using an interest rate of {rate*100:.2f}%, what lump sum today is equivalent to ${payment1:,.2f} due in {years1} year(s) and ${payment2:,.2f} due in {years2} year(s)?",
            "choices": choices,
            "solution": f"PV = {payment1:,.2f} / (1 + {rate:.4f})^{years1} + {payment2:,.2f} / (1 + {rate:.4f})^{years2} = ${pv_at_t0:,.2f}",
            "explanation": f"The equation of value equates values at a focal date (time 0). Discount each payment back to present at the given rate."
        }

    # ===== TOPIC 2: ANNUITIES (20+ methods) =====

    def annuity_immediate_pv(self) -> Dict:
        """PV of ordinary annuity (annuity immediate): a_n = [1 - (1+i)^-n] / i"""
        payment = round(random.uniform(500, 5000), 2)
        periods = random.randint(5, 30)
        rate = round(random.uniform(0.01, 0.12), 4)

        pv = round(payment * (1 - (1 + rate) ** (-periods)) / rate, 2)

        q_id = f"ann_imm_pv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment * periods, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * (1 - (1 + rate)**(-periods+1)) / rate, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * periods / (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(payment * ((1 + rate)**periods - 1) / rate, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Annuity Immediate - Present Value",
            "difficulty": 1,
            "question_text": f"An ordinary annuity pays ${payment:,.2f} at the end of each period for {periods} periods. The interest rate is {rate*100:.2f}% per period. What is the present value?",
            "choices": choices,
            "solution": f"PV = PMT × a_n̄ = {payment:,.2f} × [1 - (1 + {rate:.4f})^-{periods}] / {rate:.4f} = {payment:,.2f} × {(1 - (1 + rate)**(-periods)) / rate:.6f} = ${pv:,.2f}",
            "explanation": f"Annuity immediate (ordinary annuity) has payments at end of each period. Use a_n̄ = [1 - (1+i)^-n] / i."
        }

    def annuity_immediate_fv(self) -> Dict:
        """FV of ordinary annuity: s_n = [(1+i)^n - 1] / i"""
        payment = round(random.uniform(500, 5000), 2)
        periods = random.randint(5, 30)
        rate = round(random.uniform(0.01, 0.12), 4)

        fv = round(payment * ((1 + rate) ** periods - 1) / rate, 2)

        q_id = f"ann_imm_fv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${fv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment * periods, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * (1 - (1 + rate)**(-periods)) / rate, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * periods * (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(payment * ((1 + rate)**periods - 1), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Annuity Immediate - Future Value",
            "difficulty": 1,
            "question_text": f"An ordinary annuity pays ${payment:,.2f} at the end of each period for {periods} periods. The interest rate is {rate*100:.2f}% per period. What is the future value?",
            "choices": choices,
            "solution": f"FV = PMT × s_n̄ = {payment:,.2f} × [(1 + {rate:.4f})^{periods} - 1] / {rate:.4f} = {payment:,.2f} × {((1 + rate)**periods - 1) / rate:.6f} = ${fv:,.2f}",
            "explanation": f"For annuity immediate with FV, use s_n̄ = [(1+i)^n - 1] / i. Accumulate each payment to the end of the annuity term."
        }

    def annuity_due_pv(self) -> Dict:
        """PV of annuity due: ä_n = [1 - (1+i)^-n] / i × (1+i)"""
        payment = round(random.uniform(500, 5000), 2)
        periods = random.randint(5, 30)
        rate = round(random.uniform(0.01, 0.12), 4)

        pv = round(payment * (1 - (1 + rate) ** (-periods)) / rate * (1 + rate), 2)

        q_id = f"ann_due_pv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment * (1 - (1 + rate) ** (-periods)) / rate, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * periods, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * (1 - (1 + rate)**(-periods+1)) / rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv / (1 + rate), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Annuity Due - Present Value",
            "difficulty": 2,
            "question_text": f"An annuity due pays ${payment:,.2f} at the beginning of each period for {periods} periods. The interest rate is {rate*100:.2f}% per period. What is the present value?",
            "choices": choices,
            "solution": f"PV = PMT × ä_n̄ = {payment:,.2f} × [1 - (1 + {rate:.4f})^-{periods}] / {rate:.4f} × (1 + {rate:.4f}) = ${pv:,.2f}",
            "explanation": f"Annuity due has payments at beginning of each period. ä_n̄ = a_n̄ × (1+i). The extra (1+i) factor accounts for payments one period earlier."
        }

    def annuity_due_fv(self) -> Dict:
        """FV of annuity due: s̈_n = [(1+i)^n - 1] / i × (1+i)"""
        payment = round(random.uniform(500, 5000), 2)
        periods = random.randint(5, 30)
        rate = round(random.uniform(0.01, 0.12), 4)

        fv = round(payment * ((1 + rate) ** periods - 1) / rate * (1 + rate), 2)

        q_id = f"ann_due_fv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${fv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment * ((1 + rate) ** periods - 1) / rate, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * periods * (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * (1 - (1 + rate) ** (-periods)) / rate * (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(fv / (1 + rate), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Annuity Due - Future Value",
            "difficulty": 2,
            "question_text": f"An annuity due pays ${payment:,.2f} at the beginning of each period for {periods} periods. The interest rate is {rate*100:.2f}% per period. What is the future value?",
            "choices": choices,
            "solution": f"FV = PMT × s̈_n̄ = {payment:,.2f} × [(1 + {rate:.4f})^{periods} - 1] / {rate:.4f} × (1 + {rate:.4f}) = ${fv:,.2f}",
            "explanation": f"Annuity due FV: s̈_n̄ = s_n̄ × (1+i). Each payment earns interest one additional period compared to annuity immediate."
        }

    def deferred_annuity_pv(self) -> Dict:
        """PV of deferred annuity (immediate): discount from start of payments"""
        payment = round(random.uniform(500, 5000), 2)
        payment_periods = random.randint(5, 20)
        deferral_periods = random.randint(1, 10)
        rate = round(random.uniform(0.01, 0.12), 4)

        # PV at time of first payment
        pv_at_first_payment = round(payment * (1 - (1 + rate) ** (-payment_periods)) / rate, 2)
        # Discount back to time 0
        pv = round(pv_at_first_payment / (1 + rate) ** deferral_periods, 2)

        q_id = f"ann_def_pv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${pv_at_first_payment:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * payment_periods / (1 + rate)**deferral_periods, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * (1 - (1 + rate)**(-payment_periods)) / rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv * (1 + rate), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Deferred Annuity - Present Value",
            "difficulty": 2,
            "question_text": f"An annuity pays ${payment:,.2f} at the end of each period, starting {deferral_periods} period(s) from now, for {payment_periods} period(s). The interest rate is {rate*100:.2f}%. What is the present value?",
            "choices": choices,
            "solution": f"PV at time {deferral_periods} = {payment:,.2f} × a_{payment_periods}̄ = ${pv_at_first_payment:,.2f}. PV at time 0 = ${pv_at_first_payment:,.2f} / (1.{rate:.4f})^{deferral_periods} = ${pv:,.2f}",
            "explanation": f"For deferred annuities, calculate the PV at the start of payments, then discount back to time 0."
        }

    def deferred_annuity_due_pv(self) -> Dict:
        """PV of deferred annuity due: payments at beginning of each period"""
        payment = round(random.uniform(500, 5000), 2)
        payment_periods = random.randint(5, 20)
        deferral_periods = random.randint(1, 10)
        rate = round(random.uniform(0.01, 0.12), 4)

        # PV at time of first payment (annuity due)
        pv_at_first_payment = round(payment * (1 - (1 + rate) ** (-payment_periods)) / rate * (1 + rate), 2)
        # Discount back to time 0 (but first payment is at time deferral_periods, so discount only deferral_periods)
        pv = round(pv_at_first_payment / (1 + rate) ** (deferral_periods - 1), 2)

        q_id = f"ann_def_due_pv_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment * (1 - (1 + rate) ** (-payment_periods)) / rate * (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * payment_periods / (1 + rate)**(deferral_periods-1), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(pv / (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv * (1 + rate), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Deferred Annuity Due - Present Value",
            "difficulty": 2,
            "question_text": f"An annuity due pays ${payment:,.2f} at the beginning of each period, starting {deferral_periods} period(s) from now, for {payment_periods} period(s). The interest rate is {rate*100:.2f}%. What is the present value?",
            "choices": choices,
            "solution": f"PV at first payment = {payment:,.2f} × ä_{payment_periods}̄ = ${pv_at_first_payment:,.2f}. First payment is at time {deferral_periods}, so PV at time 0 = ${pv_at_first_payment:,.2f} / (1.{rate:.4f})^{deferral_periods-1} = ${pv:,.2f}",
            "explanation": f"Deferred annuity due: first payment is at time deferral_periods (beginning of first period), then continue for payment_periods."
        }

    def perpetuity_immediate(self) -> Dict:
        """PV of perpetuity immediate: a_∞ = 1 / i"""
        payment = round(random.uniform(500, 5000), 2)
        rate = round(random.uniform(0.01, 0.15), 4)

        pv = round(payment / rate, 2)

        q_id = f"ann_perp_imm_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${payment:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment / rate / (1 + rate), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"Cannot be determined", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Perpetuity Immediate",
            "difficulty": 2,
            "question_text": f"A perpetuity pays ${payment:,.2f} at the end of each period forever. The interest rate is {rate*100:.2f}% per period. What is the present value?",
            "choices": choices,
            "solution": f"PV = PMT / i = {payment:,.2f} / {rate:.4f} = ${pv:,.2f}",
            "explanation": f"For perpetuity immediate (payments at end): a_∞ = 1/i. As n→∞, the annuity factor approaches 1/i."
        }

    def perpetuity_due(self) -> Dict:
        """PV of perpetuity due: ä_∞ = 1 / i × (1+i)"""
        payment = round(random.uniform(500, 5000), 2)
        rate = round(random.uniform(0.01, 0.15), 4)

        pv = round(payment / rate * (1 + rate), 2)

        q_id = f"ann_perp_due_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment / rate, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${payment:,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * (1 + rate) / rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(pv / (1 + rate), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Perpetuity Due",
            "difficulty": 2,
            "question_text": f"A perpetuity due pays ${payment:,.2f} at the beginning of each period forever. The interest rate is {rate*100:.2f}% per period. What is the present value?",
            "choices": choices,
            "solution": f"PV = PMT × (1 + i) / i = {payment:,.2f} × (1 + {rate:.4f}) / {rate:.4f} = ${pv:,.2f}",
            "explanation": f"Perpetuity due: ä_∞ = (1+i)/i. Payments are one period earlier than perpetuity immediate, so multiply by (1+i)."
        }

    def increasing_annuity_arithmetic(self) -> Dict:
        """Arithmetic increasing annuity: payments are 1, 2, 3, ..., n"""
        initial_payment = round(random.uniform(100, 1000), 2)
        periods = random.randint(5, 20)
        rate = round(random.uniform(0.01, 0.12), 4)

        # (Ia)_n̄ = [a_n̄ - n(1+i)^-n] / i
        a_n = (1 - (1 + rate) ** (-periods)) / rate
        ia_n = (a_n - periods * (1 + rate) ** (-periods)) / rate
        pv = round(initial_payment * ia_n, 2)

        q_id = f"ann_inc_arith_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(initial_payment * periods * (1 + rate)**periods / rate, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(initial_payment * a_n, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(initial_payment * periods * a_n, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(initial_payment * periods / rate, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Increasing Annuity (Arithmetic)",
            "difficulty": 3,
            "question_text": f"An annuity pays ${initial_payment:,.2f} at the end of period 1, ${round(initial_payment*2, 2):,.2f} at the end of period 2, and so on, increasing by ${initial_payment:,.2f} each period for {periods} periods total. The interest rate is {rate*100:.2f}%. What is the present value?",
            "choices": choices,
            "solution": f"(Ia)_n̄ = [a_n̄ - n(1+i)^-n] / i. With i = {rate:.4f}, n = {periods}: (Ia)_n̄ ≈ {ia_n:.6f}. PV = {initial_payment:,.2f} × {ia_n:.6f} = ${pv:,.2f}",
            "explanation": f"Arithmetic increasing annuity with increment = ${initial_payment:,.2f}. Formula: (Ia)_n̄ involves both a_n̄ and adjustment for the increasing pattern."
        }

    def decreasing_annuity_arithmetic(self) -> Dict:
        """Arithmetic decreasing annuity: payments are n, n-1, ..., 1"""
        initial_payment = round(random.uniform(100, 1000), 2)
        periods = random.randint(5, 20)
        rate = round(random.uniform(0.01, 0.12), 4)

        # (Da)_n̄ = [n - a_n̄] / i
        a_n = (1 - (1 + rate) ** (-periods)) / rate
        da_n = (periods - a_n) / rate
        pv = round(initial_payment * da_n, 2)

        q_id = f"ann_dec_arith_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(initial_payment * periods * a_n, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(initial_payment * a_n, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(initial_payment * (periods - a_n), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(initial_payment * periods / rate, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Decreasing Annuity (Arithmetic)",
            "difficulty": 3,
            "question_text": f"An annuity pays ${round(initial_payment * periods, 2):,.2f} at the end of period 1, ${round(initial_payment * (periods-1), 2):,.2f} at the end of period 2, and so on, decreasing by ${initial_payment:,.2f} each period for {periods} periods total. The interest rate is {rate*100:.2f}%. What is the present value?",
            "choices": choices,
            "solution": f"(Da)_n̄ = [n - a_n̄] / i. With i = {rate:.4f}, n = {periods}: a_n̄ ≈ {a_n:.6f}, (Da)_n̄ ≈ {da_n:.6f}. PV = {initial_payment:,.2f} × {da_n:.6f} = ${pv:,.2f}",
            "explanation": f"Decreasing annuity: first payment is n times the unit, last is 1 unit. Formula: (Da)_n̄ = (n - a_n̄) / i."
        }

    def increasing_annuity_geometric(self) -> Dict:
        """Geometric increasing annuity: payments grow by fixed rate"""
        initial_payment = round(random.uniform(100, 1000), 2)
        growth_rate = round(random.uniform(0.01, 0.15), 4)
        periods = random.randint(5, 20)
        interest_rate = round(random.uniform(0.01, 0.20), 4)

        if abs(growth_rate - interest_rate) < 0.0001:
            # Special case: growth rate ≈ interest rate
            pv = round(initial_payment * periods / (1 + interest_rate), 2)
        else:
            # PV = PMT × [1 - ((1+g)/(1+i))^n] / (i - g)
            ratio = (1 + growth_rate) / (1 + interest_rate)
            pv = round(initial_payment * (1 - ratio ** periods) / (interest_rate - growth_rate), 2)

        q_id = f"ann_inc_geom_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(initial_payment * (1 - (1 + growth_rate)**periods) / growth_rate, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(initial_payment * (1 - (1 + interest_rate)**(-periods)) / interest_rate, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(initial_payment * periods / (1 + interest_rate), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(initial_payment * ((1 + growth_rate)**periods - 1) / growth_rate, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Increasing Annuity (Geometric)",
            "difficulty": 3,
            "question_text": f"An annuity pays ${initial_payment:,.2f} at the end of period 1. Each subsequent payment grows by {growth_rate*100:.2f}%. There are {periods} payments total. The interest rate is {interest_rate*100:.2f}%. What is the present value?",
            "choices": choices,
            "solution": f"PV = PMT × [1 - ((1+g)/(1+i))^n] / (i-g) = {initial_payment:,.2f} × [1 - ({(1+growth_rate)/(1+interest_rate):.6f})^{periods}] / ({interest_rate-growth_rate:.4f}) = ${pv:,.2f}",
            "explanation": f"Geometric increasing annuity with growth rate g = {growth_rate*100:.2f}%. Payments: ${initial_payment:,.2f}, ${round(initial_payment*(1+growth_rate), 2):,.2f}, etc."
        }

    def geometric_perpetuity(self) -> Dict:
        """Geometric perpetuity: payments grow forever at rate g"""
        initial_payment = round(random.uniform(100, 1000), 2)
        growth_rate = round(random.uniform(0.01, 0.10), 4)
        interest_rate = round(random.uniform(growth_rate + 0.01, 0.20), 4)

        # PV = PMT / (i - g), where i > g
        pv = round(initial_payment / (interest_rate - growth_rate), 2)

        q_id = f"ann_geom_perp_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(initial_payment / interest_rate, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(initial_payment / growth_rate, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(initial_payment / (interest_rate + growth_rate), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"Cannot be determined - diverges", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Geometric Perpetuity",
            "difficulty": 3,
            "question_text": f"A perpetuity pays ${initial_payment:,.2f} at the end of period 1. Each subsequent payment grows by {growth_rate*100:.2f}%. The interest rate is {interest_rate*100:.2f}%. What is the present value? (Assume i > g)",
            "choices": choices,
            "solution": f"PV = PMT / (i - g) = {initial_payment:,.2f} / ({interest_rate:.4f} - {growth_rate:.4f}) = {initial_payment:,.2f} / {interest_rate - growth_rate:.4f} = ${pv:,.2f}",
            "explanation": f"Geometric perpetuity converges only if i > g. Formula: PV = PMT / (i - g). Payments grow forever at rate g = {growth_rate*100:.2f}%."
        }

    def annuity_with_different_payment_interest_periods(self) -> Dict:
        """Annuity where payment frequency differs from compounding frequency"""
        payment = round(random.uniform(500, 3000), 2)
        num_payments = random.randint(8, 24)
        payments_per_year = random.choice([2, 4, 12])
        annual_rate = round(random.uniform(0.02, 0.12), 4)
        compounds_per_year = random.choice([2, 4, 12])

        years = num_payments / payments_per_year
        periods_compound = int(years * compounds_per_year)
        periodic_rate_compound = annual_rate / compounds_per_year

        # Approximate: use effective rate for payment period
        payment_periods_per_year = payments_per_year
        effective_per_payment = (1 + periodic_rate_compound) ** (compounds_per_year / payments_per_year) - 1

        pv = round(payment * (1 - (1 + effective_per_payment) ** (-num_payments)) / effective_per_payment, 2)

        q_id = f"ann_diff_periods_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment * num_payments, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * (1 - (1 + annual_rate/payment_periods_per_year)**(-num_payments)) / (annual_rate/payment_periods_per_year), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * (1 - (1 + periodic_rate_compound)**(-num_payments)) / periodic_rate_compound, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(payment * (1 - (1 + annual_rate)**(-years)) / annual_rate, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Annuity - Different Payment/Interest Periods",
            "difficulty": 3,
            "question_text": f"An annuity pays ${payment:,.2f} every {12//payments_per_year} month(s) for {num_payments} payments. Interest is {annual_rate*100:.2f}% annual, compounded {compounds_per_year} times/year. What is the PV?",
            "choices": choices,
            "solution": f"Effective rate per payment period = (1 + {periodic_rate_compound:.6f})^({compounds_per_year}/{payments_per_year}) - 1 ≈ {effective_per_payment:.6f}. PV = {payment:,.2f} × a_{num_payments}̄ = ${pv:,.2f}",
            "explanation": f"When payment frequency ≠ compounding frequency, find the effective rate per payment period by converting the periodic compound rate."
        }

    def continuous_annuity(self) -> Dict:
        """Annuity with continuous payment flow (integration-based)"""
        payment_rate = round(random.uniform(1000, 10000), 2)  # Payment per unit time
        duration = random.randint(2, 15)
        force_of_interest = round(random.uniform(0.01, 0.12), 4)

        # PV = ∫₀ⁿ P × e^(-δt) dt = P × (1 - e^(-δn)) / δ
        pv = round(payment_rate * (1 - math.exp(-force_of_interest * duration)) / force_of_interest, 2)

        q_id = f"ann_continuous_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment_rate * duration, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment_rate * (1 - math.exp(-force_of_interest * duration)), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment_rate * duration / (1 + force_of_interest), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(payment_rate * duration * math.exp(-force_of_interest * duration), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Continuous Annuity",
            "difficulty": 3,
            "question_text": f"A continuous annuity pays at a rate of ${payment_rate:,.2f} per unit time for {duration} time periods. The force of interest is {force_of_interest*100:.2f}%. What is the present value?",
            "choices": choices,
            "solution": f"PV = ∫₀^{duration} {payment_rate:,.2f} × e^(-{force_of_interest:.4f}t) dt = {payment_rate:,.2f} × (1 - e^(-{force_of_interest:.4f}×{duration})) / {force_of_interest:.4f} = ${pv:,.2f}",
            "explanation": f"Continuous annuity: total payment flow is continuous over time. Integral evaluates to (1 - e^(-δn)) / δ."
        }

    def annuity_n_payments_solve_for_n(self) -> Dict:
        """Given PV, PMT, and i, solve for n (number of payments)"""
        pv = round(random.uniform(5000, 50000), 2)
        payment = round(random.uniform(500, 5000), 2)
        rate = round(random.uniform(0.01, 0.12), 4)

        # From a_n̄ = PV / PMT, solve n
        # a_n̄ = (1 - (1+i)^-n) / i
        # n = -ln(1 - i × a_n̄) / ln(1+i)
        a_n = pv / payment
        n = round(-math.log(1 - rate * a_n) / math.log(1 + rate), 1)

        q_id = f"ann_solve_n_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{n:.1f}", "is_correct": True},
            {"label": "B", "text": f"{round(pv / payment, 1)}", "is_correct": False},
            {"label": "C", "text": f"{round(math.log(pv / payment) / math.log(1 + rate), 1)}", "is_correct": False},
            {"label": "D", "text": f"{round(pv / payment / rate, 1)}", "is_correct": False},
            {"label": "E", "text": f"{round(pv / (payment * rate), 1)}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Solve for n - Number of Payments",
            "difficulty": 2,
            "question_text": f"An ordinary annuity has a present value of ${pv:,.2f}, with payments of ${payment:,.2f} at the end of each period. If the interest rate is {rate*100:.2f}% per period, how many payments are there?",
            "choices": choices,
            "solution": f"a_n̄ = PV / PMT = {pv:,.2f} / {payment:,.2f} = {a_n:.6f}. n = -ln(1 - {rate:.4f} × {a_n:.6f}) / ln(1 + {rate:.4f}) ≈ {n:.1f}",
            "explanation": f"Rearrange the annuity formula: n = -ln(1 - i·a_n̄) / ln(1+i). Note: n will typically not be an integer."
        }

    def annuity_solve_for_interest_rate(self) -> Dict:
        """Given PV, PMT, and n, solve for i (approximation)"""
        pv = round(random.uniform(5000, 40000), 2)
        payment = round(random.uniform(500, 3000), 2)
        periods = random.randint(10, 30)

        # This requires numerical solution. Use approximation or Newton's method.
        # For demo: use known rates and verify
        trial_rate = round(random.uniform(0.01, 0.12), 4)
        calc_pv = round(payment * (1 - (1 + trial_rate) ** (-periods)) / trial_rate, 2)

        q_id = f"ann_solve_i_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{trial_rate*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{round(payment / pv, 4)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{round(1 / periods, 4)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round((payment - pv / periods) / pv, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round(math.log(payment / (payment - pv / periods)), 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Solve for Interest Rate",
            "difficulty": 3,
            "question_text": f"An ordinary annuity has a present value of ${calc_pv:,.2f}, with payments of ${payment:,.2f} at the end of each period for {periods} periods. What is the interest rate per period?",
            "choices": choices,
            "solution": f"Solve: {calc_pv:,.2f} = {payment:,.2f} × [1 - (1+i)^-{periods}] / i. Using calculator/numerical methods: i ≈ {trial_rate:.4f} = {trial_rate*100:.4f}%",
            "explanation": f"No closed-form solution exists. Use financial calculator, spreadsheet, or Newton-Raphson method. Trial and error: test values until a_n̄ × PMT ≈ PV."
        }

    def Ia_angle_n(self) -> Dict:
        """Arithmetic increasing annuity immediate: (Ia)_n̄"""
        unit_increment = round(random.uniform(100, 500), 2)
        periods = random.randint(5, 20)
        rate = round(random.uniform(0.01, 0.12), 4)

        # (Ia)_n̄ = [a_n̄ - n(1+i)^-n] / i
        a_n = (1 - (1 + rate) ** (-periods)) / rate
        ia_n = (a_n - periods * (1 + rate) ** (-periods)) / rate
        pv = round(unit_increment * ia_n, 2)

        q_id = f"ann_ia_n_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(unit_increment * periods * (periods + 1) / 2 / (1 + rate)**periods, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(unit_increment * periods / rate, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(unit_increment * ((1 + rate)**periods - 1) / rate / (1 + rate)**periods, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(unit_increment * a_n * periods, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Increasing Annuity Notation (Ia)_n",
            "difficulty": 2,
            "question_text": f"Find the present value of an annuity where payments at the end of each period are: ${unit_increment:,.2f}, ${round(2*unit_increment, 2):,.2f}, ..., ${round(periods*unit_increment, 2):,.2f}. Interest is {rate*100:.2f}% per period.",
            "choices": choices,
            "solution": f"(Ia)_{periods}̄ = [a_n̄ - n(1+i)^-n] / i ≈ {ia_n:.6f}. PV = {unit_increment:,.2f} × {ia_n:.6f} = ${pv:,.2f}",
            "explanation": f"Standard notation for arithmetic increasing annuity. Payments: 1, 2, 3, ..., n units. Formula uses both a_n̄ and a discount factor."
        }

    def Da_angle_n(self) -> Dict:
        """Arithmetic decreasing annuity immediate: (Da)_n̄"""
        unit_increment = round(random.uniform(100, 500), 2)
        periods = random.randint(5, 20)
        rate = round(random.uniform(0.01, 0.12), 4)

        # (Da)_n̄ = [n - a_n̄] / i
        a_n = (1 - (1 + rate) ** (-periods)) / rate
        da_n = (periods - a_n) / rate
        pv = round(unit_increment * da_n, 2)

        q_id = f"ann_da_n_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(unit_increment * periods * a_n, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(unit_increment * a_n, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(unit_increment * periods / rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(unit_increment * (periods**2) / (1 + rate)**periods, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Decreasing Annuity Notation (Da)_n",
            "difficulty": 2,
            "question_text": f"Find the present value of an annuity where payments at the end of each period are: ${round(periods*unit_increment, 2):,.2f}, ${round((periods-1)*unit_increment, 2):,.2f}, ..., ${unit_increment:,.2f}. Interest is {rate*100:.2f}% per period.",
            "choices": choices,
            "solution": f"(Da)_{periods}̄ = [n - a_n̄] / i where n = {periods}, a_n̄ ≈ {a_n:.6f}. (Da)_{periods}̄ ≈ {da_n:.6f}. PV = {unit_increment:,.2f} × {da_n:.6f} = ${pv:,.2f}",
            "explanation": f"Arithmetic decreasing annuity: payments n, n-1, ..., 1 units. Formula: (Da)_n̄ = (n - a_n̄) / i."
        }

    def varying_annuity_general(self) -> Dict:
        """General varying annuity: custom sequence of payments"""
        rates = [round(random.uniform(100, 2000), 2) for _ in range(5)]
        interest_rate = round(random.uniform(0.01, 0.12), 4)

        pv = sum(payment / (1 + interest_rate) ** (i + 1) for i, payment in enumerate(rates))
        pv = round(pv, 2)

        q_id = f"ann_varying_general_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(sum(rates), 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(sum(rates) / (1 + interest_rate)**len(rates), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(sum(rates) * (1 - (1 + interest_rate)**(-len(rates))) / interest_rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(sum(rates) / len(rates), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Varying Annuity - General",
            "difficulty": 2,
            "question_text": f"A 5-period annuity has payments: ${rates[0]:,.2f}; ${rates[1]:,.2f}; ${rates[2]:,.2f}; ${rates[3]:,.2f}; ${rates[4]:,.2f} (at the end of periods 1-5 respectively). The interest rate is {interest_rate*100:.2f}%. Find the present value.",
            "choices": choices,
            "solution": f"PV = Σ(Payment_t / (1+i)^t) = {rates[0]:,.2f}/(1.{interest_rate:.4f}) + ... = ${pv:,.2f}",
            "explanation": f"For custom varying payment sequences, discount each payment individually back to the present and sum."
        }

    def annuity_payable_m_times_per_year(self) -> Dict:
        """Annuity with m payments per year, n years total"""
        annual_payment_total = round(random.uniform(2000, 10000), 2)
        payments_per_year = random.choice([2, 4, 12])
        years = random.randint(3, 15)
        annual_rate = round(random.uniform(0.01, 0.12), 4)

        payment_per_period = annual_payment_total / payments_per_year
        total_periods = years * payments_per_year
        periodic_rate = annual_rate / payments_per_year

        pv = round(payment_per_period * (1 - (1 + periodic_rate) ** (-total_periods)) / periodic_rate, 2)

        q_id = f"ann_m_per_year_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${pv:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(annual_payment_total * (1 - (1 + annual_rate)**(-years)) / annual_rate, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(annual_payment_total * years, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment_per_period * total_periods, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(annual_payment_total * years / (1 + annual_rate)**years, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Annuities",
            "subtopic": "Annuity Payable m Times Per Year",
            "difficulty": 2,
            "question_text": f"An annuity pays a total of ${annual_payment_total:,.2f} per year in {payments_per_year} equal installments for {years} years. The interest rate is {annual_rate*100:.2f}% annual. What is the present value?",
            "choices": choices,
            "solution": f"Each payment = ${annual_payment_total:,.2f} / {payments_per_year} = ${payment_per_period:,.2f}. Total periods = {years} × {payments_per_year} = {total_periods}. Periodic rate = {annual_rate*100:.2f}% / {payments_per_year} = {periodic_rate*100:.4f}%. PV = ${pv:,.2f}",
            "explanation": f"Convert annual amounts to payment periods. {payments_per_year} payments/year for {years} years = {total_periods} total payment periods."
        }

    # ===== TOPIC 3: LOANS (10+ methods) =====

    def loan_amortization_payment(self) -> Dict:
        """Calculate loan payment: PMT = L × i / (1 - (1+i)^-n)"""
        loan_amount = round(random.uniform(50000, 500000), 2)
        periods = random.randint(60, 360)
        rate = round(random.uniform(0.002, 0.015), 6)

        # Monthly payment = L × [i(1+i)^n] / [(1+i)^n - 1]
        payment = round(loan_amount * rate * (1 + rate) ** periods / ((1 + rate) ** periods - 1), 2)

        q_id = f"loan_amort_pmt_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${payment:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(loan_amount / periods, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(loan_amount * rate, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(loan_amount * (1 + rate)**periods / periods, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(loan_amount * rate / (1 - (1 + rate)**(-periods)), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Amortization - Payment Calculation",
            "difficulty": 1,
            "question_text": f"A loan of ${loan_amount:,.2f} is to be repaid with {periods} equal payments at the end of each period. The interest rate is {rate*100:.4f}% per period. What is the periodic payment?",
            "choices": choices,
            "solution": f"PMT = L × i(1+i)^n / [(1+i)^n - 1] = {loan_amount:,.2f} × {rate:.6f} × {(1+rate)**periods:.6f} / ({(1+rate)**periods:.6f} - 1) = ${payment:,.2f}",
            "explanation": f"The loan payment formula is the reciprocal of the annuity formula. PV = PMT × a_n̄, so PMT = PV / a_n̄."
        }

    def loan_outstanding_balance(self) -> Dict:
        """Outstanding balance after k payments: B_k = L(1+i)^k - PMT × s_k̄"""
        loan_amount = round(random.uniform(50000, 500000), 2)
        total_periods = random.randint(120, 360)
        rate = round(random.uniform(0.002, 0.015), 6)
        k_payments_made = random.randint(1, total_periods - 1)

        payment = round(loan_amount * rate * (1 + rate) ** total_periods / ((1 + rate) ** total_periods - 1), 2)
        balance = round(loan_amount * (1 + rate) ** k_payments_made - payment * (((1 + rate) ** k_payments_made - 1) / rate), 2)

        q_id = f"loan_balance_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${balance:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(loan_amount - payment * k_payments_made, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(payment * (total_periods - k_payments_made), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(loan_amount * (1 + rate) ** (total_periods - k_payments_made), 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(loan_amount / (1 + rate) ** k_payments_made, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Outstanding Balance",
            "difficulty": 2,
            "question_text": f"A ${loan_amount:,.2f} loan is repaid with {total_periods} equal payments at {rate*100:.4f}% per period. After {k_payments_made} payments have been made, what is the outstanding balance?",
            "choices": choices,
            "solution": f"B_k = L(1+i)^k - PMT × s_k̄ = {loan_amount:,.2f} × {(1+rate)**k_payments_made:.6f} - {payment:,.2f} × {((1+rate)**k_payments_made - 1)/rate:.6f} = ${balance:,.2f}",
            "explanation": f"The outstanding balance can be computed as the future value of the original loan minus the future value of payments made."
        }

    def loan_principal_repaid_in_kth_payment(self) -> Dict:
        """Principal repaid in kth payment: P_k = PMT × [1 - (1+i)^(k-n)]"""
        loan_amount = round(random.uniform(50000, 500000), 2)
        total_periods = random.randint(120, 360)
        rate = round(random.uniform(0.002, 0.015), 6)
        k_period = random.randint(1, total_periods - 1)

        payment = round(loan_amount * rate * (1 + rate) ** total_periods / ((1 + rate) ** total_periods - 1), 2)
        principal_in_k = round(payment * (1 - (1 + rate) ** (k_period - total_periods)), 2)

        q_id = f"loan_principal_k_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${principal_in_k:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${payment:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(loan_amount / total_periods, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * (1 + rate)**k_period, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(payment / (1 + rate)**k_period, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Principal in kth Payment",
            "difficulty": 2,
            "question_text": f"A ${loan_amount:,.2f} loan is repaid with {total_periods} equal payments of ${payment:,.2f} at {rate*100:.4f}% per period. How much principal is repaid in payment {k_period}?",
            "choices": choices,
            "solution": f"P_k = PMT × [1 - (1+i)^(k-n)] = {payment:,.2f} × [1 - {(1+rate)**(k_period-total_periods):.8f}] = ${principal_in_k:,.2f}",
            "explanation": f"Principal repaid in payment k = Payment - Interest in payment k. Early payments are mostly interest; later ones are mostly principal."
        }

    def loan_interest_in_kth_payment(self) -> Dict:
        """Interest in kth payment: I_k = PMT × (1+i)^(k-1-n)"""
        loan_amount = round(random.uniform(50000, 500000), 2)
        total_periods = random.randint(120, 360)
        rate = round(random.uniform(0.002, 0.015), 6)
        k_period = random.randint(1, total_periods - 1)

        payment = round(loan_amount * rate * (1 + rate) ** total_periods / ((1 + rate) ** total_periods - 1), 2)
        interest_in_k = round(payment * (1 + rate) ** (k_period - 1 - total_periods), 2)

        q_id = f"loan_interest_k_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${interest_in_k:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(payment - interest_in_k, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(loan_amount * rate, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(payment * rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${payment:,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Interest in kth Payment",
            "difficulty": 2,
            "question_text": f"A ${loan_amount:,.2f} loan is repaid with {total_periods} equal payments of ${payment:,.2f} at {rate*100:.4f}% per period. How much interest is paid in payment {k_period}?",
            "choices": choices,
            "solution": f"I_k = PMT × (1+i)^(k-1-n) = {payment:,.2f} × {(1+rate)**(k_period-1-total_periods):.8f} = ${interest_in_k:,.2f}",
            "explanation": f"Interest in payment k = Outstanding balance before payment k × periodic rate. Or use formula: I_k = PMT × (1+i)^(k-1-n)."
        }

    def sinking_fund_method(self) -> Dict:
        """Sinking fund: annual interest + annual sinking fund deposit"""
        loan_amount = round(random.uniform(100000, 1000000), 2)
        years = random.randint(5, 20)
        loan_rate = round(random.uniform(0.02, 0.08), 4)
        sinking_rate = round(random.uniform(0.01, 0.06), 4)

        # Annual interest payment
        annual_interest = round(loan_amount * loan_rate, 2)
        # Sinking fund deposit (to accumulate to loan amount)
        sinking_deposit = round(loan_amount * sinking_rate / ((1 + sinking_rate) ** years - 1), 2)
        # Total annual payment
        total_payment = round(annual_interest + sinking_deposit, 2)

        q_id = f"loan_sinking_fund_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${total_payment:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${annual_interest:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${sinking_deposit:,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(loan_amount / years, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(loan_amount * (loan_rate + sinking_rate), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Sinking Fund Method",
            "difficulty": 2,
            "question_text": f"A ${loan_amount:,.2f} bond is issued with interest paid annually at {loan_rate*100:.2f}%. The issuer must accumulate ${loan_amount:,.2f} in a sinking fund earning {sinking_rate*100:.2f}% annually to retire the bond in {years} years. What is the total annual payment (interest + sinking fund deposit)?",
            "choices": choices,
            "solution": f"Interest = {loan_amount:,.2f} × {loan_rate:.4f} = ${annual_interest:,.2f}. Sinking fund = {loan_amount:,.2f} × {sinking_rate:.4f} / [(1.{sinking_rate:.4f})^{years} - 1] = ${sinking_deposit:,.2f}. Total = ${total_payment:,.2f}",
            "explanation": f"Sinking fund method: pay interest annually, make deposits to a separate account to accumulate the principal for repayment."
        }

    def sinking_fund_vs_amortization(self) -> Dict:
        """Compare sinking fund vs amortization methods"""
        loan_amount = round(random.uniform(100000, 500000), 2)
        years = random.randint(5, 15)
        loan_rate = round(random.uniform(0.02, 0.08), 4)
        periodic_rate = loan_rate / 12
        months = years * 12

        # Amortization method
        amort_payment = round(loan_amount * periodic_rate * (1 + periodic_rate) ** months / ((1 + periodic_rate) ** months - 1), 2)

        # Sinking fund method (annual)
        annual_interest = round(loan_amount * loan_rate, 2)
        sinking_deposit = round(loan_amount * loan_rate / ((1 + loan_rate) ** years - 1), 2)
        sinking_payment = round(annual_interest + sinking_deposit, 2)

        # Usually amortization is larger early
        lower_method = min(amort_payment * 12, sinking_payment)

        q_id = f"loan_sink_vs_amort_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"Sinking fund requires ${sinking_payment:,.2f}/year; Amortization requires ${round(amort_payment*12, 2):,.2f}/year", "is_correct": True},
            {"label": "B", "text": f"Both methods cost the same", "is_correct": False},
            {"label": "C", "text": f"Amortization requires ${sinking_payment:,.2f}/year; Sinking fund requires ${round(amort_payment*12, 2):,.2f}/year", "is_correct": False},
            {"label": "D", "text": f"Sinking fund is always more expensive", "is_correct": False},
            {"label": "E", "text": f"Cannot be compared without knowing investment returns", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Sinking Fund vs Amortization",
            "difficulty": 3,
            "question_text": f"A ${loan_amount:,.2f} loan has a {loan_rate*100:.2f}% interest rate. Compare annual costs: (A) Sinking fund method over {years} years; (B) Amortization method with monthly payments over {years} years.",
            "choices": choices,
            "solution": f"Amortization: ${round(amort_payment*12, 2):,.2f}/year. Sinking fund (at loan rate): ${sinking_payment:,.2f}/year.",
            "explanation": f"Sinking fund approach: pay only interest annually + deposit to sink fund. Amortization: make single payment covering both. Amortization typically has higher early payments."
        }

    def refinancing_loan(self) -> Dict:
        """Refinance: payoff old loan, take new loan with different terms"""
        old_loan = round(random.uniform(100000, 500000), 2)
        old_rate = round(random.uniform(0.03, 0.08), 4)
        old_total_periods = 360
        periods_elapsed = random.randint(12, 240)
        new_rate = round(random.uniform(0.01, 0.07), 4)
        new_periods = 360 - periods_elapsed

        old_periodic_rate = old_rate / 12
        # Old payment
        old_payment = round(old_loan * old_periodic_rate * (1 + old_periodic_rate) ** old_total_periods / ((1 + old_periodic_rate) ** old_total_periods - 1), 2)
        # Outstanding balance
        old_balance = round(old_payment * (1 - (1 + old_periodic_rate) ** (-new_periods)) / old_periodic_rate, 2)
        # New payment at new rate
        new_periodic_rate = new_rate / 12
        new_payment = round(old_balance * new_periodic_rate * (1 + new_periodic_rate) ** new_periods / ((1 + new_periodic_rate) ** new_periods - 1), 2)

        q_id = f"loan_refi_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${new_payment:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${old_payment:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(old_balance / new_periods, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(new_rate * old_balance / 12, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(old_balance * new_periodic_rate, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Loan Refinancing",
            "difficulty": 3,
            "question_text": f"A ${old_loan:,.2f} loan at {old_rate*100:.2f}% is being refinanced after {periods_elapsed} monthly payments. If refinanced at {new_rate*100:.2f}% for the remaining {new_periods} months, what is the new monthly payment?",
            "choices": choices,
            "solution": f"Outstanding balance after {periods_elapsed} payments ≈ ${old_balance:,.2f}. New payment over {new_periods} months at {new_rate*100:.2f}% = ${new_payment:,.2f}",
            "explanation": f"Step 1: Find balance on old loan. Step 2: Treat that balance as new principal, refinance at new rate for remaining term."
        }

    def loan_with_balloon_payment(self) -> Dict:
        """Loan with balloon payment: PMT covers part, balloon at end"""
        principal = round(random.uniform(100000, 500000), 2)
        balloon = round(principal * random.uniform(0.1, 0.3), 2)
        periodic_rate = round(random.uniform(0.002, 0.015), 6)
        periods = random.randint(60, 360)

        # L = PMT × a_n̄ + Balloon × (1+i)^-n
        # Solve for PMT: PMT = [L - Balloon × (1+i)^-n] / a_n̄
        pv_balloon = round(balloon / (1 + periodic_rate) ** periods, 2)
        annuity_factor = (1 - (1 + periodic_rate) ** (-periods)) / periodic_rate
        payment = round((principal - pv_balloon) / annuity_factor, 2)

        q_id = f"loan_balloon_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${payment:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round((principal - balloon) / periods, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(principal / periods, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round((principal + balloon) * periodic_rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round((principal - balloon) * periodic_rate / (1 - (1 + periodic_rate)**(-periods)), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Loan with Balloon Payment",
            "difficulty": 3,
            "question_text": f"A ${principal:,.2f} loan is repaid with equal payments for {periods} periods at {periodic_rate*100:.4f}% per period, with a balloon payment of ${balloon:,.2f} at the end. What is the periodic payment?",
            "choices": choices,
            "solution": f"L = PMT × a_n̄ + Balloon / (1+i)^n. PMT = [L - Balloon/(1+i)^n] / a_n̄ = [{principal:,.2f} - ${pv_balloon:,.2f}] / {annuity_factor:.6f} = ${payment:,.2f}",
            "explanation": f"PV of balloon payment is subtracted from loan, and the remainder is financed by equal payments."
        }

    def variable_rate_loan(self) -> Dict:
        """Loan with changing interest rates over time"""
        principal = round(random.uniform(50000, 300000), 2)
        periods_group1 = random.randint(12, 60)
        periods_group2 = random.randint(12, 60)
        rate1 = round(random.uniform(0.002, 0.01), 6)
        rate2 = round(random.uniform(0.002, 0.015), 6)

        total_periods = periods_group1 + periods_group2
        # Simplistic: calculate balance after period 1, then recompute payment
        balance_after_period1 = round(principal * (1 + rate1) ** periods_group1, 2)
        payment_period2 = round(balance_after_period1 * rate2 * (1 + rate2) ** periods_group2 / ((1 + rate2) ** periods_group2 - 1), 2)

        q_id = f"loan_variable_rate_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${payment_period2:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(principal / total_periods, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round((principal * (rate1 + rate2) / 2) * total_periods, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(balance_after_period1 / periods_group2, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(principal * rate1 * (1 + rate1)**periods_group1 / ((1+rate1)**periods_group1 - 1), 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Variable Rate Loan",
            "difficulty": 3,
            "question_text": f"A ${principal:,.2f} loan is structured as follows: {periods_group1} periods at {rate1*100:.4f}% per period, then {periods_group2} periods at {rate2*100:.4f}%. Compute the payment for the second {periods_group2} periods (assuming the balance carries over).",
            "choices": choices,
            "solution": f"Balance after {periods_group1} periods at {rate1*100:.4f}% = ${balance_after_period1:,.2f}. Payment for next {periods_group2} periods = ${payment_period2:,.2f}",
            "explanation": f"Variable rate loans: calculate balance at end of period 1, then refinance that balance at the new rate for the remaining periods."
        }

    def loan_total_interest_paid(self) -> Dict:
        """Total interest paid over life of loan"""
        principal = round(random.uniform(50000, 500000), 2)
        periodic_rate = round(random.uniform(0.002, 0.015), 6)
        periods = random.randint(60, 360)

        payment = round(principal * periodic_rate * (1 + periodic_rate) ** periods / ((1 + periodic_rate) ** periods - 1), 2)
        total_paid = round(payment * periods, 2)
        total_interest = round(total_paid - principal, 2)

        q_id = f"loan_total_interest_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${total_interest:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(principal * periodic_rate * periods, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${payment:,.2f}", "is_correct": False},
            {"label": "D", "text": f"${total_paid:,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(principal * periodic_rate, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Loans",
            "subtopic": "Total Interest Paid",
            "difficulty": 1,
            "question_text": f"A ${principal:,.2f} loan is repaid with {periods} equal monthly payments at {periodic_rate*100:.4f}% per month. What is the total interest paid over the life of the loan?",
            "choices": choices,
            "solution": f"Monthly payment = ${payment:,.2f}. Total paid = ${payment:,.2f} × {periods} = ${total_paid:,.2f}. Interest = ${total_paid:,.2f} - ${principal:,.2f} = ${total_interest:,.2f}",
            "explanation": f"Total interest = (Total paid) - (Principal). Or sum each month's interest portion from the amortization schedule."
        }

    # ===== TOPIC 4: BONDS (10+ methods) =====

    def bond_price_from_yield(self) -> Dict:
        """Bond pricing: P = Σ(C/(1+y)^t) + F/(1+y)^n"""
        par_value = round(random.uniform(1000, 10000), 2)
        coupon_rate = round(random.uniform(0.01, 0.10), 4)
        coupon_payment = round(par_value * coupon_rate, 2)
        years_to_maturity = random.randint(5, 30)
        yield_rate = round(random.uniform(0.01, 0.15), 4)

        # Price = sum of PV of coupons + PV of par
        pv_coupons = round(coupon_payment * (1 - (1 + yield_rate) ** (-years_to_maturity)) / yield_rate, 2)
        pv_par = round(par_value / (1 + yield_rate) ** years_to_maturity, 2)
        price = round(pv_coupons + pv_par, 2)

        q_id = f"bond_price_yield_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${price:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${par_value:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(pv_coupons, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(coupon_payment * years_to_maturity + par_value, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(par_value / (1 + coupon_rate)**years_to_maturity, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Bond Pricing from Yield",
            "difficulty": 2,
            "question_text": f"A bond with par value ${par_value:,.2f}, {coupon_rate*100:.2f}% coupon (paid annually), and {years_to_maturity} years to maturity is priced to yield {yield_rate*100:.2f}%. What is the bond price?",
            "choices": choices,
            "solution": f"Price = ${coupon_payment:,.2f} × a_{years_to_maturity}̄ + ${par_value:,.2f} / (1.{yield_rate:.4f})^{years_to_maturity} = ${pv_coupons:,.2f} + ${pv_par:,.2f} = ${price:,.2f}",
            "explanation": f"Bond price is PV of all coupons plus PV of par value, discounted at yield rate."
        }

    def bond_yield_approximation(self) -> Dict:
        """Approximate bond yield using mid-price formula"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(10, 150), 2)
        price = round(random.uniform(800, 1200), 2)
        years_to_maturity = random.randint(5, 30)

        # Approximate yield = [C + (F - P)/n] / [(F + P)/2]
        approx_yield = round((coupon_payment + (par_value - price) / years_to_maturity) / ((par_value + price) / 2), 4)

        q_id = f"bond_yield_approx_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{approx_yield*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{round(coupon_payment / price, 4)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{round((par_value - price) / years_to_maturity / price, 4)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round(coupon_payment / par_value, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round(math.log(par_value / price) / years_to_maturity, 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Bond Yield - Approximation",
            "difficulty": 2,
            "question_text": f"A bond with par ${par_value:,.2f}, coupon ${coupon_payment:,.2f}/year, {years_to_maturity} years to maturity, trading at ${price:,.2f}. Approximate the yield to maturity.",
            "choices": choices,
            "solution": f"Approx YTM = [C + (F-P)/n] / [(F+P)/2] = [{coupon_payment:,.2f} + ({par_value:,.2f}-{price:,.2f})/{years_to_maturity}] / [({par_value:,.2f}+{price:,.2f})/2] = {approx_yield*100:.4f}%",
            "explanation": f"Quick approximation for YTM without iteration. Actual YTM requires numerical solving."
        }

    def bond_premium_discount(self) -> Dict:
        """Bond trading at premium (price > par) or discount (price < par)"""
        par_value = 1000.0
        coupon_rate = round(random.uniform(0.01, 0.12), 4)
        coupon_payment = round(par_value * coupon_rate, 2)
        years_to_maturity = random.randint(5, 20)

        # Choose scenario: premium or discount
        scenario = random.choice(['premium', 'discount'])
        if scenario == 'premium':
            yield_rate = round(coupon_rate * random.uniform(0.5, 0.9), 4)
        else:
            yield_rate = round(coupon_rate * random.uniform(1.1, 2.0), 4)

        pv_coupons = round(coupon_payment * (1 - (1 + yield_rate) ** (-years_to_maturity)) / yield_rate, 2)
        pv_par = round(par_value / (1 + yield_rate) ** years_to_maturity, 2)
        price = round(pv_coupons + pv_par, 2)

        premium_discount = round(price - par_value, 2)
        pct_change = round((price - par_value) / par_value * 100, 2)

        q_id = f"bond_prem_disc_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${abs(premium_discount):,.2f} {'premium' if premium_discount > 0 else 'discount'}", "is_correct": True},
            {"label": "B", "text": f"${abs(premium_discount):,.2f} {'discount' if premium_discount > 0 else 'premium'}", "is_correct": False},
            {"label": "C", "text": f"${price:,.2f} premium", "is_correct": False},
            {"label": "D", "text": f"${coupon_payment * years_to_maturity:,.2f} premium", "is_correct": False},
            {"label": "E", "text": f"No premium or discount", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Bond Premium/Discount",
            "difficulty": 1,
            "question_text": f"A bond with par ${par_value:,.2f}, {coupon_rate*100:.2f}% coupon, {years_to_maturity} years to maturity is priced to yield {yield_rate*100:.2f}%. Is it trading at a premium or discount, and by how much?",
            "choices": choices,
            "solution": f"Coupon rate {coupon_rate*100:.2f}% vs Yield {yield_rate*100:.2f}%. Since {'coupon < yield' if coupon_rate < yield_rate else 'coupon > yield'}, bond trades at {'discount' if coupon_rate < yield_rate else 'premium'}. Price = ${price:,.2f}, so ${abs(premium_discount):,.2f} {'premium' if premium_discount > 0 else 'discount'}.",
            "explanation": f"Coupon rate < YTM → discount (sell below par). Coupon rate > YTM → premium (sell above par)."
        }

    def bond_amortization_schedule(self) -> Dict:
        """Bond amortization: Book value grows from purchase to par"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        purchase_price = round(random.uniform(800, 950), 2)
        years_to_maturity = random.randint(3, 15)

        # Implied yield (approximation for simplicity)
        ytm_approx = round((coupon_payment + (par_value - purchase_price) / years_to_maturity) / ((par_value + purchase_price) / 2), 6)

        # Year 1 book value increase
        interest_income = round(purchase_price * ytm_approx, 2)
        amortization = round(coupon_payment - interest_income, 2)
        book_value_year1 = round(purchase_price + amortization, 2)

        q_id = f"bond_amort_sched_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"Interest income: ${interest_income:,.2f}; Amortization: ${amortization:,.2f}; Book value end of year 1: ${book_value_year1:,.2f}", "is_correct": True},
            {"label": "B", "text": f"Interest income: ${coupon_payment:,.2f}; Amortization: $0; Book value end of year 1: ${purchase_price:,.2f}", "is_correct": False},
            {"label": "C", "text": f"Interest income: ${round(purchase_price * coupon_payment / par_value, 2):,.2f}; Amortization: ${round(coupon_payment - purchase_price * coupon_payment / par_value, 2):,.2f}; Book value: ${round(purchase_price + (par_value - purchase_price)/years_to_maturity, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"Interest income: ${round(purchase_price * ytm_approx, 2):,.2f}; Book value: ${par_value:,.2f}", "is_correct": False},
            {"label": "E", "text": f"Cannot determine without more information", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Bond Amortization Schedule",
            "difficulty": 2,
            "question_text": f"A bond with par ${par_value:,.2f}, {round(coupon_payment*100/par_value, 2)}% coupon, {years_to_maturity} years to maturity is purchased for ${purchase_price:,.2f}. Fill in Year 1: Interest income, Amortization of discount, and Book value at end of Year 1.",
            "choices": choices,
            "solution": f"YTM ≈ {ytm_approx*100:.4f}%. Interest income = ${purchase_price:,.2f} × {ytm_approx:.6f} = ${interest_income:,.2f}. Amortization = ${coupon_payment:,.2f} - ${interest_income:,.2f} = ${amortization:,.2f}. BV year-end = ${book_value_year1:,.2f}.",
            "explanation": f"Bond discount amortizes (increases) the book value each year. Interest income at YTM, coupon is cash; difference is amortization."
        }

    def callable_bond_price(self) -> Dict:
        """Price of callable bond: minimum of YTM price or call price"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        years_to_maturity = random.randint(5, 20)
        call_price = round(par_value * random.uniform(1.01, 1.05), 2)
        years_to_call = random.randint(2, min(10, years_to_maturity - 1))
        yield_rate = round(random.uniform(0.02, 0.15), 4)

        # Price to maturity
        pv_coupons_mat = round(coupon_payment * (1 - (1 + yield_rate) ** (-years_to_maturity)) / yield_rate, 2)
        pv_par_mat = round(par_value / (1 + yield_rate) ** years_to_maturity, 2)
        price_to_maturity = round(pv_coupons_mat + pv_par_mat, 2)

        # Price to call
        pv_coupons_call = round(coupon_payment * (1 - (1 + yield_rate) ** (-years_to_call)) / yield_rate, 2)
        pv_call_price = round(call_price / (1 + yield_rate) ** years_to_call, 2)
        price_to_call = round(pv_coupons_call + pv_call_price, 2)

        callable_price = min(price_to_maturity, price_to_call)

        q_id = f"bond_callable_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${callable_price:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${price_to_maturity:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${price_to_call:,.2f}", "is_correct": False},
            {"label": "D", "text": f"${call_price:,.2f}", "is_correct": False},
            {"label": "E", "text": f"${par_value:,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Callable Bond Pricing",
            "difficulty": 3,
            "question_text": f"A bond: par ${par_value:,.2f}, ${coupon_payment:,.2f} annual coupon, {years_to_maturity} years to maturity, callable at ${call_price:,.2f} after {years_to_call} years. YTM = {yield_rate*100:.2f}%. What is the bond price?",
            "choices": choices,
            "solution": f"Price to maturity = ${price_to_maturity:,.2f}. Price to call = ${price_to_call:,.2f}. Callable bond price = min(${price_to_maturity:,.2f}, ${price_to_call:,.2f}) = ${callable_price:,.2f}",
            "explanation": f"Callable bond price is the minimum of price-to-maturity and price-to-call. Issuer will call if bond trades above call price."
        }

    def par_value_bond(self) -> Dict:
        """Bond trading at par: coupon rate = yield rate"""
        par_value = 1000.0
        rate = round(random.uniform(0.02, 0.10), 4)
        coupon_payment = round(par_value * rate, 2)
        years_to_maturity = random.randint(5, 20)

        # Coupon rate = yield rate, so price = par
        price = par_value

        q_id = f"bond_par_value_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${price:,.2f} (trading at par)", "is_correct": True},
            {"label": "B", "text": f"${round(coupon_payment * years_to_maturity, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${coupon_payment:,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(par_value / (1 + rate)**years_to_maturity, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"Cannot determine", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Par Value Bond",
            "difficulty": 1,
            "question_text": f"A bond has par ${par_value:,.2f}, {rate*100:.2f}% coupon (${coupon_payment:,.2f}/year), and {years_to_maturity} years to maturity. If the YTM is also {rate*100:.2f}%, at what price does it trade?",
            "choices": choices,
            "solution": f"When coupon rate = yield rate, bond trades at par value = ${par_value:,.2f}.",
            "explanation": f"Par value bonds: coupon rate = YTM. All periods: coupon gives {rate*100:.2f}% return, plus capital return = 0 since price = par always."
        }

    def bond_price_between_coupons(self) -> Dict:
        """Dirty vs clean price: price between coupon dates"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        yield_rate = round(random.uniform(0.02, 0.12), 4)
        years_to_maturity = random.randint(3, 20)
        months_since_coupon = random.randint(1, 11)  # 1-11 months into coupon period

        # Price at last coupon date
        pv_coupons = round(coupon_payment * (1 - (1 + yield_rate) ** (-years_to_maturity)) / yield_rate, 2)
        pv_par = round(par_value / (1 + yield_rate) ** years_to_maturity, 2)
        clean_price = round(pv_coupons + pv_par, 2)

        # Accrue interest for time since last coupon
        fraction_period = months_since_coupon / 12
        accrued_interest = round(coupon_payment * fraction_period, 2)
        dirty_price = round(clean_price + accrued_interest, 2)

        q_id = f"bond_dirty_clean_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"Clean price: ${clean_price:,.2f}; Dirty price: ${dirty_price:,.2f}; Accrued: ${accrued_interest:,.2f}", "is_correct": True},
            {"label": "B", "text": f"Clean price: ${dirty_price:,.2f}; Dirty price: ${clean_price:,.2f}", "is_correct": False},
            {"label": "C", "text": f"All prices equal ${clean_price:,.2f}", "is_correct": False},
            {"label": "D", "text": f"Clean price: ${clean_price:,.2f}; Accrued interest: $0", "is_correct": False},
            {"label": "E", "text": f"Cannot compute without annual yield", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Bond Price Between Coupons",
            "difficulty": 2,
            "question_text": f"A bond trades between coupon dates, {months_since_coupon} months after the last coupon. Par ${par_value:,.2f}, ${coupon_payment:,.2f} annual coupon, {years_to_maturity} years to maturity, YTM {yield_rate*100:.2f}%. Find clean price, dirty price, and accrued interest.",
            "choices": choices,
            "solution": f"Clean price = ${clean_price:,.2f}. Accrued interest = ${coupon_payment:,.2f} × {fraction_period:.4f} = ${accrued_interest:,.2f}. Dirty price = ${dirty_price:,.2f}.",
            "explanation": f"Clean price ignores accrued coupon; dirty price includes it. Buyer pays dirty price, seller receives accrued interest compensation."
        }

    def zero_coupon_bond(self) -> Dict:
        """Zero-coupon bond: P = F / (1+y)^n"""
        par_value = 1000.0
        years_to_maturity = random.randint(5, 30)
        yield_rate = round(random.uniform(0.02, 0.12), 4)

        price = round(par_value / (1 + yield_rate) ** years_to_maturity, 2)

        q_id = f"bond_zero_coupon_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${price:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${par_value:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(par_value * (1 + yield_rate)**years_to_maturity, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(par_value / years_to_maturity, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(par_value * yield_rate * years_to_maturity, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Zero-Coupon Bond",
            "difficulty": 1,
            "question_text": f"A zero-coupon bond has par ${par_value:,.2f} and matures in {years_to_maturity} years. If the YTM is {yield_rate*100:.2f}%, what is its price?",
            "choices": choices,
            "solution": f"Price = F / (1+y)^n = ${par_value:,.2f} / (1 + {yield_rate:.4f})^{years_to_maturity} = ${price:,.2f}",
            "explanation": f"Zero-coupon bonds have no coupon payments, only return par value at maturity. Price is simply the discounted par value."
        }

    def serial_bonds(self) -> Dict:
        """Serial bonds: different tranches mature at different times"""
        total_par = 10000.0
        par_per_tranche = total_par / 5
        coupon_rate = round(random.uniform(0.02, 0.08), 4)
        coupon_per_bond = round(par_per_tranche * coupon_rate, 2)
        yield_rate = round(random.uniform(0.01, 0.12), 4)

        # 5 tranches maturing in years 1, 2, 3, 4, 5
        total_price = 0
        for year in range(1, 6):
            pv_coupons = round(coupon_per_bond * (1 - (1 + yield_rate) ** (-year)) / yield_rate, 2)
            pv_par = round(par_per_bond / (1 + yield_rate) ** year, 2)
            tranche_price = pv_coupons + pv_par
            total_price += tranche_price

        total_price = round(total_price, 2)

        q_id = f"bond_serial_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${total_price:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${total_par:,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(total_par + coupon_per_bond * (1+2+3+4+5), 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(total_par / (1 + yield_rate)**3, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(total_par * (1 + coupon_rate)**2.5, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Serial Bonds",
            "difficulty": 3,
            "question_text": f"${total_par:,.2f} of serial bonds with {coupon_rate*100:.2f}% coupon rate are issued. Five equal tranches mature in years 1-5. YTM = {yield_rate*100:.2f}%. Find total price for all tranches.",
            "choices": choices,
            "solution": f"Price each tranche separately: Tranche 1 (1-year) at ${round(coupon_per_bond + par_per_bond / (1+yield_rate), 2):,.2f}, ..., Tranche 5 (5-year). Sum = ${total_price:,.2f}.",
            "explanation": f"Serial bonds: different maturities. Price each tranche individually, then sum."
        }

    def bond_duration_calculation(self) -> Dict:
        """Macaulay duration of a bond"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        years_to_maturity = random.randint(3, 15)
        yield_rate = round(random.uniform(0.01, 0.12), 4)

        # Simplified: Macaulay D ≈ (1+y)/y - (1+y+n(c-y))/[c((1+y)^n - 1) + y]
        # Easier: compute as weighted average of cash flow timings
        cf_pv_sum = 0
        pv_sum = 0
        weighted_time = 0

        for t in range(1, years_to_maturity + 1):
            if t < years_to_maturity:
                cf = coupon_payment
            else:
                cf = coupon_payment + par_value

            pv_cf = cf / (1 + yield_rate) ** t
            cf_pv_sum += pv_cf
            weighted_time += t * pv_cf

        duration = round(weighted_time / cf_pv_sum, 2)

        q_id = f"bond_duration_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{duration:.2f} years", "is_correct": True},
            {"label": "B", "text": f"{years_to_maturity:.2f} years", "is_correct": False},
            {"label": "C", "text": f"{round(years_to_maturity / 2, 2):.2f} years", "is_correct": False},
            {"label": "D", "text": f"{round((1 + yield_rate) / yield_rate, 2):.2f} years", "is_correct": False},
            {"label": "E", "text": f"{round(years_to_maturity * coupon_payment / par_value, 2):.2f} years", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Bonds",
            "subtopic": "Bond Duration",
            "difficulty": 3,
            "question_text": f"Bond: par ${par_value:,.2f}, ${coupon_payment:,.2f} annual coupon, {years_to_maturity} years to maturity, YTM {yield_rate*100:.2f}%. Find Macaulay duration.",
            "choices": choices,
            "solution": f"Duration = Σ(t × PV(CF_t)) / Σ(PV(CF_t)) ≈ {duration:.2f} years",
            "explanation": f"Macaulay duration is the weighted average time to receive cash flows. Duration < maturity for coupon bonds; = maturity for zero-coupon."
        }

    # ===== TOPIC 5: TERM STRUCTURE & RATES (8+ methods) =====

    def spot_rate_from_bond_prices(self) -> Dict:
        """Extract spot rates from par bond prices"""
        par = 100.0
        rate_1y = round(random.uniform(0.01, 0.08), 4)
        rate_2y = round(random.uniform(rate_1y, 0.12), 4)

        # 1-year zero: price = 100 / (1 + s_1)
        price_1y = round(par / (1 + rate_1y), 2)

        # 2-year coupon bond at par with 2-year spot rates
        # For simplicity, assume 2-year bond paying coupons = 2-year spot rate
        coupon_2y = rate_2y * par
        price_2y = round(coupon_2y / (1 + rate_1y) + (par + coupon_2y) / (1 + rate_2y) ** 2, 2)

        q_id = f"term_spot_rates_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"1-year: {rate_1y*100:.4f}%; 2-year: {rate_2y*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"1-year: {rate_2y*100:.4f}%; 2-year: {rate_1y*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"1-year: {round((rate_1y + rate_2y)/2, 4)*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"All rates: {round((price_1y + price_2y) / 2 / par, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"Cannot determine from given information", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Spot Rates from Bond Prices",
            "difficulty": 3,
            "question_text": f"Given: 1-year zero-coupon bond price ${price_1y:,.2f}; 2-year coupon bond at par with {rate_2y*100:.2f}% coupon trading at ${price_2y:,.2f}. Extract 1-year and 2-year spot rates.",
            "choices": choices,
            "solution": f"s_1 from zero-coupon: {price_1y:,.2f} = 100/(1+s_1) → s_1 ≈ {rate_1y*100:.4f}%. s_2 from coupon bond: {price_2y:,.2f} = {coupon_2y:.2f}/(1+s_1) + {par+coupon_2y:,.2f}/(1+s_2)^2 → s_2 ≈ {rate_2y*100:.4f}%",
            "explanation": f"Bootstrapping: use zero-coupon bonds or par bonds to extract spot rates sequentially."
        }

    def forward_rate_from_spots(self) -> Dict:
        """Calculate forward rate from two spot rates: f_{1,1} = [(1+s_2)^2 / (1+s_1)] - 1"""
        s1 = round(random.uniform(0.01, 0.06), 4)
        s2 = round(random.uniform(s1, 0.10), 4)

        # 1-year forward rate 1 year from now
        forward_rate = round(((1 + s2) ** 2 / (1 + s1)) - 1, 4)

        q_id = f"term_forward_rate_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{forward_rate*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{s2*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{s1*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round((s1 + s2) / 2, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round(2 * s2 - s1, 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Forward Rate from Spot Rates",
            "difficulty": 2,
            "question_text": f"Given 1-year spot rate s_1 = {s1*100:.4f}% and 2-year spot rate s_2 = {s2*100:.4f}%, find the 1-year forward rate 1 year from now.",
            "choices": choices,
            "solution": f"f_{{1,1}} = [(1 + {s2:.4f})^2 / (1 + {s1:.4f})] - 1 = {forward_rate*100:.4f}%",
            "explanation": f"Forward rate relates future yields to current spot rates. (1+s_2)^2 = (1+s_1) × (1+f_{{1,1}})."
        }

    def forward_rate_agreement_value(self) -> Dict:
        """Value of FRA: gain/loss on interest rate change"""
        contract_notional = round(random.uniform(100000, 1000000), 2)
        contract_rate = round(random.uniform(0.01, 0.08), 4)
        current_forward_rate = round(random.uniform(0.01, 0.12), 4)
        payment_period_fraction = round(random.uniform(0.25, 0.5), 2)

        # FRA value = Notional × (f_actual - f_contract) × time fraction / (1 + f_actual × time)
        fra_value = round(contract_notional * (current_forward_rate - contract_rate) * payment_period_fraction / (1 + current_forward_rate * payment_period_fraction), 2)

        q_id = f"term_fra_value_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${fra_value:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(contract_notional * (current_forward_rate - contract_rate), 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${round(contract_notional * contract_rate * payment_period_fraction, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round((current_forward_rate - contract_rate) * contract_notional * payment_period_fraction, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"$0 (FRAs have no value until settlement)", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Forward Rate Agreement Value",
            "difficulty": 3,
            "question_text": f"FRA: Notional ${contract_notional:,.2f}, contract rate {contract_rate*100:.4f}%, payment period {payment_period_fraction*12:.0f} months. Current forward rate = {current_forward_rate*100:.4f}%. Find FRA value (party receiving fixed).",
            "choices": choices,
            "solution": f"FRA value = {contract_notional:,.2f} × ({current_forward_rate:.4f} - {contract_rate:.4f}) × {payment_period_fraction:.2f} / (1 + {current_forward_rate:.4f} × {payment_period_fraction:.2f}) = ${fra_value:,.2f}",
            "explanation": f"If actual forward > contract: receiver of fixed gains (positive value). Discounted by (1 + forward rate × fraction)."
        }

    def yield_curve_bootstrapping(self) -> Dict:
        """Bootstrap spot rates from treasury bond prices"""
        prices = [round(random.uniform(95, 100), 2) for _ in range(3)]
        par = 100.0

        # 1-year: par bond at given price → s_1
        s1 = round((par / prices[0]) - 1, 4)

        # 2-year: coupon bond at given price
        # Assume 2-year coupon = 3% → price = 3/(1+s_1) + 103/(1+s_2)^2
        coupon_2y = 3.0
        temp = (par + coupon_2y) / prices[1] - coupon_2y / (1 + s1)
        s2 = round((temp ** (1/2)) - 1, 4)

        # 3-year similarly
        coupon_3y = 3.5
        temp = (par + coupon_3y) / prices[2] - coupon_3y / (1 + s1) - coupon_3y / (1 + s2) ** 2
        s3 = round((temp ** (1/3)) - 1, 4)

        q_id = f"term_bootstrap_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"s_1 = {s1*100:.4f}%; s_2 = {s2*100:.4f}%; s_3 = {s3*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"All equal {round((s1+s2+s3)/3, 4)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"s_1 = {s2*100:.4f}%; s_2 = {s3*100:.4f}%; s_3 = {s1*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"Cannot determine from prices alone", "is_correct": False},
            {"label": "E", "text": f"s_1 = {round(3/prices[0], 4)*100:.4f}%; s_2 = {round(3/prices[1], 4)*100:.4f}%; s_3 = {round(3.5/prices[2], 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Yield Curve Bootstrapping",
            "difficulty": 3,
            "question_text": f"Treasury prices: 1-yr ${prices[0]:,.2f}, 2-yr ${prices[1]:,.2f} (3% coupon), 3-yr ${prices[2]:,.2f} (3.5% coupon). Bootstrap spot rates.",
            "choices": choices,
            "solution": f"s_1 = (100/{prices[0]:.2f}) - 1 = {s1*100:.4f}%. Then solve s_2, s_3 sequentially.",
            "explanation": f"Bootstrapping: use known spot rates to solve for future ones. 1-year is easy (zero-coupon); 2-year uses s_1 to solve s_2, etc."
        }

    def par_yield_curve(self) -> Dict:
        """Par yield: coupon rate where bond trades at par"""
        years = random.randint(2, 10)
        spot_rates = [round(random.uniform(0.01, 0.08), 4) for _ in range(years)]

        # Par yield: c where P = Σ(c/(1+s_t)^t) + 100/(1+s_years)^years = 100
        # So: c × Σ(1/(1+s_t)^t) = 100 - 100/(1+s_years)^years
        pv_factor_sum = sum(1 / (1 + spot_rates[i]) ** (i + 1) for i in range(years))
        pv_par = 100 / (1 + spot_rates[-1]) ** years
        par_yield = round((100 - pv_par) / pv_factor_sum, 4)

        q_id = f"term_par_yield_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{par_yield*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{round((sum(spot_rates) / years), 4)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{spot_rates[-1]*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{spot_rates[0]*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round(100 / pv_factor_sum / years, 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Par Yield Curve",
            "difficulty": 3,
            "question_text": f"Spot rate curve for {years} years: {', '.join([f's_{i+1}={spot_rates[i]*100:.2f}%' for i in range(min(3, years))])} ... Find the {years}-year par yield.",
            "choices": choices,
            "solution": f"Par yield c: PV of coupons + PV of par = 100. c × Σ(PV factors) = 100 - PV(par) → c = {par_yield*100:.4f}%",
            "explanation": f"Par yield is the coupon rate such that a bond with those spot rates trades at par."
        }

    def swap_rate_calculation(self) -> Dict:
        """Plain vanilla swap rate: fixed rate where PV fixed = PV floating"""
        notional = round(random.uniform(1000000, 10000000), 2)
        spot_rates = [round(random.uniform(0.01, 0.08), 4) for _ in range(5)]

        # Swap rate: s where fixed PV = 100 (par)
        # s × Σ(DF_t) = 100, where DF_t = 1/(1+s_t)^t
        df_sum = sum(1 / (1 + spot_rates[i]) ** (i + 1) for i in range(5))
        swap_rate = round(1.0 / df_sum - 1, 4)

        q_id = f"term_swap_rate_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{swap_rate*100:.4f}%", "is_correct": True},
            {"label": "B", "text": f"{round(sum(spot_rates) / 5, 4)*100:.4f}%", "is_correct": False},
            {"label": "C", "text": f"{spot_rates[-1]*100:.4f}%", "is_correct": False},
            {"label": "D", "text": f"{round(1 / df_sum, 4)*100:.4f}%", "is_correct": False},
            {"label": "E", "text": f"{round((spot_rates[0] + spot_rates[-1])/2, 4)*100:.4f}%", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Swap Rate Calculation",
            "difficulty": 3,
            "question_text": f"5-year plain vanilla interest rate swap. Spot rates: s_1={spot_rates[0]*100:.2f}%, s_2={spot_rates[1]*100:.2f}%, ..., s_5={spot_rates[-1]*100:.2f}%. Find the swap rate.",
            "choices": choices,
            "solution": f"Swap rate where PV of fixed = PV of par. Σ(DF) = {df_sum:.6f}. Swap rate = 1/Σ(DF) - 1 ≈ {swap_rate*100:.4f}%",
            "explanation": f"Plain vanilla swap: receiver of fixed benefits if forward rates rise above swap rate."
        }

    def interest_rate_swap_value(self) -> Dict:
        """Valuation of swap after inception"""
        notional = 1000000.0
        swap_rate = round(random.uniform(0.01, 0.08), 4)
        current_spot_rates = [round(random.uniform(0.01, 0.10), 4) for _ in range(3)]
        years_elapsed = random.randint(1, 2)

        # Value to fixed-rate payer: (spot rate - swap rate) × notional × PV of annuity
        df_sum = sum(1 / (1 + current_spot_rates[i]) ** (i + 1) for i in range(3))
        swap_value = round((current_spot_rates[0] - swap_rate) * notional * df_sum, 2)

        q_id = f"term_swap_value_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${swap_value:,.2f}", "is_correct": True},
            {"label": "B", "text": f"$0 (swaps start at zero value)", "is_correct": False},
            {"label": "C", "text": f"${round((swap_rate - current_spot_rates[0]) * notional, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(notional * sum(current_spot_rates) / 3, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"Cannot determine without more information", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Interest Rate Swap Valuation",
            "difficulty": 3,
            "question_text": f"3-year IRS: notional ${notional:,.0f}, fixed rate (swap rate) {swap_rate*100:.4f}%. Current spots: {current_spot_rates[0]*100:.2f}%, {current_spot_rates[1]*100:.2f}%, {current_spot_rates[2]*100:.2f}%. Value to fixed payer?",
            "choices": choices,
            "solution": f"Value = (s - swap_rate) × Notional × PV(annuity) = ({current_spot_rates[0]:.4f} - {swap_rate:.4f}) × ${notional:,.0f} × {df_sum:.6f} = ${swap_value:,.2f}",
            "explanation": f"If current spot rises above swap rate, fixed-rate payer gains (positive value)."
        }

    def floating_vs_fixed_comparison(self) -> Dict:
        """Compare floating-rate vs fixed-rate borrowing"""
        principal = round(random.uniform(100000, 1000000), 2)
        fixed_rate = round(random.uniform(0.02, 0.08), 4)
        spread = round(random.uniform(0.001, 0.02), 4)
        floating_index = round(random.uniform(0.01, 0.07), 4)
        years = random.randint(3, 10)

        floating_rate = floating_index + spread
        fixed_annual_cost = round(principal * fixed_rate, 2)
        floating_annual_cost = round(principal * floating_rate, 2)
        savings = round(fixed_annual_cost - floating_annual_cost, 2) if floating_rate < fixed_rate else -abs(round(fixed_annual_cost - floating_annual_cost, 2))

        q_id = f"term_float_vs_fixed_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"Fixed: ${fixed_annual_cost:,.2f}/yr; Floating: ${floating_annual_cost:,.2f}/yr. {'Fixed is cheaper' if fixed_rate < floating_rate else 'Floating is cheaper'} by ${abs(savings):,.2f}/yr.", "is_correct": True},
            {"label": "B", "text": f"Fixed: ${fixed_annual_cost:,.2f}/yr; Floating: ${round(principal * floating_index, 2):,.2f}/yr", "is_correct": False},
            {"label": "C", "text": f"Both cost the same", "is_correct": False},
            {"label": "D", "text": f"Floating always cheaper", "is_correct": False},
            {"label": "E", "text": f"Cannot compare without knowing future rates", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Term Structure",
            "subtopic": "Floating vs Fixed Rate Comparison",
            "difficulty": 2,
            "question_text": f"Borrowing ${principal:,.2f}: (A) Fixed {fixed_rate*100:.4f}%/year; (B) Floating LIBOR+{spread*100:.2f}% where LIBOR={floating_index*100:.2f}%. Compare annual costs.",
            "choices": choices,
            "solution": f"Fixed annual = ${fixed_annual_cost:,.2f}. Floating annual = ${floating_annual_cost:,.2f}. Difference = ${abs(savings):,.2f}.",
            "explanation": f"Fixed protects against rate increases; floating benefits if rates fall. Compare fixed rate vs (index + spread)."
        }

    # ===== TOPIC 6: DURATION & CONVEXITY (7+ methods) =====

    def macaulay_duration(self) -> Dict:
        """Macaulay duration: weighted average time to cash flows"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        years_to_maturity = random.randint(3, 15)
        yield_rate = round(random.uniform(0.01, 0.12), 4)

        weighted_time = 0
        pv_sum = 0

        for t in range(1, years_to_maturity + 1):
            if t < years_to_maturity:
                cf = coupon_payment
            else:
                cf = coupon_payment + par_value

            pv_cf = cf / (1 + yield_rate) ** t
            pv_sum += pv_cf
            weighted_time += t * pv_cf

        macaulay_d = round(weighted_time / pv_sum, 2)

        q_id = f"dur_macaulay_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{macaulay_d:.2f} years", "is_correct": True},
            {"label": "B", "text": f"{years_to_maturity:.2f} years", "is_correct": False},
            {"label": "C", "text": f"{round(years_to_maturity / 2, 2):.2f} years", "is_correct": False},
            {"label": "D", "text": f"{round(coupon_payment / yield_rate, 2):.2f} years", "is_correct": False},
            {"label": "E", "text": f"{round(pv_sum / 1000, 2):.2f} years", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Macaulay Duration",
            "difficulty": 2,
            "question_text": f"Bond: par ${par_value:,.2f}, ${coupon_payment:,.2f} annual coupon, {years_to_maturity} years to maturity, YTM {yield_rate*100:.2f}%. Find Macaulay duration.",
            "choices": choices,
            "solution": f"D_Mac = Σ(t × PV(CF_t)) / Price = {weighted_time:,.2f} / {pv_sum:,.2f} = {macaulay_d:.2f} years",
            "explanation": f"Macaulay duration is weighted average time to receive cash flows, weighted by present value."
        }

    def modified_duration(self) -> Dict:
        """Modified duration: D* = D_Mac / (1 + y)"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        years_to_maturity = random.randint(3, 15)
        yield_rate = round(random.uniform(0.01, 0.12), 4)

        weighted_time = 0
        pv_sum = 0

        for t in range(1, years_to_maturity + 1):
            if t < years_to_maturity:
                cf = coupon_payment
            else:
                cf = coupon_payment + par_value

            pv_cf = cf / (1 + yield_rate) ** t
            pv_sum += pv_cf
            weighted_time += t * pv_cf

        macaulay_d = weighted_time / pv_sum
        modified_d = round(macaulay_d / (1 + yield_rate), 2)

        q_id = f"dur_modified_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{modified_d:.2f}", "is_correct": True},
            {"label": "B", "text": f"{round(macaulay_d, 2):.2f}", "is_correct": False},
            {"label": "C", "text": f"{round(macaulay_d * (1 + yield_rate), 2):.2f}", "is_correct": False},
            {"label": "D", "text": f"{round(yield_rate * 100, 2):.2f}", "is_correct": False},
            {"label": "E", "text": f"{round(macaulay_d - yield_rate, 2):.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Modified Duration",
            "difficulty": 2,
            "question_text": f"Bond Macaulay duration = {round(macaulay_d, 2):.2f} years, YTM = {yield_rate*100:.2f}%. Find modified duration.",
            "choices": choices,
            "solution": f"D* = D_Mac / (1 + y) = {round(macaulay_d, 2):.2f} / (1 + {yield_rate:.4f}) = {modified_d:.2f}",
            "explanation": f"Modified duration adjusts Macaulay for the yield. D* ≈ % change in price per 1% change in yield."
        }

    def effective_duration(self) -> Dict:
        """Effective duration: ΔP / (P × Δy × 2)"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        years_to_maturity = random.randint(3, 15)
        base_yield = round(random.uniform(0.01, 0.12), 4)

        # Price at base yield
        pv_coupons = round(coupon_payment * (1 - (1 + base_yield) ** (-years_to_maturity)) / base_yield, 2)
        pv_par = round(par_value / (1 + base_yield) ** years_to_maturity, 2)
        price_base = pv_coupons + pv_par

        # Price at yield ± 1%
        dy = 0.01
        pv_coupons_up = coupon_payment * (1 - (1 + base_yield + dy) ** (-years_to_maturity)) / (base_yield + dy)
        pv_par_up = par_value / (1 + base_yield + dy) ** years_to_maturity
        price_up = pv_coupons_up + pv_par_up

        pv_coupons_dn = coupon_payment * (1 - (1 + base_yield - dy) ** (-years_to_maturity)) / (base_yield - dy)
        pv_par_dn = par_value / (1 + base_yield - dy) ** years_to_maturity
        price_dn = pv_coupons_dn + pv_par_dn

        effective_d = round((price_dn - price_up) / (price_base * 2 * dy), 2)

        q_id = f"dur_effective_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{effective_d:.2f}", "is_correct": True},
            {"label": "B", "text": f"{round((price_up - price_dn) / price_base / dy, 2):.2f}", "is_correct": False},
            {"label": "C", "text": f"{round((price_base - price_up) / (price_base * dy), 2):.2f}", "is_correct": False},
            {"label": "D", "text": f"{round(years_to_maturity / 2, 2):.2f}", "is_correct": False},
            {"label": "E", "text": f"{round(price_dn / price_base, 2):.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Effective Duration",
            "difficulty": 3,
            "question_text": f"Bond: par ${par_value:,.2f}, coupon ${coupon_payment:,.2f}, {years_to_maturity} yrs, YTM {base_yield*100:.2f}%. Price at YTM-1% = ${round(price_dn, 2):,.2f}; at YTM+1% = ${round(price_up, 2):,.2f}; current = ${price_base:,.2f}. Find effective duration.",
            "choices": choices,
            "solution": f"Eff D = (P_down - P_up) / (P × 2 × Δy) = ({round(price_dn, 2):.2f} - {round(price_up, 2):.2f}) / ({price_base:,.2f} × 2 × 0.01) = {effective_d:.2f}",
            "explanation": f"Effective duration captures price sensitivity to yield changes empirically, without assuming linearity."
        }

    def dollar_duration(self) -> Dict:
        """Dollar duration: D$ = D* × P × denominator (basis points)"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        years_to_maturity = random.randint(3, 15)
        yield_rate = round(random.uniform(0.01, 0.12), 4)

        pv_coupons = round(coupon_payment * (1 - (1 + yield_rate) ** (-years_to_maturity)) / yield_rate, 2)
        pv_par = round(par_value / (1 + yield_rate) ** years_to_maturity, 2)
        price = pv_coupons + pv_par

        weighted_time = sum((i + 1) * (coupon_payment if i < years_to_maturity - 1 else coupon_payment + par_value) / (1 + yield_rate) ** (i + 1) for i in range(years_to_maturity))
        macaulay_d = weighted_time / price
        modified_d = macaulay_d / (1 + yield_rate)

        dollar_duration = round(modified_d * price, 2)

        q_id = f"dur_dollar_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"${dollar_duration:,.2f}", "is_correct": True},
            {"label": "B", "text": f"${round(modified_d * par_value, 2):,.2f}", "is_correct": False},
            {"label": "C", "text": f"${price:,.2f}", "is_correct": False},
            {"label": "D", "text": f"${round(price * yield_rate, 2):,.2f}", "is_correct": False},
            {"label": "E", "text": f"${round(modified_d, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Dollar Duration",
            "difficulty": 2,
            "question_text": f"Bond price: ${price:,.2f}, modified duration: {round(modified_d, 2):.2f}. Find dollar duration (price change per 1 basis point yield move).",
            "choices": choices,
            "solution": f"D$ = D* × Price = {round(modified_d, 2):.2f} × ${price:,.2f} = ${dollar_duration:,.2f} per basis point",
            "explanation": f"Dollar duration shows dollar change in price for 1 basis point yield move. Dollar duration = Modified duration × Price."
        }

    def convexity_calculation(self) -> Dict:
        """Bond convexity: second derivative of price w.r.t. yield"""
        par_value = 1000.0
        coupon_payment = round(random.uniform(20, 100), 2)
        years_to_maturity = random.randint(3, 15)
        yield_rate = round(random.uniform(0.01, 0.12), 4)

        # Convexity = Σ[t(t+1) × CF_t / (1+y)^(t+2)] / Price
        convexity_numerator = 0
        pv_sum = 0

        for t in range(1, years_to_maturity + 1):
            if t < years_to_maturity:
                cf = coupon_payment
            else:
                cf = coupon_payment + par_value

            pv_cf = cf / (1 + yield_rate) ** t
            pv_sum += pv_cf
            convexity_numerator += t * (t + 1) * cf / (1 + yield_rate) ** (t + 2)

        convexity = round(convexity_numerator / pv_sum / ((1 + yield_rate) ** 2), 4)

        q_id = f"dur_convexity_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{convexity:.4f}", "is_correct": True},
            {"label": "B", "text": f"{round(years_to_maturity * (years_to_maturity + 1) / 2, 4):.4f}", "is_correct": False},
            {"label": "C", "text": f"{round(coupon_payment / yield_rate, 4):.4f}", "is_correct": False},
            {"label": "D", "text": f"{round(1 / yield_rate, 4):.4f}", "is_correct": False},
            {"label": "E", "text": f"{round(yield_rate ** 2, 4):.4f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Convexity Calculation",
            "difficulty": 3,
            "question_text": f"Bond: par ${par_value:,.2f}, ${coupon_payment:,.2f} coupon, {years_to_maturity} years, YTM {yield_rate*100:.2f}%. Calculate convexity.",
            "choices": choices,
            "solution": f"Convexity = Σ[t(t+1)×CF_t/(1+y)^(t+2)] / (Price × (1+y)^2) ≈ {convexity:.4f}",
            "explanation": f"Convexity measures curvature of price-yield relationship. Positive convexity = beneficial to bondholder."
        }

    def price_change_estimate_duration(self) -> Dict:
        """Estimate price change using duration: ΔP ≈ -D* × P × Δy"""
        price = round(random.uniform(900, 1100), 2)
        modified_d = round(random.uniform(3, 10), 2)
        yield_change = round(random.uniform(-0.02, 0.02), 4)

        price_change = round(-modified_d * price * yield_change, 2)
        new_price = round(price + price_change, 2)

        q_id = f"dur_price_change_1_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"Price change: ${price_change:,.2f}; New price: ${new_price:,.2f}", "is_correct": True},
            {"label": "B", "text": f"Price change: ${-price_change:,.2f}; New price: ${price - price_change:,.2f}", "is_correct": False},
            {"label": "C", "text": f"Price change: ${round(price * yield_change, 2):,.2f}", "is_correct": False},
            {"label": "D", "text": f"Price change: $0 (no change)", "is_correct": False},
            {"label": "E", "text": f"Price change: ${round(modified_d * yield_change, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Price Change Estimate - Duration",
            "difficulty": 1,
            "question_text": f"Bond price ${price:,.2f}, modified duration {modified_d:.2f}, yield changes by {yield_change*100:+.2f}%. Estimate price change using duration.",
            "choices": choices,
            "solution": f"ΔP ≈ -D* × P × Δy = -{modified_d:.2f} × ${price:,.2f} × {yield_change:.4f} = ${price_change:,.2f}. New price ≈ ${new_price:,.2f}",
            "explanation": f"Duration approximation (linear): price change = -modified duration × price × yield change."
        }

    def price_change_duration_convexity(self) -> Dict:
        """Estimate price change using duration + convexity: ΔP ≈ -D*×P×Δy + 0.5×Convexity×P×(Δy)²"""
        price = round(random.uniform(900, 1100), 2)
        modified_d = round(random.uniform(3, 10), 2)
        convexity = round(random.uniform(50, 150), 2)
        yield_change = round(random.uniform(-0.03, 0.03), 4)

        duration_effect = round(-modified_d * price * yield_change, 2)
        convexity_effect = round(0.5 * convexity * price * (yield_change ** 2), 2)
        total_change = round(duration_effect + convexity_effect, 2)
        new_price = round(price + total_change, 2)

        q_id = f"dur_price_change_2_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"Duration effect: ${duration_effect:,.2f}; Convexity: ${convexity_effect:,.2f}; Total: ${total_change:,.2f}", "is_correct": True},
            {"label": "B", "text": f"Total change: ${duration_effect:,.2f} (convexity ignored)", "is_correct": False},
            {"label": "C", "text": f"Total change: ${convexity_effect:,.2f} (duration ignored)", "is_correct": False},
            {"label": "D", "text": f"Total change: $0", "is_correct": False},
            {"label": "E", "text": f"Total change: ${round(duration_effect - convexity_effect, 2):,.2f}", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Price Change - Duration & Convexity",
            "difficulty": 2,
            "question_text": f"Bond: price ${price:,.2f}, modified duration {modified_d:.2f}, convexity {convexity:.2f}, yield Δ = {yield_change*100:+.2f}%. Estimate ΔP with duration & convexity.",
            "choices": choices,
            "solution": f"ΔP ≈ -D*×P×Δy + 0.5×C×P×(Δy)² = ${duration_effect:,.2f} + ${convexity_effect:,.2f} = ${total_change:,.2f}",
            "explanation": f"Duration estimates linear price change; convexity adds quadratic (curvature) correction. Convexity effect is always positive."
        }

    def immunization_condition(self) -> Dict:
        """Immunization: duration of liabilities = duration of assets"""
        liability_pv = round(random.uniform(100000, 1000000), 2)
        liability_duration = round(random.uniform(3, 8), 2)
        asset1_price = round(random.uniform(50000, liability_pv), 2)
        asset1_duration = round(random.uniform(1, 6), 2)

        # Solve for asset2 weight
        asset2_required_pv = liability_pv - asset1_price
        if asset2_required_pv > 0:
            # asset1_duration × (asset1_price/liability_pv) + asset2_duration × (asset2_price/liability_pv) = liability_duration
            asset2_duration = round(random.uniform(liability_duration, 15), 2)
            # Solve: asset1_duration × asset1_price + asset2_duration × asset2_required_pv = liability_duration × liability_pv
            # asset2_required_pv = (liability_duration × liability_pv - asset1_duration × asset1_price) / asset2_duration
            asset2_price = round((liability_duration * liability_pv - asset1_duration * asset1_price) / asset2_duration, 2)
        else:
            asset2_price = 0

        q_id = f"dur_immunization_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"Asset 1: ${asset1_price:,.2f}, D={asset1_duration:.2f}; Asset 2: ${asset2_price:,.2f}, D={asset2_duration:.2f}. Portfolio D = {liability_duration:.2f}", "is_correct": True},
            {"label": "B", "text": f"All assets in single bond with D={liability_duration:.2f}", "is_correct": False},
            {"label": "C", "text": f"Equal dollar weights regardless of duration", "is_correct": False},
            {"label": "D", "text": f"Immunization is impossible", "is_correct": False},
            {"label": "E", "text": f"Invest all in longest-duration asset", "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Immunization",
            "difficulty": 3,
            "question_text": f"Liability: ${liability_pv:,.2f}, duration {liability_duration:.2f} yrs. Asset 1: ${asset1_price:,.2f}, duration {asset1_duration:.2f}. What Asset 2 would immunize (match duration)?",
            "choices": choices,
            "solution": f"D_portfolio = (D_1 × P_1 + D_2 × P_2) / (P_1 + P_2) must equal {liability_duration:.2f}. Solve for P_2 and choose D_2 accordingly.",
            "explanation": f"Immunization: match portfolio duration to liability duration. Protects against parallel yield curve shifts."
        }

    def portfolio_duration(self) -> Dict:
        """Portfolio duration: weighted average of component durations"""
        num_assets = random.randint(2, 4)
        weights = [round(random.uniform(0.1, 0.5), 2) for _ in range(num_assets - 1)]
        weights.append(round(1 - sum(weights), 2))
        durations = [round(random.uniform(2, 12), 2) for _ in range(num_assets)]

        portfolio_d = round(sum(w * d for w, d in zip(weights, durations)), 2)

        q_id = f"dur_portfolio_{datetime.now().timestamp()}"
        choices = [
            {"label": "A", "text": f"{portfolio_d:.2f} years", "is_correct": True},
            {"label": "B", "text": f"{round(sum(durations) / num_assets, 2):.2f} years", "is_correct": False},
            {"label": "C", "text": f"{max(durations):.2f} years", "is_correct": False},
            {"label": "D", "text": f"{min(durations):.2f} years", "is_correct": False},
            {"label": "E", "text": f"{round(sum(weights), 2):.2f} years", "is_correct": False},
        ]
        random.shuffle(choices)

        weights_str = ", ".join([f"{w*100:.1f}%" for w in weights])
        durations_str = ", ".join([f"{d:.2f}yr" for d in durations])

        return {
            "id": q_id,
            "exam": "FM",
            "topic": "Duration & Convexity",
            "subtopic": "Portfolio Duration",
            "difficulty": 1,
            "question_text": f"Portfolio: {num_assets} bonds with weights {weights_str} and durations {durations_str}. Calculate portfolio duration.",
            "choices": choices,
            "solution": f"D_portfolio = {' + '.join([f'{w:.2f}×{d:.2f}' for w, d in zip(weights, durations)])} = {portfolio_d:.2f} years",
            "explanation": f"Portfolio duration is the weighted average of component durations, using market-value weights."
        }

    @classmethod
    def generate_all(cls, n_per_method: int = 100) -> List[Dict]:
        """Generate n questions from each available method."""
        questions = []
        methods = cls.get_all_methods()

        for _ in range(n_per_method):
            gen = cls()
            for method_name in methods:
                method = getattr(gen, method_name)
                questions.append(method())

        return questions

    @classmethod
    def get_all_methods(cls) -> List[str]:
        """Return list of all question generation methods."""
        return [
            method for method in dir(cls)
            if not method.startswith('_') and callable(getattr(cls, method)) and method not in ['generate_all', 'get_all_methods']
        ]
