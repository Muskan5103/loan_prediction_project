from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from .models import LoanApplication
from .forms import LoanForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import LoanApplicationSerializer
import pickle
import numpy as np
import os
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.http import JsonResponse
import json

# MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor', 'ml', 'loan_model.pkl')
# model = pickle.load(open(MODEL_PATH, 'rb'))



import os
import pickle
from django.conf import settings


def load_active_model():

    model_path = os.path.join(
        settings.BASE_DIR,
        'ml_models',
        'loan_model.pkl'
    )

    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    return model

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from django.core.exceptions import PermissionDenied

# @login_required
# def home(request):
#     user = request.user

#     # 👑 Super Admin → redirect
#     if user.is_superuser:
#         return redirect("superadmin_dashboard")

#     # 👨‍💼 Admin → redirect
#     if user.is_staff:
#         return redirect("admin_dashboard")

#     # 👤 Normal user only
#     return render(request, 'predictor/home.html')
def home(request):

    # 👑 Super Admin
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("superadmin_dashboard")

    # 👨‍💼 Admin
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    # 🌐 Everyone can see homepage
    return render(request, "predictor/home.html")


def index(request):

    # 👑 Super Admin
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("superadmin_dashboard")

    # 👨‍💼 Admin
    elif request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    # 👤 Normal User
    elif request.user.is_authenticated:
        return redirect("home")

    # 🌐 Guest User
    return render(request, "predictor/index.html")

def generate_ai_explanation(income, loan_amount, probability):
    reasons = []

    if income >= 5000:
        reasons.append("Income is sufficient")
    else:
        reasons.append("Low income")

    if loan_amount <= income * 20:
        reasons.append("Loan within safe limit")
    else:
        reasons.append("High loan amount")

    if probability >= 0.7:
        reasons.append("High approval probability")
    else:
        reasons.append("Low approval probability")

    return " | ".join(reasons)





# from .fraud_detection import detect_fraud

# def result(request):
#     if request.method == 'POST':
#         form = LoanForm(request.POST, request.FILES)
#         document = request.FILES.get("document")

#         if form.is_valid():
#             applicant_income = form.cleaned_data['applicant_income']
#             coapplicant_income = form.cleaned_data['coapplicant_income'] or 0
#             loan_amount = form.cleaned_data['loan_amount']
#             loan_term = form.cleaned_data['loan_term']
#             credit_history = int(form.cleaned_data['credit_history'])

#             total_income = applicant_income + coapplicant_income
            
          
            

#             # 🔴 FRAUD CHECK
#             fraud, reasons = detect_fraud(total_income, loan_amount)

#             # =========================
#             # 🚨 FRAUD CASE
#             # =========================
#             if fraud:
#                 LoanApplication.objects.create(
#                     user=request.user,
#                     applicant_income=applicant_income,
#                     coapplicant_income=coapplicant_income,
#                     loan_amount=loan_amount,
#                     loan_term=loan_term,
#                     credit_history=credit_history,
#                     document=document,
#                     # ✅ safe values
#                     probability=0,
#                     ai_explanation="Fraud detected",
#                     fraud_reason=" | ".join(reasons),
#                     status="REJECTED"
#                 )

#                 return render(request, "predictor/result.html", {
#                     "fraud": True,
#                     "fraud_reasons": reasons,
#                     "recommended_loan": round(recommended_loan, 2),
#                     "emi": emi,
#                     "interest_rate": interest_rate,
#                 })

#             # =========================
#             # 🤖 ML PREDICTION
#             # =========================
#             input_data = np.array([
#                 applicant_income,
#                 coapplicant_income,
#                 loan_amount,
#                 loan_term,
#                 credit_history
#             ]).reshape(1, -1)

#             model = load_active_model()

#             if not model:
#                 return render(request, "predictor/result.html", {
#                     "error": "No active ML model found"
#                 })

#             prediction = model.predict(input_data)[0]

