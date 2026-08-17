from decimal import Decimal
from django.db import models
from accounts.models import User
from categories.models import Category


PAYMENT_METHODS = [
    ("cash", "Cash"),
    ("card", "Card"),
    ("mobile_money", "Mobile Money"),
]


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="cash")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "expenses"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.amount} {self.user.default_currency} - {self.category}"


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    class Meta:
        db_table = "incomes"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.amount} {self.user.default_currency} - {self.source}"
