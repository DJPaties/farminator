from rest_framework import serializers
from .models import CustomUser, Farm, FarmConditions, Condition_Rule, Condition_Type


class FarmSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    user_id = serializers.CharField()
    product_id = serializers.CharField(max_length=255)
    conditions = serializers.JSONField()

    def validate(self, attrs):
        user = CustomUser.objects.filter(id=attrs['user_id'])
        if not user:
            raise serializers.ValidationError("User Not Found, Please Login")
        attrs['user_id'] = user[0]
        return attrs

    def create(self, validated_data):
        print("CREATE")
        print(validated_data)
        validated_data.pop('conditions')
        farm = Farm.objects.create(**validated_data)
        return farm.id

        # return True

    def update(self, instance, validated_data):
        farm = Farm.objects.get(id=instance)
        for type in validated_data['conditions']:
            if type in Condition_Type:
                if validated_data['conditions'][type]['rule']  in Condition_Rule:
                    FarmConditions.objects.create(
                        farm_id=farm, notify_at=validated_data['conditions'][type]['value'], 
                        condition_type=type, condition_rule=validated_data['conditions'][type]['rule'],)
                else:
                    farm.delete()
                    raise serializers.ValidationError("Wrong Rule Type")
            else:
                farm.delete()
                raise serializers.ValidationError("Wrong Condition Type")
        return True
    
    

    
