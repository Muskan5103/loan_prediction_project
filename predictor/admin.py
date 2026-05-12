from django.contrib import admin
from .models import LoanApplication


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'loan_amount',
        'probability',
        'status',
        'admin',
        'created_at',
    )

    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)