from django.db import models
from accounts.models import User


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="categories")
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=30, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "categories"
        unique_together = ("user", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name
