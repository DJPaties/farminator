from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers as django_serializers
from .serializer import FarmSerializer
from .models import Farm
import json



class FarmGetAll(APIView):
    def get(self, request):
        farms = Farm.objects.all()
        farms = [farm.serialize() for farm in farms]
        return Response({
            'success': True,
            "data": farms
        })
class FarmCreate(APIView):
    def post(self, request):
        serializer = FarmSerializer(data=request.data)

        if serializer.is_valid():
            farm = serializer.save()
            request.data.pop('conditions')
            data = {
                "success": True,
                "data": request.data
            }
            # data['data'].pop('conditions')
        else:
            data = {
                "success": True,
                "message": serializer.errors["non_field_errors"][0]
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
            'success':True
        })


