from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import NotificationSerializer
from rest_framework.authentication import TokenAuthentication
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification as noti
from rest_framework.permissions import IsAuthenticated
from .models import Notification

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
