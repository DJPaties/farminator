from rest_framework import serializers
from .models import Notification, CustomUser, Farm


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=10000)
    user_id = serializers.CharField(max_length=255)
    farm_id = serializers.CharField(max_length=255)

    def validate(self, attrs):
        user = CustomUser.objects.filter(id=attrs['user_id'])
        farm = Farm.objects.filter(id=attrs['farm_id'])
        print(user)
        if not user:
            raise serializers.ValidationError(
                "User Not Found, Please Login")
        if not farm:
            raise serializers.ValidationError(
                'Farm Not Found, Please Check again Later or With Support')
        attrs['user_id'] = user[0]
        attrs['farm_id'] = farm[0]
        return attrs

    def create(self, validated_data):
        try:
            print(validated_data['user_id'])
            notification = Notification.objects.create(
                title=validated_data['title'],
                description=validated_data['description'],
                user_id=validated_data['user_id'],
                farm_id=validated_data['farm_id'],
            )
            print("damn")
        except:
            notification.delete()
        return notification
