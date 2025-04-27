def clean_numeric(value):
    return float(value.replace('$', '').replace(',', '').strip())

def check_loan_eligibility(income, loan_amount):
    try:
        annual_income = clean_numeric(income)
        loan_amount = clean_numeric(loan_amount)
    except (ValueError, AttributeError):
        return False, "Invalid financial values"
    
    # Simple eligibility criteria: loan amount should not exceed 5x annual income
    if loan_amount <= annual_income * 5:
        return True, "Congratulations! You are eligible for the loan"
    return False, "Loan amount exceeds eligible limit (5x annual income)"