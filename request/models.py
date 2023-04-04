from django.db import models

from authentication.models import Doctor, Patient
from detection.models import Record


class Request(models.Model):
    createdTs = models.DateTimeField(auto_now_add=True)
    updatedTs = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    record = models.ForeignKey(Record, on_delete=models.DO_NOTHING,null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    # open | fullfield
    status = models.CharField(max_length=20, default="open")
    note = models.TextField(null=True)
