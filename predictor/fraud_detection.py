def detect_fraud(total_income, loan_amount):
    fraud_flag = False
    reasons = []

    # Rule 1: Very low income but high loan
    if total_income < 20000 and loan_amount > 500000:
        fraud_flag = True
        reasons.append(
            "Low income with unusually high loan amount"
        )

    return fraud_flag, reasons
