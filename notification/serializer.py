from rest_framework import serializers
from .models import Notification, CustomUser


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=10000)
    user_id = serializers.CharField(max_length=255)

    def validate(self, attrs):
        user = CustomUser.objects.filter(id=attrs['user_id'])
        print(user)
        if not user:
            raise serializers.ValidationError(
                "User Not Found, Please Login")
        attrs['user_id'] = user[0]
        return attrs

    def create(self, validated_data):
        try:
            print(validated_data['user_id'])
            notification = Notification.objects.create(
                title=validated_data['title'],
                description=validated_data['description'],
                user_id=validated_data['user_id']
            )
            print("damn")
        except:
            notification.delete()
        return notification
