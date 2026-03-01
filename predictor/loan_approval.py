def check_loan_eligibility(total_income, loan_amount, credit_history, loan_term):

    if credit_history == 0:
        return False, "No credit history available"

    if total_income < 15000:
        return False, "Income too low"

    if loan_amount > total_income * 20:
        return False, "Loan amount too high compared to income"

    if loan_term > 360:
        return False, "Loan term too long"

    return True, "Loan Approved"

from .fraud_detection import detect_fraud
from .models import LoanApplication

def create_loan_application(
    income,
    loan_amount,
    credit_history,
    loan_term,
    probability
):
    # 1️⃣ Eligibility check
    eligible, eligibility_msg = check_loan_eligibility(
        income, loan_amount, credit_history, loan_term
    )

    # 2️⃣ Fraud check
    is_fraud, fraud_msg = detect_fraud(income, loan_amount)

    # 3️⃣ Decide final status
    if is_fraud:
        status = 'REJECTED'
        explanation = f"Fraud detected: {fraud_msg}"
    elif not eligible:
        status = 'REJECTED'
        explanation = eligibility_msg
    else:
        status = 'AI_APPROVED'
        explanation = eligibility_msg

    # 4️⃣ Save to database ✅
    loan = LoanApplication.objects.create(
        applicant_income=income,
        loan_amount=loan_amount,
        probability=probability,
        ai_explanation=explanation,
        is_fraud=is_fraud,
        status=status
    )

    return loan
