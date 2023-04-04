import base64
import re
import datetime
import threading
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, serializers, status

from detection.serializers import RecordSerializer
from helpers import getUserType
from .aiDetection import runDetection
from .models import Record
from .firebase import storage
from authentication.models import Patient
from chat.models import Chat


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def FileUploadView(request):
    file = request.data.get('file')
    file = re.sub('^data:image/.+;base64,', '', file)
    image_64_decode = base64.b64decode(file)
    image_result = open('image.jpg', 'wb')
    ts = datetime.datetime.now().timestamp()
    image_result.write(image_64_decode)
    storage.child(f"/record-annotations/{ts}").put("image.jpg")
    url = storage.child(f"/record-annotations/{ts}").get_url(None)
    return response.Response({"url": url})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def OperatorView(request):
    user = getUserType(request.user)
    if user == "patient":
        file = request.data.get('file')
        file = re.sub('^data:image/.+;base64,', '', file)
        image_64_decode = base64.b64decode(file)
        image_result = open('image.jpg', 'wb')
        ts = datetime.datetime.now().timestamp()
        image_result.write(image_64_decode)
        storage.child(f"/record-annotations/{ts}").put("image.jpg")
        url = storage.child(f"/record-annotations/{ts}").get_url(None)
        model_result,model_version = runDetection()
        record = Record(
            patient=request.user.patient,
            photoUri=url,
            modelVersion=model_version,
            modelFeedback=True if model_result == [0.] else False
        )
        record.save()
        record_serializer = RecordSerializer(instance=record)
        # detectionThread = threading.Thread(target=runDetection)
        # detectionThread.start()
        return response.Response({"record": record_serializer.data}, status=status.HTTP_200_OK)
    elif user == 'doctor':
        patient_id = request.data.get('patient_id')
        patient = Patient.objects.get(pk=patient_id)
        file = request.data.get('file')
        file = re.sub('^data:image/.+;base64,', '', file)
        image_64_decode = base64.b64decode(file)
        image_result = open('image.jpg', 'wb')
        ts = datetime.datetime.now().timestamp()
        image_result.write(image_64_decode)
        storage.child(f"/record-annotations/{ts}").put("image.jpg")
        url = storage.child(f"/record-annotations/{ts}").get_url(None)
        model_result,model_version = runDetection()
        chat = Chat(patient=patient, doctor=request.user.doctor)
        chat.save()
        record = Record(
            patient=patient,
            doctor=request.user.doctor,
            photoUri=url,
            modelVersion=model_version,
            modelFeedback=True if model_result == 0 else False,
            chat=chat
        )
        record.save()
        record_serializer = RecordSerializer(instance=record)
        return response.Response({"record": record_serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RecordsView(request):
    user = getUserType(request.user)
    records = []
    if user == 'patient':
        records = request.user.patient.record_set.all()
    elif user == 'doctor':
        records = request.user.doctor.record_set.all()
    records = RecordSerializer(records, many=True)
    return response.Response({"records": records.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AnnotationView(request):
    file = request.data.get('file')
    file = re.sub('^data:image/.+;base64,', '', file)
    image_64_decode = base64.b64decode(file)
    image_result = open('image.jpg', 'wb')
    ts = datetime.datetime.now().timestamp()
    image_result.write(image_64_decode)
    storage.child(f"/record-annotations/{ts}").put("image.jpg")
    url = storage.child(f"/record-annotations/{ts}").get_url(None)
    recordId = request.data.get('record_id')
    record = Record.objects.get(pk=recordId)
    record.annotationUri = url
    record.save()
    serializer = RecordSerializer(instance=record)
    return response.Response({'message': 'Annotation Added', 'record': serializer.data})
