from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import NotificationSerializer
from rest_framework.authentication import TokenAuthentication
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification as noti
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from remoteSystem.models import RemoteSystemRegister
from farm.models import Farm
import json
# Create your views here.


class NotificationGetUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user_id=user.id)
        notifications = [notification.serialize()
                         for notification in notifications]
        return Response({
            'success': True,
            'data': notifications,
        })


class NotificationCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        requestData = request.data
        requestData._mutable = True
        requestData['user_id'] = request.user.id
        serializer = NotificationSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': True,
                'data': requestData
            }
            devices = FCMDevice.objects.filter(user=requestData['user_id'])
            devices.send_message(
                message=Message(
                    notification=noti(
                        title=requestData['title'],
                        body=requestData['description']
                    ),
                ),
            )
        else:
            data = {
                "error": True,
                'message': serializer.errors
            }
        return Response(data)
    
class CheckNotify(APIView):
    def post(self, request):
        remoteSystems = RemoteSystemRegister.objects.filter(custom_token=request.data['farm_token'])
        farm = Farm.objects.filter(product_id=remoteSystems[0].id)
        devices = FCMDevice.objects.filter(user_id=farm[0].user_id)
        print(request.data )
        message = json.loads(request.data['message'])
        print(message)
        for key in message:
            print(key)
            devices.send_message(
                message=Message(
                    notification=noti(
                        title="Condition/s Breached!",
                        body=message[key]
                    ),
                ),
            )
        #print(request.data['farm_token'])
        return Response({request.data['message']})
