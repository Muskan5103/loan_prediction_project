from django.db import models
from django.contrib.auth.models import User


class LoanApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ai_result = models.CharField(max_length=50)
    applicant_income = models.FloatField()
    coapplicant_income = models.FloatField(null=True, blank=True)
    loan_amount = models.FloatField()
    loan_term = models.IntegerField()
    credit_history = models.IntegerField()

    probability = models.FloatField()
    ai_explanation = models.TextField(null=True, blank=True)
    fraud_reason = models.TextField(null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_loans')
    admin_note = models.TextField(null=True, blank=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('AI_APPROVED', 'Approved by AI'),
        ('ADMIN_APPROVED', 'Approved by Admin'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    document = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    def __str__(self):
        return f"{self.user} - {self.status}"

from django.db import models
from django.contrib.auth.models import User


class MLModel(models.Model):
    file = models.FileField(upload_to="ml_models/")
    version = models.CharField(max_length=20)
    accuracy = models.FloatField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            MLModel.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file.name} (v{self.version})"


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"


