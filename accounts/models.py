from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    default_currency = models.CharField(max_length=3, default="KES")

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
