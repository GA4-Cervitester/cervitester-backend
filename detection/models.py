from django.db import models
from django.db.models.deletion import DO_NOTHING

from authentication.models import Doctor, Patient
from chat.models import Chat


class Record(models.Model):
    createdTs = models.DateTimeField(auto_now_add=True)
    updatedTs = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    photoUri = models.URLField(null=True)
    annotationUri = models.URLField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True)
    result = models.BooleanField(null=True)
    # open | active | resolved
    status = models.CharField(max_length=20, default="open")
    chat = models.ForeignKey(Chat, on_delete=DO_NOTHING, null=True)
    modelFeedback = models.BooleanField(null=True)
    modelVersion = models.CharField(max_length=20)

class Model(models.Model):
    createdTs = models.DateTimeField(auto_now_add=True)
    updatedTs = models.DateTimeField(auto_now=True)
    model_id = models.CharField(max_length=20,unique=True)
    active = models.BooleanField(default=False)