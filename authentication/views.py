from django.db import utils
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status
from authentication.serializers import DoctorSerializer, PatientSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import Doctor, Patient
from helpers import getUserType


@api_view(['POST'])
def RegisterView(request, type):
    if type == "patient":
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            try:
                name = serializer.validated_data.get('name')
                phoneNumber = serializer.validated_data.get('phoneNumber')
                email = serializer.validated_data.get('email')
                dob = serializer.validated_data.get('dob')
                user = User.objects.create_user(
                    username=email, password=serializer.validated_data.get('password'), email=serializer.validated_data.get('password'))
                patient = Patient.objects.create(
                    name=name,
                    email=email,
                    dob=dob,
                    user=user,
                    phoneNumber=phoneNumber)
                patient.save()
                refresh = RefreshToken.for_user(user)
                send_mail('Welcome to Cervi-Tester', 'Welcome to cervi-tester app', 'suyashsonawane005@gmail.com',
                          [email],  fail_silently=False,)
                return response.Response({"message": serializer.data, 'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
            except utils.IntegrityError as ex:
                print(ex)
                return response.Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return response.Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif type == "doctor":
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                name = serializer.validated_data.get('name')
                phoneNumber = serializer.validated_data.get('phoneNumber')
                email = serializer.validated_data.get('email')
                dob = serializer.validated_data.get('dob')
                user = User.objects.create_user(
                    username=email, password=serializer.validated_data.get('password'), email=serializer.validated_data.get('password'))
                doctor = Doctor.objects.create(
                    name=name,
                    email=email,
                    dob=dob,
                    user=user,
                    phoneNumber=phoneNumber)
                doctor.save()
                send_mail('Welcome Doctor to Cervi-Tester', 'Welcome to cervi-tester app, your account will be reviewed by our admin and you will receive once it is approved', 'suyashsonawane005@gmail.com',
                          [email],  fail_silently=False,)
                return response.Response({"message": serializer.data}, status=status.HTTP_200_OK)
            except utils.IntegrityError as ex:
                return response.Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif type == "worker":
        print("worker")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProfileInfoView(request):
    user_type = getUserType(request.user)
    content = {}
    user = None
    if user_type == 'patient':
        user = request.user.patient
    elif user_type == 'doctor':
        user = request.user.doctor
    elif user_type == 'admin':
        user = request.user.admin
    if user is not None:
        content = {
            'name': user.name,
            'dob': "" if user_type == "admin" else user.dob,
            'email': user.email,
            'phoneNumber': user.phoneNumber
        }
        return response.Response(content)
    return response.Response({'error': 'invalid user'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def getToken(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    user_type = getUserType(user)
    if user_type == 'doctor':
        if not user.doctor.isVerified:
            return response.Response({'error': 'not verified'}, status.HTTP_400_BAD_REQUEST)
        if user.doctor.disabled:
            return response.Response({'error': 'account disabled'}, status.HTTP_400_BAD_REQUEST)
    if user_type is None:
        return response.Response({'error': 'invalid credentials'}, status.HTTP_400_BAD_REQUEST)
    if user_type == 'patient' and user.patient.disabled:
        return response.Response({'error': 'account disabled'}, status.HTTP_400_BAD_REQUEST)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return response.Response({
            'access': str(refresh.access_token),
            'user_type': user_type
        })

    return response.Response({'error': 'invalid data'}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getPatient(request):
    user = getUserType(request.user)
    if user == 'doctor':
        phoneNumber = request.data.get('phoneNumber')
        patients = Patient.objects.filter(phoneNumber=phoneNumber)
        return response.Response({"patient": patients.values()}, status=status.HTTP_200_OK)
    else:
        return response.Response({"error": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDoctors(request):
    doctors = Doctor.objects.filter(isVerified=True, disabled=False)
    return response.Response({"doctors": doctors.values()}, status=status.HTTP_200_OK)