#             prediction_proba = model.predict_proba(
#                 input_data
#             )[0][1]
#             probability = round(prediction_proba * 100, 2)
        

#             if probability >= 80:
#                 recommended_loan = loan_amount

#             elif probability >= 60:
#                 recommended_loan = loan_amount * 0.8

#             else:
#                 recommended_loan = loan_amount * 0.5

#             recommended_loan = round(recommended_loan, 2)

#             interest_rate = 8.5

#             monthly_rate = interest_rate / 12 / 100

#             months = loan_term

#             emi = (
#                 recommended_loan *
#                 monthly_rate *
#                 ((1 + monthly_rate) ** months)
#             ) / (
#                 ((1 + monthly_rate) ** months) - 1
#             )

#             emi = round(emi, 2)
            
#             uncertainty = ""

#             if probability >= 85:
#                 uncertainty = "Very confident prediction"

#             elif probability >= 60:
#                 uncertainty = "Moderately confident prediction"

#             else:
#                 uncertainty = "Prediction has higher uncertainty"

#             risk = "Low" if probability > 80 else "Medium" if probability >= 50 else "High"

#             result_text = "Loan Approved (AI Prediction)" if prediction == 1 else "Loan Rejected (AI Prediction)"
#             confidence_width = probability
#             explanation = generate_ai_explanation(
#                 income=total_income,
#                 loan_amount=loan_amount,
#                 probability=prediction_proba
#             )

#             # ✅ SAVE CORRECT DATA
#             LoanApplication.objects.create(
#                 user=request.user,
#                 applicant_income=applicant_income,
#                 coapplicant_income=coapplicant_income,
#                 loan_amount=loan_amount,
#                 loan_term=loan_term,
#                 credit_history=credit_history,
#                 document=document,
#                 probability=probability,
#                 ai_explanation=explanation,
#                 fraud_reason=None,
#                 status="AI_APPROVED" if prediction == 1 else "REJECTED"
#             )

#             return render(request, "predictor/result.html", {
#                 "fraud": False,
#                 "result": result_text,
#                 "probability": probability,
#                 "risk": risk,
#                 "confidence_width": confidence_width,
#                 "uncertainty": uncertainty,
#                 "recommended_loan": round(recommended_loan, 2),
#                 "emi": emi,
#                 "interest_rate": interest_rate,
#             })

#     return redirect("index")

