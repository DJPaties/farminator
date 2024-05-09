from rest_framework import serializers
from users.serializers import UserRegistrationSerializer
from .models import RemoteSystemRegister

class RemoteSystemRegisterSerializer(serializers.ModelSerializer):
    user_id_connected = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = RemoteSystemRegister
        fields = ('id', 'custom_token', 'user_id_connected')
