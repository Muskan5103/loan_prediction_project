# utils.py
def is_super_admin(user):
    return user.groups.filter(name="SuperAdmin").exists()


def get_user_input():
    name = input("Enter Applicant Name: ")
    age = int(input("Enter Age: "))
    income = int(input("Enter Monthly Income: "))
    credit_score = int(input("Enter Credit Score: "))
    loan_amount = int(input("Enter Loan Amount: "))
    application_count = int(input("Loan applications in last 7 days: "))

    return name, age, income, credit_score, loan_amount, application_count


def show_fraud_message(reasons):
    print("\n⚠️ POTENTIAL FRAUD DETECTED")
    for r in reasons:
        print("•", r)
    print("🔍 Application sent for manual review")


def show_loan_status(status, message):
    print("\n📄 LOAN STATUS")
    if status:
        print("✅", message)
    else:
        print("❌ Loan Rejected:", message)
