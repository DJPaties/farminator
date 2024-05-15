from .models import Reminder
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import ReminderSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class ReminderGetUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reminders = Reminder.objects.filter(user_id=user.id)
        reminders = [reminder.serilize() for reminder in reminders]

        return Response({
            'success': True,
            'data': reminders,
        })

class ReminderCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        requestData = request.data
        requestData._mutable = True
        requestData['user_id'] = request.user.id
        serilizer = ReminderSerializer(data=request.data)
        if (serilizer.is_valid()):
            serilizer.save()
            data = {
                'success': True,
                'data': requestData
            }
        else:
            data = {
                'error':True,
                'message': serilizer.errors
            }
        return Response(data)
        

def reminderSendNotification():
    print("hello")