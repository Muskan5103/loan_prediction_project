from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect

from .forms import LoanForm
from .models import LoanHistory
import pickle
import numpy as np
import os
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor', 'ml', 'loan_model.pkl')
model = pickle.load(open(MODEL_PATH, 'rb'))


from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def home(request):
    user = request.user

    # Super Admin
    if user.is_superuser:
        return redirect("superadmin_dashboard")

    # Admin (staff but not superuser)
    if user.is_staff:
        return redirect("admin_dashboard")  
    
    form = LoanForm()
    return render(request, 'predictor/home.html', {
        'form': form
    })
    





# def result(request):
#     if request.method == 'POST':
#         form = LoanForm(request.POST)

#         if form.is_valid():
#             applicant_income = form.cleaned_data['applicant_income']
#             coapplicant_income = form.cleaned_data['coapplicant_income']
#             loan_amount = form.cleaned_data['loan_amount']
#             loan_term = form.cleaned_data['loan_term']
#             credit_history = int(form.cleaned_data['credit_history'])

#             input_data = np.array([
#                 applicant_income,
#                 coapplicant_income,
#                 loan_amount,
#                 loan_term,
#                 credit_history
#             ]).reshape(1, -1)

#             # ✅ ML Prediction
#             prediction = model.predict(input_data)[0]
#             prediction_proba = model.predict_proba(input_data)[0][1]

#             # ✅ Probability %
#             probability = round(prediction_proba * 100, 2)

#             # ✅ RISK LOGIC (THIS IS WHERE IT BELONGS)
#             if probability > 80:
#                 risk = "Low"
#             elif probability >= 50:
#                 risk = "Medium"
#             else:
#                 risk = "High"

#             # ✅ Approval / Rejection Text
#             if prediction == 1:
#                 result_text = "Loan Approved (AI Prediction)"
#             else:
#                 result_text = "Loan Rejected (AI Prediction)"

#             # ✅ Explainable AI
#             explanation = generate_ai_explanation(
#                 income=applicant_income,
#                 loan_amount=loan_amount,
#                 probability=prediction_proba
#             )

#             # ✅ Save History
#             LoanHistory.objects.create(
#                 user=request.user,
#                 applicant_income=applicant_income,
#                 coapplicant_income=coapplicant_income,
#                 loan_amount=loan_amount,
#                 loan_term=loan_term,
#                 credit_history=credit_history,
#                 ai_result=result_text,
#                 probability=probability,
#                 ai_explanation=explanation
#             )

#             # ✅ FINAL CONTEXT (USED BY result.html)
#             context = {
#                 "result": result_text,
#                 "probability": probability,
#                 "risk": risk
#             }

#             return render(request, "predictor/result.html", context)

#     return redirect("home")


# def result(request):
#     if request.method == 'POST':
#         form = LoanForm(request.POST)

#         if form.is_valid():
#             applicant_income = form.cleaned_data['applicant_income']
#             coapplicant_income = form.cleaned_data['coapplicant_income'] or 0
#             loan_amount = form.cleaned_data['loan_amount']
#             loan_term = form.cleaned_data['loan_term']
#             credit_history = int(form.cleaned_data['credit_history'])

#             total_income = applicant_income + coapplicant_income

#             # ==============================
#             # STEP 1: FRAUD DETECTION
#             # ==============================
#             fraud, reasons = detect_fraud(
#                 total_income=total_income,
#                 loan_amount=loan_amount
#             )

#             if fraud:
#                 # Save fraud case (optional but impressive)
#                 LoanHistory.objects.create(
#                     user=request.user,
#                     applicant_income=applicant_income,
#                     coapplicant_income=coapplicant_income,
#                     loan_amount=loan_amount,
#                     loan_term=loan_term,
#                     credit_history=credit_history,
#                     ai_result="Potential Fraud Detected",
#                     probability=0,
#                     ai_explanation="Application flagged for manual review due to suspicious patterns."
#                 )

#                 return render(request, "predictor/result.html", {
#                     "fraud": True,
#                     "fraud_reasons": reasons
#                 })

#             # ==============================
#             # STEP 2: ML PREDICTION
#             # ==============================
#             input_data = np.array([
#                 applicant_income,
#                 coapplicant_income,
#                 loan_amount,
#                 loan_term,
#                 credit_history
#             ]).reshape(1, -1)

#             prediction = model.predict(input_data)[0]
#             prediction_proba = model.predict_proba(input_data)[0][1]

#             probability = round(prediction_proba * 100, 2)

#             # ==============================
#             # RISK CALCULATION
#             # ==============================
#             if probability > 80:
#                 risk = "Low"
#             elif probability >= 50:
#                 risk = "Medium"
#             else:
#                 risk = "High"

