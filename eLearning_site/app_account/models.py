from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountProfile(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_profile")

    acc_types = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    ]
    account_type = models.CharField(max_length=64, choices=acc_types, default='Student')
    acc_name = models.CharField(max_length=264, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)