from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status

from .models import Message, Chat
from helpers import getUserType


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def MessagesView(request):
    id = request.data.get('id')
    messages = Chat.objects.get(pk=id).message_set.all()
    return response.Response({'messages': messages.values()})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddMessageView(request):
    chatId = request.data.get('id')
    message = request.data.get('message')
    userType = getUserType(request.user)
    chat = Chat.objects.get(pk=chatId)
    messageObj = Message(message=message, chat=chat, sender=userType)
    messageObj.save()
    return response.Response({'message': 'message added'})
