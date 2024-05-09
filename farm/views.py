from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers as django_serializers
from .serializer import FarmSerializer
from .models import Farm, FarmConditions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
import json


class FarmGetAll(APIView):
    def get(self, request):
        farms = Farm.objects.all()
        farms = [farm.serialize() for farm in farms]
        return Response({
            'success': True,
            "data": farms
        })


# class FarmGetUser(APIView):
#     def get(self, request):
#         token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
#         user_id = CustomToken.objects.get(token=token).custom_user_id
#         farms = Farm.objects.filter(user_id=user_id)
#         farms = [farm.serialize() for farm in farms]

#         return Response({
#             'success': True,
#             'data': farms,
#         })

class FarmGetUser(APIView):
    def get(self, request):
        user = request.user
        # user_id = CustomToken.objects.get(token=token).custom_user_id
        farms = Farm.objects.filter(user_id=user.id)
        farms = [farm.serialize() for farm in farms]

        return Response({
            'success': True,
            'data': farms,
        })


class FarmCreate(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        # token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
        # user_id = CustomToken.objects.get(token=
        serializer = FarmSerializer(data=request.data)

        if serializer.is_valid():
            requestData = request.data
            farm = serializer.save()

            requestData['id'] = farm.id
            requestData['image'] = farm.image.name

            data = {
                "success": True,
                "data": requestData
            }
            # data['data'].pop('conditions')
        else:
            data = {
                "error": True,
                "message": serializer.errors
            }
        return Response(data)


class FarmEdit(APIView):
    def post(self, request):
        serializer = FarmSerializer(data=request.data)
        old_farm = Farm.objects.filter(id=request.data['id'])
        if serializer.is_valid() and old_farm:
            serializer.update(old_farm[0], request.data)
        else:
            print(serializer.errors)

        requestData = request.data
        requestData.pop("conditions")
        return Response({
            'success': True,
            'data': requestData,

        })

    def get(self, request, farm_id):
        print(farm_id)
        farm = Farm.objects.get(id=farm_id)
        conditons = FarmConditions.objects.filter(farm_id_id=36)
        data = farm.serialize()

        data['conditions'] = [condition.serialize() for condition in conditons]

        return Response({
            'success': True,
            "data": data,
        })