from .fraud_detection import detect_fraud
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def result(request):

    if request.method == 'POST':

        form = LoanForm(request.POST, request.FILES)

        # uploaded document
        document = request.FILES.get("document")

        if form.is_valid():

            # =========================
            # FORM DATA
            # =========================

            applicant_income = form.cleaned_data['applicant_income']

            coapplicant_income = (
                form.cleaned_data['coapplicant_income'] or 0
            )

            loan_amount = form.cleaned_data['loan_amount']

            loan_term = form.cleaned_data['loan_term']

            credit_history = int(
                form.cleaned_data['credit_history']
            )

            total_income = (
                applicant_income + coapplicant_income
            )

            # =========================
            # DEFAULT RECOMMENDATION
            # (used in fraud case too)
            # =========================

            # DEFAULT SMART RECOMMENDATION
            recommended_loan = min(
                total_income * 20,
                loan_amount * 0.5
            )

            recommended_loan = round(recommended_loan, 2)

            # =========================
            # EMI CALCULATOR
            # =========================

            interest_rate = 8.5

            monthly_rate = (
                interest_rate / 12 / 100
            )

            months = loan_term

            emi = (
                recommended_loan *
                monthly_rate *
                ((1 + monthly_rate) ** months)
            ) / (
                ((1 + monthly_rate) ** months) - 1
            )

            emi = round(emi, 2)

            # =========================
            # FRAUD CHECK
            # =========================

            fraud, reasons = detect_fraud(
                total_income,
                loan_amount
            )

            # =========================
            # FRAUD CASE
            # =========================

            if fraud:

                LoanApplication.objects.create(
                    user=request.user,
                    applicant_income=applicant_income,
                    coapplicant_income=coapplicant_income,
                    loan_amount=loan_amount,
                    loan_term=loan_term,
                    credit_history=credit_history,
                    document=document,

                    probability=0,
                    ai_explanation="Fraud detected",
                    fraud_reason=" | ".join(reasons),
                    status="REJECTED"
                )

                return render(
                    request,
                    "predictor/result.html",
                    {
                        "fraud": True,
                        "fraud_reasons": reasons,
                        "recommended_loan": round(recommended_loan, 2),
                        "emi": emi,
                        "interest_rate": interest_rate,
                    }
                )

            # =========================
            # ML PREDICTION
            # =========================

            input_data = np.array([
                applicant_income,
                coapplicant_income,
                loan_amount,
                loan_term,
                credit_history
            ]).reshape(1, -1)

            model = load_active_model()

            if not model:

                return render(
                    request,
                    "predictor/result.html",
                    {
                        "error": "No active ML model found"
                    }
                )

            prediction = model.predict(
                input_data
            )[0]

            prediction_proba = model.predict_proba(
                input_data
            )[0][1]

            probability = round(
                prediction_proba * 100,
                2
            )

            # =========================
            # SMART LOAN RECOMMENDATION
            # =========================

            if probability >= 80:

                recommended_loan = loan_amount

            elif probability >= 60:

                recommended_loan = loan_amount * 0.8

            else:

                recommended_loan = min(total_income * 20, loan_amount * 0.5)

            recommended_loan = round(
                recommended_loan,
                2
            )

            # =========================
            # UPDATED EMI
            # =========================

            emi = (
                recommended_loan *
                monthly_rate *
                ((1 + monthly_rate) ** months)
            ) / (
                ((1 + monthly_rate) ** months) - 1
            )

            emi = round(emi, 2)

            # =========================
            # CONFIDENCE
            # =========================

            if probability >= 85:

                uncertainty = (
                    "Very confident prediction"
                )

            elif probability >= 60:

                uncertainty = (
                    "Moderately confident prediction"
                )

            else:

                uncertainty = (
                    "Prediction has higher uncertainty"
                )

            # =========================
            # RISK LEVEL
            # =========================

            if probability > 80:

                risk = "Low"

            elif probability >= 50:

                risk = "Medium"

            else:

                risk = "High"

            # =========================
            # RESULT TEXT
            # =========================

            if prediction == 1:

                result_text = (
                    "Loan Approved (AI Prediction)"
                )

            else:

                result_text = (
                    "Loan Rejected (AI Prediction)"
                )

            confidence_width = probability

            # =========================
            # AI EXPLANATION
            # =========================

            explanation = generate_ai_explanation(
                income=total_income,
                loan_amount=loan_amount,
                probability=prediction_proba
            )

            # =========================
            # SAVE TO DATABASE
            # =========================

            LoanApplication.objects.create(
                user=request.user,
                applicant_income=applicant_income,
                coapplicant_income=coapplicant_income,
                loan_amount=loan_amount,
                loan_term=loan_term,
                credit_history=credit_history,
                document=document,

                probability=probability,
                ai_explanation=explanation,
                fraud_reason=None,

                status=(
                    "AI_APPROVED"
                    if prediction == 1
                    else "REJECTED"
                )
            )

            # =========================
            # RESULT PAGE
            # =========================

            return render(
                request,
                "predictor/result.html",
                {
                    "fraud": False,
                    "result": result_text,
                    "probability": probability,
                    "risk": risk,
                    "confidence_width": confidence_width,
                    "uncertainty": uncertainty,

                    "recommended_loan": recommended_loan,

                    "emi": emi,
                    "interest_rate": interest_rate,
                }
            )

    return redirect("index")

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def history(request):
    records = LoanApplication.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # ===== GET FILTER VALUES =====
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search = request.GET.get('search')

    # ===== STATUS FILTER =====
    if status:
        records = records.filter(status=status)

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





# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)   # ✅ THIS IS REQUIRED
#             return redirect('home')  # or dashboard
#     else:
#         form = RegisterForm()

#     if form.is_valid():
#         user = form.save()
#         print("USER CREATED:", user.username)
#         login(request, user)
#         return redirect('home')
#     else:
#         print(form.errors)


#     return render(request, 'predictor/register.html', {'form': form})



from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            print("USER CREATED:", user.username)
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, 'predictor/register.html', {'form': form})



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
                return redirect("index")

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
    applications = LoanApplication.objects.all().order_by('-created_at')
    return render(request, 'predictor/admin_dashboard.html', {
        'applications': applications
    })


@staff_member_required
def update_loan_status(request, loan_id, decision):
    loan = LoanApplication.objects.get(id=loan_id)
    loan.admin_decision = decision
    loan.save()
    return redirect('admin_dashboard')

from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def approve_loan(request, loan_id):
    loan = get_object_or_404(LoanApplication, id=loan_id)
    loan.status = 'ADMIN_APPROVED'
    loan.admin = request.user
    loan.save()
    return redirect('admin_dashboard')


@staff_member_required
def reject_loan(request, loan_id):
    loan = get_object_or_404(LoanApplication, id=loan_id)
    loan.status = 'REJECTED'
    loan.admin = request.user
    loan.save()
    return redirect('admin_dashboard')








from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from datetime import timedelta


@staff_member_required
def admin_dashboard(request):

    applications = LoanApplication.objects.all().order_by('-id')

    total = applications.count()

    # =========================
    # APPROVAL STATS
    # =========================

    ai_approved = applications.filter(
        status='AI_APPROVED'
    ).count()

    admin_approved = applications.filter(
        status='ADMIN_APPROVED'
    ).count()

    rejected = applications.filter(
        status='REJECTED'
    ).count()

    ai_percent = round(
        (ai_approved / total) * 100,
        2
    ) if total else 0

    admin_percent = round(
        (admin_approved / total) * 100,
        2
    ) if total else 0

    reject_percent = round(
        (rejected / total) * 100,
        2
    ) if total else 0


    # =========================
    # FRAUD ANALYSIS
    # =========================

    fraud_cases = applications.filter(
        fraud_reason__isnull=False
    ).exclude(
        fraud_reason=""
    ).count()

    normal_cases = total - fraud_cases


    # =========================
    # LOAN DISTRIBUTION
    # =========================

    small_loans = applications.filter(
        loan_amount__lt=100000
    ).count()

    medium_loans = applications.filter(
        loan_amount__gte=100000,
        loan_amount__lt=500000
    ).count()

    large_loans = applications.filter(
        loan_amount__gte=500000
    ).count()


    # =========================
    # LAST 7 DAYS TREND
    # =========================

    last_7_days = []

    approvals = []

    for i in range(6, -1, -1):

        day = now().date() - timedelta(days=i)

        count = applications.filter(
            status='ADMIN_APPROVED',
            created_at__date=day
        ).count()

        last_7_days.append(
            day.strftime('%d %b')
        )

        approvals.append(count)


    # =========================
    # AI EXPLANATIONS
    # =========================

    for app in applications:

        if app.ai_explanation:

            app.explanation_list = (
                app.ai_explanation.split(" | ")
            )

        else:

            app.explanation_list = []


    # =========================
    # CONTEXT
    # =========================

    context = {

        'applications': applications,

        'total': total,

        'ai_percent': ai_percent,

        'admin_percent': admin_percent,

        'reject_percent': reject_percent,

        'days': last_7_days,

        'approvals': approvals,

        # ⭐ NEW
        'fraud_cases': fraud_cases,

        'normal_cases': normal_cases,

        'small_loans': small_loans,

        'medium_loans': medium_loans,

        'large_loans': large_loans,
    }

    return render(
        request,
        'predictor/admin_dashboard.html',
        context
    )



