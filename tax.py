# Tax rates for 2026/27: England, Wales and Northern Ireland.
# CHECK EVERY FIGURE AGAINST GOV.UK before relying on the results.
# These are estimates only, not financial advice.

# Income tax (annual)
PERSONAL_ALLOWANCE = 12570
PERSONAL_ALLOWANCE_TAPER_START = 100000
BASIC_RATE_BAND = 37700
ADDITIONAL_RATE_THRESHOLD = 125140
BASIC_RATE = 0.20
HIGHER_RATE = 0.40
ADDITIONAL_RATE = 0.45

# Employee National Insurance, Class 1 (monthly)
NI_PRIMARY_THRESHOLD = 1048
NI_UPPER_EARNINGS_LIMIT = 4189
NI_MAIN_RATE = 0.08
NI_UPPER_RATE = 0.02

# Student loans (annual threshold, rate)
STUDENT_LOAN_PLANS = {
    "plan_1": (26900, 0.09),
    "plan_2": (29385, 0.09),
    "plan_4": (33795, 0.09),
    "plan_5": (25000, 0.09),
    "postgraduate": (21000, 0.06),
}


def personal_allowance(annual_income):
    if annual_income <= PERSONAL_ALLOWANCE_TAPER_START:
        return PERSONAL_ALLOWANCE
    reduction = (annual_income - PERSONAL_ALLOWANCE_TAPER_START) / 2
    return max(PERSONAL_ALLOWANCE - reduction, 0)


def income_tax(annual_income):
    taxable = max(annual_income - personal_allowance(annual_income), 0)

    tax = min(taxable, BASIC_RATE_BAND) * BASIC_RATE
    if taxable > BASIC_RATE_BAND:
        tax += (min(taxable, ADDITIONAL_RATE_THRESHOLD) - BASIC_RATE_BAND) * HIGHER_RATE
    if taxable > ADDITIONAL_RATE_THRESHOLD:
        tax += (taxable - ADDITIONAL_RATE_THRESHOLD) * ADDITIONAL_RATE
    return tax


def national_insurance(monthly_pay):
    if monthly_pay <= NI_PRIMARY_THRESHOLD:
        return 0
    ni = (min(monthly_pay, NI_UPPER_EARNINGS_LIMIT) - NI_PRIMARY_THRESHOLD) * NI_MAIN_RATE
    if monthly_pay > NI_UPPER_EARNINGS_LIMIT:
        ni += (monthly_pay - NI_UPPER_EARNINGS_LIMIT) * NI_UPPER_RATE
    return ni


def student_loan(annual_income, plan):
    if plan not in STUDENT_LOAN_PLANS:
        return 0
    threshold, rate = STUDENT_LOAN_PLANS[plan]
    return max(annual_income - threshold, 0) * rate


def monthly_deductions(monthly_pay, other_annual_salary, loan_plan, pension_percent):
    pension = monthly_pay * pension_percent / 100
    taxable_pay = monthly_pay - pension

    tax = (
        income_tax(other_annual_salary + taxable_pay * 12)
        - income_tax(other_annual_salary)
    ) / 12
    ni = national_insurance(monthly_pay)
    loan = (
        student_loan(other_annual_salary + monthly_pay * 12, loan_plan)
        - student_loan(other_annual_salary, loan_plan)
    ) / 12

    return {
        "pay": monthly_pay,
        "pension": pension,
        "income_tax": tax,
        "national_insurance": ni,
        "student_loan": loan,
        "take_home": monthly_pay - pension - tax - ni - loan,
    }
