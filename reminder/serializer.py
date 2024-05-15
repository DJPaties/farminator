from rest_framework import serializers
from .models import Reminder, CustomUser, Farm


class ReminderSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=10000)
    user_id = serializers.CharField(max_length=255)
    farm_id = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)
    date_time = serializers.DateTimeField()

    def validate(self, attrs):
        user = CustomUser.objects.filter(id=attrs['user_id'])
        farm = Farm.objects.filter(id=attrs['farm_id'])
        if not user:
            raise serializers.ValidationError(
                "User Not Found, Please Login")
        if not farm:
            raise serializers.ValidationError(
                'Farm Not Found, Please Check again Later or With Support')
        attrs['user'] = user[0]
        attrs['farm'] = farm[0]
        return attrs

    def create(self, validated_data):
        try:
            reminder = Reminder.objects.create(
                description=validated_data['description'],
                user=validated_data['user'],
                farm=validated_data['farm'],
                type=validated_data['type'],
                date_time=validated_data['date_time'],
            )
        except:
            reminder.delete()
        return reminder