from django.shortcuts import redirect, get_object_or_404



from django.shortcuts import get_object_or_404, redirect

def admin_decision(request, pk, decision):
    application = get_object_or_404(LoanApplication, pk=pk)

    if request.method == 'POST':

        if decision == 'approve':
            application.status = 'ADMIN_APPROVED'
            application.admin = request.user

        elif decision == 'reject':
            application.status = 'REJECTED'
            application.admin = request.user

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
            is_active=True,
            version=f"v{MLModel.objects.count() + 1}",
            accuracy=95.2
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
    records = LoanApplication.objects.select_related('user').order_by('-created_at')
    return render(request, 'predictor/admin_history.html', {
        'records': records
    })

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def superuser_required(user):
    return user.is_superuser


@user_passes_test(superuser_required)
def superuser_history(request):
    records = LoanApplication.objects.select_related('user').order_by('-created_at')

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

    applications = LoanApplication.objects.all().order_by('-id')

    for app in applications:
        writer.writerow([
            app.user.username if app.user else 'N/A',
            app.loan_amount,
            app.status,
            f"{round(app.probability, 2)}%",
            
            app.created_at.strftime("%Y-%m-%d")
        ])

    return response

from fpdf import FPDF

@staff_member_required
def export_pdf(request):
    applications = LoanApplication.objects.all().order_by('-id')

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
        clean_result = app.status.replace("(AI Prediction)", "").strip()
        pdf.cell(31, 8, clean_result, 1)

        pdf.cell(31, 8, f"{round(app.probability, 2)}%", 1)
        
        pdf.cell(31, 8, app.created_at.strftime('%d-%m-%Y'), 1)
        pdf.ln()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="loan_report.pdf"'
    response.write(pdf.output(dest='S').encode('latin-1'))

    return response





from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import is_super_admin
from .models import MLModel,AuditLog

@login_required
@user_passes_test(is_super_admin)
def superadmin_dashboard(request):

    active_model = MLModel.objects.filter(
        is_active=True
    ).first()

    models = MLModel.objects.all().order_by(
        '-uploaded_at'
    )

    context = {

        "active_model": active_model,

        "models": models,

        "total_predictions":
            LoanApplication.objects.count(),

        "ai_decisions": LoanApplication.objects.exclude(
                probability=0
        ).count(),

        "admin_decisions":
            LoanApplication.objects.filter(
                status='ADMIN_APPROVED'
            ).count(),

        "recent_logs":
            AuditLog.objects.order_by(
                "-timestamp"
            )[:5],
    }

    return render(
        request,
        "predictor/superadmin_dashboard.html",
        context
    )

@login_required
@user_passes_test(is_super_admin)
def activate_model(request, model_id):

    model = get_object_or_404(
        MLModel,
        id=model_id
    )

    # deactivate all
    MLModel.objects.update(
        is_active=False
    )

    # activate selected
    model.is_active = True
    model.save()

    # audit log
    AuditLog.objects.create(
        user=request.user,
        action=f"Activated model: {model.version}"
    )

    return redirect("superadmin_dashboard")


@login_required
@user_passes_test(is_super_admin)
def system_history(request):

    logs = AuditLog.objects.order_by(
        '-timestamp'
    )

    return render(
        request,
        'predictor/system_history.html',
        {
            'records': logs
        }
    )


# from django.shortcuts import render

# def index(request):
#     return render(request, 'predictor/index.html')


from django.shortcuts import render
from .forms import LoanForm
from .fraud_detection import detect_fraud
from .loan_approval import check_loan_eligibility

import os
from django.conf import settings



