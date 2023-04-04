from django.db import models
from django.contrib.auth.models import User


class Admin(models.Model):
    name = models.CharField(null=False, max_length=30)
    phoneNumber = models.CharField(max_length=11)
    email = models.EmailField(null=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
