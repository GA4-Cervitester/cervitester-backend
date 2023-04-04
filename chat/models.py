from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

from authentication.models import Doctor, Patient


class Chat(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=DO_NOTHING)
    patient = models.ForeignKey(Patient, on_delete=DO_NOTHING)


class Message(models.Model):
    createdTs = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=CASCADE, null=True)
    # doctor | patient
    sender = models.CharField(max_length=10)