#             # ==============================
#             # RESULT TEXT
#             # ==============================
#             if prediction == 1:
#                 result_text = "Loan Approved (AI Prediction)"
#             else:
#                 result_text = "Loan Rejected (AI Prediction)"

#             # ==============================
#             # EXPLAINABLE AI
#             # ==============================
#             explanation = generate_ai_explanation(
#                 income=total_income,
#                 loan_amount=loan_amount,
#                 probability=prediction_proba
#             )

#             # ==============================
#             # SAVE HISTORY
#             # ==============================
#             LoanHistory.objects.create(
#                 user=request.user,
#                 applicant_income=applicant_income,
#                 coapplicant_income=coapplicant_income,
#                 loan_amount=loan_amount,
#                 loan_term=loan_term,
#                 credit_history=credit_history,
#                 ai_result=result_text,
#                 probability=probability,
#                 ai_explanation=explanation
#             )

#             # ==============================
#             # FINAL CONTEXT
#             # ==============================
#             context = {
#                 "fraud": False,
#                 "result": result_text,
#                 "probability": probability,
#                 "risk": risk
#             }

#             return render(request, "predictor/result.html", context)

#     return redirect("home")
   

# def generate_ai_explanation(income, loan_amount, probability):
#     reasons = []

#     if income >= 5000:
#         reasons.append("Income is sufficient (≥ ₹5,000)")
#     else:
#         reasons.append("Income is low")

#     if loan_amount <= income * 20:
#         reasons.append("Loan amount within safe limit")
#     else:
#         reasons.append("Loan amount is high compared to income")

#     if probability >= 0.7:
#         reasons.append(f"High approval probability ({round(probability*100)}%)")
#     else:
#         reasons.append(f"Low approval probability ({round(probability*100)}%)")

#     return " | ".join(reasons)

from .fraud_detection import detect_fraud

def result(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)

        if form.is_valid():
            applicant_income = form.cleaned_data['applicant_income']
            coapplicant_income = form.cleaned_data['coapplicant_income'] or 0
            loan_amount = form.cleaned_data['loan_amount']
            loan_term = form.cleaned_data['loan_term']
            credit_history = int(form.cleaned_data['credit_history'])

            total_income = applicant_income + coapplicant_income

            # 🔴 FRAUD CHECK
            fraud, reasons = detect_fraud(total_income, loan_amount)

            if fraud:
                LoanHistory.objects.create(
                    user=request.user,
                    applicant_income=applicant_income,
                    coapplicant_income=coapplicant_income,
                    loan_amount=loan_amount,
                    loan_term=loan_term,
                    credit_history=credit_history,
                    ai_result="Potential Fraud Detected",
                    probability=0,
                    ai_explanation=" | ".join(reasons),
                    is_fraud=True  
                )

                return render(request, "predictor/result.html", {
                    "fraud": True,
                    "fraud_reasons": reasons
                })

            # ✅ ML PREDICTION
            input_data = np.array([
                applicant_income,
                coapplicant_income,
                loan_amount,
                loan_term,
                credit_history
            ]).reshape(1, -1)

            prediction = model.predict(input_data)[0]
            prediction_proba = model.predict_proba(input_data)[0][1]
            probability = round(prediction_proba * 100, 2)

            risk = "Low" if probability > 80 else "Medium" if probability >= 50 else "High"

            result_text = "Loan Approved (AI Prediction)" if prediction == 1 else "Loan Rejected (AI Prediction)"

            explanation = generate_ai_explanation(
                income=total_income,
                loan_amount=loan_amount,
                probability=prediction_proba
            )

            LoanHistory.objects.create(
                user=request.user,
                applicant_income=applicant_income,
                coapplicant_income=coapplicant_income,
                loan_amount=loan_amount,
                loan_term=loan_term,
                credit_history=credit_history,
                ai_result=result_text,
                probability=probability,
                ai_explanation=explanation,
                is_fraud=False  # ✅ NORMAL CASE
            )

            return render(request, "predictor/result.html", {
                "fraud": False,
                "result": result_text,
                "probability": probability,
                "risk": risk
            })

    return redirect("home")

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def history(request):
    records = LoanHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # ===== GET FILTER VALUES =====
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search = request.GET.get('search')

    # ===== STATUS FILTER =====
    if status:
        records = records.filter(admin_decision=status)

    # ===== DATE RANGE FILTER =====
    from datetime import datetime, timedelta

    if start_date and end_date:
        records = records.filter(
        created_at__date__range=[start_date, end_date]
    )

    elif start_date:
        records = records.filter(created_at__date__gte=start_date)

    elif end_date:
        records = records.filter(created_at__date__lte=end_date)

    # ===== SEARCH (Loan Amount / Income) =====
    if search:
        records = records.filter(
            Q(loan_amount__icontains=search) |
            Q(applicant_income__icontains=search)
        )

    return render(request, 'predictor/history.html', {
        'records': records
    })





