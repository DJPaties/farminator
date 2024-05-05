from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers as django_serializers
from .serializer import FarmSerializer
from .models import Farm
import json


class FarmCreate(APIView):
    def post(self, request):
        serializer = FarmSerializer(data=request.data)

        if serializer.is_valid():
            farm = serializer.save()
            if request.data['conditions'] != {}:
                serializer.update(farm, request.data)

            data = {
                "success": True,
                "data": request.data
            }
            data['data'].pop('conditions')
        else:
            data = {
                "success": True,
                "message": serializer.errors["non_field_errors"][0]
            }
        return Response(data)


class FarmGetAll(APIView):
    def get(self, request):
        farms = Farm.objects.all()
        farms = [farm.serialize() for farm in farms]
        return Response({
            'success': True,
            "data": farms
        })
