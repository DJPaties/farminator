from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers as django_serializers
from .serializer import FarmSerializer
from .models import Farm, FarmConditions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
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


class FarmGetUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        farms = Farm.objects.filter(user_id=user.id)
        farms = [farm.serialize() for farm in farms]

        return Response({
            'success': True,
            'data': farms,
        })


class FarmCreate(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        requestData = request.data
        requestData._mutable = True
        requestData['user_id'] = request.user.id
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
            data['data']['image'] = "/".join(data['data']
                                             ['image'].split("/")[-2:])
            # data['data'].pop('conditions')
        else:
            data = {
                "error": True,
                "message": serializer.errors
            }
        return Response(data)


class FarmEdit(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        requestData = request.data
        requestData._mutable = True
        requestData['user_id'] = request.user.id
        old_farm = Farm.objects.filter(id=request.data['id'])

        if ('image' not in requestData.keys()):
            requestData['image'] = old_farm[0].image
        serializer = FarmSerializer(data=requestData)

        if serializer.is_valid() and old_farm:
            farm = serializer.update(old_farm[0], serializer.validated_data)
            requestData['id'] = farm.id
            requestData['image'] = farm.image.name

            data = {
                "success": True,
                "data": requestData
            }
            data['data']['image'] = "/".join(data['data']
                                             ['image'].split("/")[-2:])
            return Response({
                'success': True,
                'data': requestData,
            })
        else:
            print(serializer.errors)

        requestData.pop("conditions")
        return Response({
            'error': True,
            'message': serializer.errors
        })

    def get(self, request, farm_id):
        farm = Farm.objects.get(id=farm_id)
        conditons = FarmConditions.objects.filter(farm_id=farm_id)
        data = farm.serialize()
        data['conditions'] = [condition.serialize() for condition in conditons]

        return Response({
            'success': True,
            "data": data,
        })


class FarmDelete(APIView):
    def post(self, request):
        print(request.data)
        farm = Farm.objects.filter(id=request.data['id'])
        print(farm)
        if farm:
            farm.delete()
            return Response({
                'success': True,
                'message': 'Farm Deleted Successfully'
            })
        return Response({
            'error': True,
            'message': 'Farm Not Found!',
        })
