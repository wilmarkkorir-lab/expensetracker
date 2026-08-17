from django.contrib import admin
from transactions.models import Expense, Income


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "payment_method", "date")
    list_filter = ("payment_method", "date", "category")
    search_fields = ("note", "user__username")


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("user", "source", "amount", "date")
    list_filter = ("date",)
    search_fields = ("source", "user__username")
