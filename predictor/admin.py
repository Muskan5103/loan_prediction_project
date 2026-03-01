from django.contrib import admin
from .models import LoanHistory


@admin.register(LoanHistory)
class LoanHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'loan_amount',
        'ai_result',
        'probability',
        'admin_decision',
    )

    list_filter = ('admin_decision',)
    search_fields = ('user__username',)
