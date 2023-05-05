from django.db import utils
from rest_framework.permissions import IsAuthenticated
from admin.models import Admin
from rest_framework import response, status
from django.contrib.auth.models import User
from admin.serializers import AdminSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from detection.models import Model, Record
from authentication.models import Patient, Doctor
from detection.serializers import RecordSerializer
from helpers import getUserType


@api_view(['POST'])
def RegisterView(request):
    serializer = AdminSerializer(data=request.data)
    key = request.data.get('key')
    if key != "wubba lubba dub dub" or key is None:
        return response.Response({'error': 'not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    if serializer.is_valid():
        try:
            name = serializer.validated_data.get('name')
            phoneNumber = serializer.validated_data.get('phoneNumber')
            email = serializer.validated_data.get('email')
            user = User.objects.create_user(
                username=email, password=serializer.validated_data.get('password'), email=serializer.validated_data.get('password'))
            admin = Admin.objects.create(
                name=name,
                email=email,
                user=user,
                phoneNumber=phoneNumber)
            admin.save()
            refresh = RefreshToken.for_user(user)
            return response.Response({"message": serializer.data, 'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        except utils.IntegrityError as ex:
            return response.Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return response.Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDataView(request):
    if getUserType(request.user) != "admin":
        return response.Response({'error': 'not allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    patients = Patient.objects.all().values()
    doctors = Doctor.objects.all().values()
    records = RecordSerializer(Record.objects.all(), many=True).data
    models = Model.objects.all().values()
    return response.Response({'patients': patients, 'doctors': doctors, 'records': records, 'models': models})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VerifyDoctor(request):
    id = request.data.get('id')
    if id is None:
        return response.Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        request.user.admin
        doctor = Doctor.objects.get(pk=id)
        doctor.isVerified = True
        doctor.save()
        send_mail('Account Verified', 'Greetings, we have successfully verified your account you can processed to log into your account.', 'domain.cervitester@gmail.com',
                  [doctor.email],  fail_silently=False,)
        return response.Response({'message': 'doctor verified'}, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        return response.Response({'error': 'not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    except Doctor.DoesNotExist:
        return response.Response({'error': "doctor does'nt exists"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DisableUserView(request):
    if getUserType(request.user) != "admin":
        return response.Response({'error': 'not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    id = request.data.get('id')
    if id is None:
        return response.Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(pk=id)
    user_type = getUserType(user)
    if user_type == 'patient':
        user.patient.disabled = True
        user.patient.save()
    elif user_type == 'doctor':
        user.doctor.disabled = True
        user.doctor.save()

    return response.Response({'message': 'user disabled'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EnableUserView(request):
    if getUserType(request.user) != "admin":
        return response.Response({'error': 'not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    id = request.data.get('id')
    if id is None:
        return response.Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(pk=id)
    user_type = getUserType(user)
    if user_type == 'patient':
        user.patient.disabled = False
        user.patient.save()
    elif user_type == 'doctor':
        user.doctor.disabled = False
        user.doctor.save()

    return response.Response({'message': 'user enabled'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddModelView(request):
    if getUserType(request.user) != "admin":
        return response.Response({'error': 'not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    model_id = request.data.get('model_id')
    active = request.data.get('active')

    if model_id is None:
        return response.Response({'error': 'model_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    active = False if active is None else active
    model = Model(model_id=model_id, active=active)
    try:
        model.save()
    except utils.IntegrityError as e:
        return response.Response({'error': 'model_id already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if (model.active):
        for m in Model.objects.filter(active=True):
            if m.model_id == model_id:
                continue
            m.active = False
            m.save()

    return response.Response({'message': 'model added successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SetActiveModelView(request):
    if getUserType(request.user) != "admin":
        return response.Response({'error': 'not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    model_id = request.data.get('model_id')

    if model_id is None:
        return response.Response({'error': 'model_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    for m in Model.objects.filter(active=True):
        m.active = False
        m.save()

    try:
        model = Model.objects.get(model_id=model_id)
        model.active = True
        model.save()
    except Model.DoesNotExist:
        return response.Response({'error': 'model does not exists'}, status=status.HTTP_400_BAD_REQUEST)

    return response.Response({'message': 'active model updated successfully'}, status=status.HTTP_200_OK)
