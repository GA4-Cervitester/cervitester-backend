from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, serializers, status
from authentication.models import Patient, Doctor
from request.serializers import RequestSerializer
from .models import Request
from detection.models import Record
from chat.models import Chat
from helpers import getUserType


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddRequestView(request):
    user_type = getUserType(request.user)
    if user_type != 'patient':
        return response.Response({'error': 'not allowed'}, status.HTTP_403_FORBIDDEN)
    try:
        patient = request.data.get('patient')
        doctor = request.data.get('doctor')
        note = request.data.get('note')
        record = request.data.get('record')
        record = Record.objects.get(pk=record)
        patient = Patient.objects.get(pk=patient)
        doctor = Doctor.objects.get(pk=doctor)
        requestObject = Request(patient=patient, doctor=doctor, note=note,record=record)
        requestObject.save()
        serializer = RequestSerializer(instance=requestObject)
        return response.Response({'message': serializer.data})
    except Patient.DoesNotExist:
        return response.Response({'error': "Patient doesn't exists"}, status.HTTP_400_BAD_REQUEST)
    except Doctor.DoesNotExist:
        return response.Response({'error': "Doctor doesn't exists"}, status.HTTP_400_BAD_REQUEST)
    except Record.DoesNotExist:
        return response.Response({'error': "Record doesn't exists"}, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRequestsView(request):
    user_type = getUserType(request.user)
    user = None
    if user_type == 'patient':
        user = request.user.patient
    elif user_type == 'doctor':
        user = request.user.doctor
    else:
        return response.Response({'error': 'not allowed'}, status.HTTP_403_FORBIDDEN)
    requests = user.request_set.all()
    return response.Response({'requests': requests.values()})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRequestByIdView(request, id):
    user_type = getUserType(request.user)
    user = None
    if user_type == 'patient':
        user = request.user.patient
    elif user_type == 'doctor':
        user = request.user.doctor
    else:
        return response.Response({'error': 'not allowed'}, status.HTTP_403_FORBIDDEN)
    try:
        requestObject = user.request_set.get(pk=id)
        serializer = RequestSerializer(instance=requestObject)
        return response.Response({'message': serializer.data})
    except Request.DoesNotExist:
        return response.Response({'error': "Request doesn't exists"}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateRequestView(request):
    id = request.data.get('requestId')
    status = request.data.get('status')
    user_type = getUserType(request.user)
    if user_type != 'doctor':
        return response.Response({'error': 'not allowed'}, status.HTTP_403_FORBIDDEN)
    requestObject = request.user.doctor.request_set.get(pk=id)
    requestObject.status = status
    requestObject.save()
    serializer = RequestSerializer(instance=requestObject)
    return response.Response({'message': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RespondRequestView(request):
    id = request.data.get('id')
    res = request.data.get('response')
    user_type = getUserType(request.user)
    if user_type != 'doctor':
        return response.Response({'error': 'not allowed'}, status.HTTP_403_FORBIDDEN)
    requestObj = Request.objects.get(pk=id)
    requestObj.status= "yes" if res== 1 else "no"
    requestObj.save()
    if res != 1:
        return response.Response({'message':'request denied'})
    requestObj.record.doctor = requestObj.doctor
    chat = Chat(patient=requestObj.patient, doctor=requestObj.doctor)
    chat.save()
    requestObj.record.chat = chat
    requestObj.record.save()
    return response.Response({'message':'request success'})
