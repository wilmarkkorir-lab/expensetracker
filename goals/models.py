from decimal import Decimal
from django.db import models
from accounts.models import User


PERIOD_CHOICES = [
    ("monthly", "Monthly"),
    ("yearly", "Yearly"),
]


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=100)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_achieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "goals"
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class GoalAllocation(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="allocations")
    label = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "goal_allocations"
        unique_together = ("goal", "label")

    def __str__(self):
        return f"{self.goal.name} - {self.label} ({self.percentage}%)"
