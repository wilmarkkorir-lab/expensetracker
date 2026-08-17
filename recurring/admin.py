from django.contrib import admin
from recurring.models import RecurringExpense


@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "frequency", "next_due_date", "is_active")
    list_filter = ("frequency", "is_active")
    search_fields = ("category__name", "user__username")
