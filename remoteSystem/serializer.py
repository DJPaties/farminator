from rest_framework import serializers
from customUsers.serializer import CustomUserSerializer
from .models import RemoteSystemRegister

class RemoteSystemRegisterSerializer(serializers.ModelSerializer):
    user_id_connected = CustomUserSerializer(read_only=True)

    class Meta:
        model = RemoteSystemRegister
        fields = ('id', 'custom_token', 'user_id_connected')