def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # ✅ THIS IS REQUIRED
            return redirect('home')  # or dashboard
    else:
        form = RegisterForm()

    if form.is_valid():
        user = form.save()
        print("USER CREATED:", user.username)
        login(request, user)
        return redirect('home')
    else:
        print(form.errors)


    return render(request, 'predictor/register.html', {'form': form})



# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             print(request.user.is_authenticated)

#             return redirect('home')
#         else:
#             return render(request, 'predictor/login.html', {'error': 'Invalid credentials'})

#     return render(request, 'predictor/login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 ROLE-BASED REDIRECT
            if user.is_superuser:
                return redirect("superadmin_dashboard")
            elif user.is_staff:
                return redirect("admin_dashboard")
            else:
                return redirect("home")

        return render(request, "predictor/login.html", {
            "error": "Invalid credentials"
        })

    return render(request, "predictor/login.html")




def user_logout(request):
    logout(request)
    return redirect('login')


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    applications = LoanHistory.objects.all().order_by('-created_at')
    return render(request, 'predictor/admin_dashboard.html', {
        'applications': applications
    })


@staff_member_required
def update_loan_status(request, loan_id, decision):
    loan = LoanHistory.objects.get(id=loan_id)
    loan.admin_decision = decision
    loan.save()
    return redirect('admin_dashboard')

from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def approve_loan(request, loan_id):
    loan = get_object_or_404(LoanHistory, id=loan_id)
    loan.admin_decision = 'Approved'
    loan.save()
    return redirect('admin_dashboard')


@staff_member_required
def reject_loan(request, loan_id):
    loan = get_object_or_404(LoanHistory, id=loan_id)
    loan.admin_decision = 'Rejected'
    loan.save()
    return redirect('admin_dashboard')








from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from datetime import timedelta
from .models import LoanHistory

@staff_member_required
def admin_dashboard(request):
    applications = LoanHistory.objects.all().order_by('-id')

    total = applications.count()

    ai_approved = applications.filter(ai_result__icontains='Approved').count()
    admin_approved = applications.filter(admin_decision='Approved').count()
    rejected = applications.filter(admin_decision='Rejected').count()

    ai_percent = round((ai_approved / total) * 100, 2) if total else 0
    admin_percent = round((admin_approved / total) * 100, 2) if total else 0
    reject_percent = round((rejected / total) * 100, 2) if total else 0

    # 📈 Last 7 days approval trend (FIXED)
    last_7_days = []
    approvals = []

    for i in range(6, -1, -1):
        day = now().date() - timedelta(days=i)

        count = applications.filter(
            admin_decision='Approved',
            created_at__date=day
        ).count()

        last_7_days.append(day.strftime('%d %b'))
        approvals.append(count)

    for app in applications:
        if app.ai_explanation:
            app.explanation_list = app.ai_explanation.split(" | ")
        else:
            app.explanation_list = []

    context = {
        'applications': applications,
        'total': total,
        'ai_percent': ai_percent,
        'admin_percent': admin_percent,
        'reject_percent': reject_percent,
        'days': last_7_days,
        'approvals': approvals,
    }

    return render(request, 'predictor/admin_dashboard.html', context)



from django.shortcuts import redirect, get_object_or_404
from .models import LoanHistory


def admin_decision(request, pk, decision):
    application = get_object_or_404(LoanHistory, pk=pk)

    if request.method == 'POST':
        if decision == 'approve':
            application.admin_decision = 'Approved'
        elif decision == 'reject':
            application.admin_decision = 'Rejected'

        application.save()

    return redirect('admin_dashboard')


from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def superuser_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url='login'
    )(view_func)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import MLModel, AuditLog
from .utils import is_super_admin


@login_required
@user_passes_test(is_super_admin)
def upload_model(request):
    if request.method == "POST":
        model_file = request.FILES.get("model_file")

        if not model_file:
            return render(request, "predictor/upload_model.html", {
                "error": "Please select a model file"
            })

        # deactivate old models
        MLModel.objects.update(is_active=False)

        # save new model
        MLModel.objects.create(
            file=model_file,
            uploaded_by=request.user,
            is_active=True
        )

        # log activity
        AuditLog.objects.create(
            user=request.user,
            action="Uploaded & activated new ML model"
        )

        # ✅ redirect BACK to dashboard
        return redirect("superadmin_dashboard")

    return render(request, "predictor/upload_model.html")