def loan_form(request):

    form = LoanForm()
    context = {"form": form}

    if request.method == "POST":

        # ✅ IMPORTANT
        form = LoanForm(request.POST, request.FILES)

        if form.is_valid():

            # -----------------------------
            # GET FORM DATA
            # -----------------------------
            applicant_income = form.cleaned_data["applicant_income"]

            coapplicant_income = (
                form.cleaned_data["coapplicant_income"] or 0
            )

            loan_amount = form.cleaned_data["loan_amount"]

            credit_history = int(
                form.cleaned_data["credit_history"]
            )

            loan_term = form.cleaned_data["loan_term"]

            # ✅ DOCUMENT FILE
            document = form.cleaned_data.get("document")

            # Total income
            total_income = (
                applicant_income + coapplicant_income
            )

            # -----------------------------
            # SAVE DOCUMENT
            # -----------------------------
            if document:

                

                upload_path = os.path.join(
                    settings.MEDIA_ROOT,
                    "documents",
                    document.name
                )

                os.makedirs(
                    os.path.dirname(upload_path),
                    exist_ok=True
                )

                with open(upload_path, "wb+") as destination:
                    for chunk in document.chunks():
                        destination.write(chunk)

            # -----------------------------
            # STEP 1: FRAUD DETECTION
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
                # STEP 2: LOAN APPROVAL
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

    return render(
        request,
        "predictor/loan_form.html",
        context
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_loan_api(request):

    applicant_income = float(
        request.data.get('applicant_income')
    )

    coapplicant_income = float(
        request.data.get('coapplicant_income')
    )

    loan_amount = float(
        request.data.get('loan_amount')
    )

    loan_term = int(
        request.data.get('loan_term')
    )

    credit_history = int(
        request.data.get('credit_history')
    )


    # =========================
    # LOAD MODEL
    # =========================

    active_model = MLModel.objects.filter(
        is_active=True
    ).first()

    if not active_model:

        return Response({

            'error': 'No active ML model found'

        })


    with open(active_model.file.path, 'rb') as file:

        model = pickle.load(file)


    # =========================
    # PREDICTION
    # =========================

    features = [[

        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_term,
        credit_history

    ]]

    prediction = model.predict(features)[0]

    probability = round(

        model.predict_proba(features)[0][1] * 100,

        2
    )

    result = (
        "Approved"
        if prediction == 1
        else "Rejected"
    )


    return Response({

        'prediction': result,

        'probability': probability,

        'risk': (
            'Low'
            if probability > 80
            else 'Medium'
            if probability >= 50
            else 'High'
        )
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loan_history_api(request):

    loans = LoanApplication.objects.all().order_by('-id')

    serializer = LoanApplicationSerializer(
        loans,
        many=True
    )

    return Response(serializer.data)



def chatbot(request):

    if request.method == "POST":

        data = json.loads(request.body)

        message = data.get("message", "").lower()

        response = "Sorry, I didn't understand."

        # GREETING
        if (
            "hello" in message or
            "hi" in message or
            "hlo" in message or
            "hey" in message
        ):

            response = (
                "Hello 👋 Welcome to Loan Predictor!"
            )

        # LOAN
        elif "loan" in message:

            response = (
                "Loan approval depends on income, "
                "credit history, loan amount, "
                "and fraud detection."
            )

        # APPROVAL
        elif "approved" in message:

            response = (
                "Higher income and good credit "
                "history increase approval chances."
            )

        # REJECTION
        elif "rejected" in message:

            response = (
                "Loan may be rejected because of "
                "low income, high loan amount, "
                "or poor credit history."
            )

        # EMI
        elif "emi" in message:

            response = (
                "EMI depends on loan amount, "
                "interest rate, and loan term."
            )

        # DOCUMENTS
        elif (
            "document" in message or
            "documents" in message
        ):

            response = (
                "Upload Aadhaar, PAN card, "
                "or salary slip."
            )

        return JsonResponse({
            "response": response
        })

    return JsonResponse({
        "response": "Invalid request"
    })