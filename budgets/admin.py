from django.contrib import admin
from budgets.models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "period", "limit_amount")
    list_filter = ("period",)
    search_fields = ("category__name", "user__username")
