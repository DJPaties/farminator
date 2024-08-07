from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializer import RemoteSystemRegisterSerializer

from rest_framework.views import APIView
from .models import RemoteSystemRegister
import json
token_raspi = None
instantData = {}
control_list = {}
control_flag = False
data_flag = False
executed_flag = False
condition_flag=False
condition_list={}
saved_condition_flag = False

class CheckConditionSystem(APIView):
    def post(self, request):
        global token_raspi
        global saved_condition_flag
        global data_flag
        global condition_list
        global condition_flag
        system = RemoteSystemRegister.objects.get(
            id=request.data['product_id'])
        token_raspi = system.custom_token
        token_check = system.custom_token
        # data_flag = request.data['data_flag']
        condition_list = request.data['condition_list']
        condition_flag = request.data['condition_flag']
        while not saved_condition_flag:
            pass
        saved_condition_flag = False
        condition_flag = False
        condition_list = {}
        return Response({"success":True,
                         "message": "Conditions Set Successfully"},status=status.HTTP_200_OK)
        
class ConditionSet(APIView):
    def post(self, request):
        global saved_condition_flag
        saved_condition_flag = request.data['saved_condition_flag']
        return Response({'success': True}, status=status.HTTP_200_OK)

class ControlExecute(APIView):
    def post(self, request):
        global executed_flag
        executed_flag = request.data['executed_flag']
        return Response({'success': True}, status=status.HTTP_200_OK)

class AuthenticateSystem(APIView):
    def post(self, request):
        token = request.data['token']

        try:
            # Attempt to retrieve a RemoteSystemRegister instance with the provided token
            system = RemoteSystemRegister.objects.get(custom_token=token)
        except RemoteSystemRegister.DoesNotExist:
            # Return error response if the system with the token does not exist
            return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)

        # If the system with the token exists, serialize it and return the serialized data
        serializer = RemoteSystemRegisterSerializer(system)
        return Response({'success': True})


class RegisterSystem(APIView):
    def post(self, request):
        token = request.data['token']
        try:
            check_system = RemoteSystemRegister.objects.get(custom_token=token)
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        except RemoteSystemRegister.DoesNotExist:
            check_system = RemoteSystemRegister.objects.create(
                custom_token=token)
            if check_system:
                serilized_system = RemoteSystemRegisterSerializer(check_system)
                # if serilized_system.is_valid():
                return Response({"success": True, "data": serilized_system.data}, status=status.HTTP_201_CREATED)
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


class CheckFlagSystem(APIView):
    def post(self, request):
        global token_raspi
        global control_list
        global control_flag
        global data_flag
        global condition_flag
        global condition_list
        data = {"token_system": token_raspi,
                "data_flag": data_flag,
                'control_flag': control_flag,
                'control_list': control_list,
                'condition_flag': condition_flag,
                'condition_list': condition_list
                }
        token_raspi = None
        control_flag = False
        data_flag = False
        control_list = {}
        return Response({json.dumps(data)
                         }, status=status.HTTP_200_OK)


class CheckRemoteSystem(APIView):
    def post(self, request):
        global token_raspi
        global instantData
        global data_flag
        global control_list
        instantData = {}
        system = RemoteSystemRegister.objects.get(
            id=request.data['farm_product_id'])
        token_raspi = system.custom_token
        token_check = system.custom_token
        data_flag = request.data['data_flag']
        control_list = request.data['control_list']
        print(control_list)
        while True:
            if 'token_system' in instantData:
                if token_check == instantData['token_system']:
                    break

                else:
                    continue
        token_raspi = None

        return Response({json.dumps(instantData)}, status=status.HTTP_200_OK)


class CheckControlSystem(APIView):
    def post(self, request):
        global token_raspi
        global control_list
        global control_flag
        global executed_flag
        print(request.data['product_id'])
        system = RemoteSystemRegister.objects.get(
            id=request.data['product_id'])
        token_raspi = system.custom_token
        token_check = system.custom_token
        control_flag = request.data['control_flag']
        control_list = request.data['control_list']
        # while True:
        #     if 'token_system' in control_list:
        #         if token_check == control_list['token_system']:
        #             break

        #         else:
        #             continue
        # token_raspi = None
        # control_flag = False
        # return Response({json.dumps(control_list)}, status=status.HTTP_200_OK)
        while not executed_flag:
            pass
        executed_flag = False
        return Response({'success':True,
                         'message': "Executed Control"}, status=status.HTTP_200_OK)


class GetInstantDataSystem(APIView):
    def post(self, request):
        global instantData
        instantData = request.data
        return Response({'success': True}, status=status.HTTP_200_OK)
