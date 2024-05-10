from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import CustomUser


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        data = {}
        if (serializer.is_valid()):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = request.data
            data._mutable = True
            data['id'] = user.id
            data['email'] = user.email
            data['token'] = token.key
            data.pop('password')
            return Response({
                'success': True,
                'data': data,
            })
        return Response({
            'error': True,
            'message': serializer.errors
        })


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,
                             "message": "You Have Registed Successfully", }, status=status.HTTP_201_CREATED)
        return Response({"error": True,
                         "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the token associated with the user
        token = Token.objects.get(user=request.user)
        # Delete the token
        token.delete()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
