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


# def pretty_request(request):
#     headers = ''
#     for header, value in request.META.items():
#         if not header.startswith('HTTP'):
#             continue
#         header = '-'.join([h.capitalize()
#                           for h in header[5:].lower().split('_')])
#         headers += '{}: {}\n'.format(header, value)

#     return (
#         '{method} HTTP/1.1\n'
#         'Content-Length: {content_length}\n'
#         'Content-Type: {content_type}\n'
#         '{headers}\n\n'
#         '{body}'
#     ).format(
#         method=request.method,
#         content_length=request.META['CONTENT_LENGTH'],
#         content_type=request.META['CONTENT_TYPE'],
#         headers=headers,
#         body=request.body,
#     )


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
        if (request.data.get('test_type') == "0"):
            normal_Count, rounded_ratio, abnormal_Count = runDetection(
                request.data.get('test_type'))
            # modelFeedback = normal count , model_version = rounded ratio

            record = Record(
                patient=request.user.patient,
                photoUri=url,
                # modelFeedback=True if modelFeedback[0] > modelFeedback[1] else False
                # modelFeedback=modelFeedback,
                normalCount=normal_Count,
                roundedRatio=rounded_ratio,
                abnormalCount=abnormal_Count
            )
            # printable = pretty_request(request)
            print(record)
            testtype = request.data.get('test_type')
            print(testtype)
            record.save()
            record_serializer = RecordSerializer(instance=record)
        elif (request.data.get('test_type') == "1"):
            resultArray = runDetection(request.data.get('test_type'))

            record = Record(
                patient=request.user.patient,
                photoUri=url,
                modelFeedback=True if resultArray[0] > resultArray[1] else False
                # modelFeedback=modelFeedback,
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
        # model_result, model_version = runDetection()
        normal_Count, rounded_ratio, abnormal_Count = runDetection()
        chat = Chat(patient=patient, doctor=request.user.doctor)
        chat.save()
        record = Record(
            patient=patient,
            doctor=request.user.doctor,
            photoUri=url,
            normalCount=normal_Count,
            roundedRatio=rounded_ratio,
            abnormalCount=abnormal_Count,
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
