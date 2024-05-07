from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializer import RemoteSystemRegisterSerializer

from rest_framework.views import APIView
from .models import RemoteSystemRegister

token_raspi = None
instantData = {}
class AuthenticateSystem(APIView):
    def post(self,request):
        token = request.data['token']
        
        try:
            # Attempt to retrieve a RemoteSystemRegister instance with the provided token
            system = RemoteSystemRegister.objects.get(custom_token=token)
        except RemoteSystemRegister.DoesNotExist:
            # Return error response if the system with the token does not exist
            return Response({'success': False }, status=status.HTTP_404_NOT_FOUND)

        # If the system with the token exists, serialize it and return the serialized data
        serializer = RemoteSystemRegisterSerializer(system)
        return Response({'success':True})
        

class RegisterSystem(APIView):
    def post(self, request):
        token = request.data['token']
        try:
            check_system = RemoteSystemRegister.objects.get(custom_token=token)
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
        except RemoteSystemRegister.DoesNotExist:
            check_system=RemoteSystemRegister.objects.create(custom_token=token)
            if check_system:
                return Response({"success":True}, status=status.HTTP_201_CREATED)
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

class CheckFlagSystem(APIView):
    def post(self,request):
        return Response({"token_system":token_raspi},status=status.HTTP_200_OK)

class CheckRemoteSystem(APIView):
    def post(self,request):
        global token_raspi
        token_raspi = request.data['token_system']
        token_check = request.data['token_system']
        while True:
            if 'token_system' in instantData:
                if token_check == instantData['token_system']:
                    break
        
                else:
                    continue
        return Response({instantData},status=status.HTTP_200_OK)
        
        
class GetInstantDataSystem(APIView):
    def post(self,request):
        global instantData
        instantData = request.data
        return Response({'success':True},status=status.HTTP_200_OK)
        

        
        