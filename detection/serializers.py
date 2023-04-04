from rest_framework import serializers
from .models import Record
from authentication.models import Doctor, Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('name', 'email', 'phoneNumber', 'user_id')


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('name', 'email', 'phoneNumber', 'user_id')


class RecordSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(many=False)
    patient = PatientSerializer(many=False)

    class Meta:
        model = Record
        fields = "__all__"
