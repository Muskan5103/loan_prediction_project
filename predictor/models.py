from django.db import models
from django.contrib.auth.models import User

class LoanHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    applicant_income = models.FloatField()
    coapplicant_income = models.FloatField()
    loan_amount = models.FloatField()
    loan_term = models.IntegerField()
    ai_explanation = models.TextField(null=True, blank=True)
    is_fraud = models.BooleanField(default=False)
    credit_history = models.IntegerField()
    ai_result = models.CharField(max_length=50)
    probability = models.FloatField()
    admin_decision = models.CharField(
    max_length=20,
    choices=[
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ],
    default='Pending'
)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.ai_result}"


# models.py
class LoanApplication(models.Model):
    applicant_income = models.FloatField()
    loan_amount = models.FloatField()
    probability = models.FloatField()
    ai_explanation = models.TextField(null=True, blank=True)
    is_fraud = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('AI_APPROVED', 'Approved by AI'),
        ('ADMIN_APPROVED', 'Approved by Admin'),
        ('REJECTED', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.loan_amount} - {self.status}"


from django.db import models
from django.contrib.auth.models import User


class MLModel(models.Model):
    file = models.FileField(upload_to="ml_models/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"