from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_history(request):
    records = LoanHistory.objects.select_related('user').order_by('-created_at')
    return render(request, 'predictor/admin_history.html', {
        'records': records
    })

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def superuser_required(user):
    return user.is_superuser


@user_passes_test(superuser_required)
def superuser_history(request):
    records = LoanHistory.objects.select_related('user').order_by('-created_at')

    return render(
        request,
        'predictor/superuser_history.html',
        {'records': records}
    )


import csv
from django.http import HttpResponse
from .models import LoanApplication
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="loan_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'User',
        'Loan Amount',
        'AI Result',
        'Probability',
        'Admin Decision',
        'Date'
    ])

    applications = LoanHistory.objects.all().order_by('-id')

    for app in applications:
        writer.writerow([
            app.user.username if app.user else 'N/A',
            app.loan_amount,
            app.ai_result,
            f"{round(app.probability, 2)}%",
            app.admin_decision,
            app.created_at.strftime("%Y-%m-%d")
        ])

    return response

from fpdf import FPDF

@staff_member_required
def export_pdf(request):
    applications = LoanHistory.objects.all().order_by('-id')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    pdf.cell(190, 10, "Loan Approval Report", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", "B", 9)
    headers = ["User", "Loan Amt", "AI Result", "Prob", "Decision", "Date"]

    for h in headers:
        pdf.cell(31, 8, h, border=1)
    pdf.ln()

    pdf.set_font("Arial", size=9)

    for app in applications:
        pdf.cell(31, 8, app.user.username if app.user else 'N/A', 1)
        pdf.cell(31, 8, str(app.loan_amount), 1)
        clean_result = app.ai_result.replace("(AI Prediction)", "").strip()
        pdf.cell(31, 8, clean_result, 1)

        pdf.cell(31, 8, f"{round(app.probability, 2)}%", 1)
        pdf.cell(31, 8, app.admin_decision, 1)
        pdf.cell(31, 8, app.created_at.strftime('%d-%m-%Y'), 1)
        pdf.ln()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="loan_report.pdf"'
    response.write(pdf.output(dest='S').encode('latin-1'))

    return response





from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import is_super_admin
from .models import MLModel, LoanHistory, AuditLog

@login_required
@user_passes_test(is_super_admin)
def superadmin_dashboard(request):
    active_model = MLModel.objects.filter(is_active=True).first()

    context = {
        "active_model": active_model,
        "total_predictions": LoanHistory.objects.count(),
        "ai_decisions": LoanHistory.objects.filter(admin_decision__isnull=True).count(),
        "admin_decisions": LoanHistory.objects.filter(admin_decision__isnull=False).count(),
        "recent_logs": AuditLog.objects.order_by("-timestamp")[:5],
    }

    return render(request, "predictor/superadmin_dashboard.html", context)



@login_required
@user_passes_test(is_super_admin)
def system_history(request):
    logs = AuditLog.objects.order_by('-timestamp')
    return render(
        request,
        'predictor/superuser_history.html',
        {'logs': logs}
    )


from django.shortcuts import render

def index(request):
    return render(request, 'predictor/index.html')


from django.shortcuts import render
from .forms import LoanForm
from .fraud_detection import detect_fraud
from .loan_approval import check_loan_eligibility





def loan_form(request):
    form = LoanForm()
    context = {"form": form}

    if request.method == "POST":
        form = LoanForm(request.POST)

        if form.is_valid():
            # Get cleaned data
            applicant_income = form.cleaned_data["applicant_income"]
            coapplicant_income = form.cleaned_data["coapplicant_income"] or 0
            loan_amount = form.cleaned_data["loan_amount"]
            credit_history = int(form.cleaned_data["credit_history"])
            loan_term = form.cleaned_data["loan_term"]

            # Total income
            total_income = applicant_income + coapplicant_income

            # -----------------------------
            # STEP 1: Fraud Detection
            # -----------------------------
            fraud, reasons = detect_fraud(
                total_income,
                loan_amount
            )

            if fraud:
                context.update({
                    "fraud": True,
                    "fraud_reasons": reasons
                })
            else:
                # -----------------------------
                # STEP 2: Loan Approval
                # -----------------------------
                status, message = check_loan_eligibility(
                    total_income,
                    loan_amount,
                    credit_history,
                    loan_term
                )

                context.update({
                    "fraud": False,
                    "status": status,
                    "message": message
                })

    return render(request, "predictor/loan_form.html", context)
