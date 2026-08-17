from decimal import Decimal
from django.db import models
from accounts.models import User
from categories.models import Category


PERIOD_CHOICES = [
    ("daily", "Daily"),
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
]


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "budgets"
        unique_together = ("user", "category", "period")
        ordering = ["period", "category__name"]

    def __str__(self):
        return f"{self.category.name} - {self.period} ({self.limit_amount})"
