from django.db import models
from accounts.models import User


TYPE_CHOICES = [
    ("budget_warning", "Budget Warning"),
    ("budget_exceeded", "Budget Exceeded"),
    ("goal_on_track", "Goal On Track"),
    ("goal_at_risk", "Goal At Risk"),
    ("no_activity", "No Activity Reminder"),
]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.type}"
