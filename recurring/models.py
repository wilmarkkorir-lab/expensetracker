from django.db import models
from accounts.models import User
from categories.models import Category


FREQUENCY_CHOICES = [
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("yearly", "Yearly"),
]


class RecurringExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recurring_expenses")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recurring_expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    next_due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "recurring_expenses"
        ordering = ["next_due_date"]

    def __str__(self):
        return f"{self.category.name} - {self.frequency} ({self.amount})"
