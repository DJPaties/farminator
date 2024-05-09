from rest_framework import serializers
from .models import CustomUser, Farm, FarmConditions, Condition_Rule, Condition_Type


class FarmSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    image = serializers.ImageField(max_length=1000000,
                                   allow_empty_file=False,
                                   write_only=True,
                                   use_url=False)
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
        try:
            
            farm = Farm.objects.create(title=validated_data['title'],
                                       location=validated_data['location'],
                                       image=validated_data['image'],
                                       product_id=validated_data['product_id'],
                                       user_id=validated_data['user_id'])

            if farm:
                for type in validated_data['conditions']:
                    if type in Condition_Type:
                        if validated_data['conditions'][type]['rule'] in Condition_Rule:
                            FarmConditions.objects.create(
                                farm_id=farm, notify_at=validated_data['conditions'][type]['value'],
                                condition_type=type, condition_rule=validated_data['conditions'][type]['rule'],)
                        else:
                            farm.delete()
                            raise serializers.ValidationError(
                                "Wrong Rule Type")
                    else:
                        farm.delete()
                        raise serializers.ValidationError(
                            "Wrong Condition Type")
        except:
            farm.delete()
        return farm

        # return True

    def update(self, instance, validated_data):

        farm = Farm.objects.get(id=validated_data['id'])
        farm.title = validated_data['title']
        farm.location = validated_data['location']
        farm.image = validated_data['image']
        farm.product_id = validated_data['product_id']
        farm.user_id = CustomUser.objects.get(id=validated_data['user_id'])

        if farm:
            farm.save()
            for i in validated_data['conditions']:
                try:
                    farm_condition = FarmConditions.objects.get(
                        farm_id_id=validated_data['id'], condition_type=i)
                    print(farm_condition.serialize())
                    farm_condition.farm_id_id = validated_data['id']
                    farm_condition.condition_type = i
                    farm_condition.condition_rule = validated_data['conditions'][i]['rule']
                    farm_condition.notify_at = validated_data['conditions'][i]['value']

                    farm_condition.save()
                except:
                    FarmConditions.objects.create(
                        farm_id_id=validated_data['id'], notify_at=validated_data['conditions'][i]['value'],
                        condition_type=i, condition_rule=validated_data['conditions'][i]['rule'],)

        return instance.id
