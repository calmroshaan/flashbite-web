from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('store_owner', 'Store Owner'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="+92XXXXXXXXXX")
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"