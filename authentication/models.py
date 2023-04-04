from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    name = models.CharField(null=False, max_length=30)
    phoneNumber = models.CharField(max_length=11, unique=True)
    email = models.EmailField(null=False)
    dob = models.DateField(null=False)
    disabled = models.BooleanField(default=False)
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, primary_key=True)


class Doctor(models.Model):
    name = models.CharField(null=False, max_length=30)
    phoneNumber = models.CharField(max_length=11, unique=True)
    email = models.EmailField(null=False)
    dob = models.DateField(null=False)
    isVerified = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, primary_key=True)

    def __str__(self) -> str:
        return self.name
