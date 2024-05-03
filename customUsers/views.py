
# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializer import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from .models import CustomUser, CustomToken


class CustomUserLogin(APIView):
    def post(self, request):

        custom_user = None

        try:
            custom_user = CustomUser.objects.get(
                username=request.data['username'])
        except CustomUser.DoesNotExist:
            return Response({"error": True, 'message': "Invalid Username or Password"}, status=status.HTTP_404_NOT_FOUND)

        # Validate password (you might want to use a secure password hashing mechanism here)
        if check_password(request.data['password'], custom_user.password):
            token_key = CustomToken.generate_token(custom_user)
            return Response({
                'success': True,
                'data': {
                    "token": token_key,
                    'username': custom_user.username,
                    'id': custom_user.id
                }}, status=status.HTTP_200_OK)
        else:
            return Response({"error": True, 'message': "Invalid Username or Password"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserLogout(APIView):
    def post(self, request):
        token = request.data['token']
        authenticated_token = CustomToken.objects.get(token=token)

        if authenticated_token:
            CustomToken.objects.get(token=token).delete()
            return Response({'success': True, 'message': "Logged out"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': True, 'message': "Token Invalid."}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserRegister(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        data = None
        if serializer.is_valid():
            custom_user = serializer.save()
            data = {
                'success': True,
                'message': "You Have registered succesffuly"
            }
        else:
            data = {
                'error': True,
                "message": serializer.errors["non_field_errors"][0]
            }

        return Response(data)


class CustomUserValidateToken(APIView):
    def post(self, request):
        custom_user = None

        try:
            custom_Token = CustomToken.objects.get(token=request.data['token'])
            custom_user = CustomUser.objects.get(
                id=custom_Token.custom_user_id)

            return Response({
                'success': True,
                'data': {
                    "token": request.data['token'],
                    'username': custom_user.username,
                    'id': custom_user.id
                }}, status=status.HTTP_200_OK)
        except CustomToken.DoesNotExist:
            return Response({"error": True, 'message': "Unauthorized Token."}, status=status.HTTP_404_NOT_FOUND)
