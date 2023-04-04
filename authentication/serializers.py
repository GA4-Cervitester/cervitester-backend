from rest_framework import serializers


class PatientSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=30, min_length=2, allow_blank=False, trim_whitespace=True)
    name = serializers.CharField(
        max_length=30, min_length=2, allow_blank=False, trim_whitespace=True)
    phoneNumber = serializers.CharField(
        max_length=11, min_length=2, allow_blank=False, trim_whitespace=True)
    email = serializers.EmailField(allow_blank=False)
    dob = serializers.DateField()


class DoctorSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=30, min_length=2, allow_blank=False, trim_whitespace=True)
    name = serializers.CharField(
        max_length=30, min_length=2, allow_blank=False, trim_whitespace=True)
    phoneNumber = serializers.CharField(
        max_length=11, min_length=2, allow_blank=False, trim_whitespace=True)
    email = serializers.EmailField(allow_blank=False)
    dob = serializers.DateField()
