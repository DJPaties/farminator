from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers as django_serializers
from .serializer import FarmSerializer
from .models import Farm
from customUsers.models import CustomToken
import json


class FarmGetAll(APIView):
    def get(self, request):
        farms = Farm.objects.all()
        farms = [farm.serialize() for farm in farms]
        return Response({
            'success': True,
            "data": farms
        })


class FarmGetUser(APIView):
    def get(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        user_id = CustomToken.objects.get(token=token).custom_user_id
        farms = Farm.objects.filter(user_id=user_id)
        farms = [farm.serialize() for farm in farms]

        return Response({
            'success': True,
            'data': farms,
        })


class FarmCreate(APIView):
    def post(self, request):
        # token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        # user_id = CustomToken.objects.get(token=token).custom_user_id
        
        print(request.data['conditions'])
        serializer = FarmSerializer(data=request.data)

        if serializer.is_valid():
            farm = serializer.save()
            # request.data.pop('conditions')
            data = {
                "success": True,
                "data": request.data
            }
            # data['data'].pop('conditions')
        else:
            data = {
                "success": True,
                "message": serializer.errors
            }
        return Response(data)


class FarmEdit(APIView):
    def post(self, request):
        serializer = FarmSerializer(data=request.data)
        old_farm = Farm.objects.filter(id=request.data['id'])
        if serializer.is_valid() and old_farm:
            print("VALID")
            serializer.update(old_farm[0], request.data)
        else:
            print(serializer.errors)

        return Response({
            'success': True
        })
