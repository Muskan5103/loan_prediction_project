from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LoanApplication
from django.contrib.auth.models import User

# Example Audit Log model (if you create one)
# from .models import AuditLog

@receiver(post_save, sender=LoanApplication)
def log_application(sender, instance, created, **kwargs):
    if created:
        print(f"New Loan Application Created by {instance.user}")

    else:
        print(f"Loan Application Updated (ID: {instance.id})")