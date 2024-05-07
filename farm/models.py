from django.db import models
from customUsers.models import CustomUser
# Create your models here.


water = 'WATER'
soil = 'SOIL'
temp = 'TEMP'
light = 'LIGHT'
Condition_Type = [
    'water_level',
    'soil_moisture',
    'temperature',
    'light_intensity',
]

EQ = 'EQUAL'
GT = 'GREATER'
LT = 'LESS'
Condition_Rule = [
    'equal',
    'greater_than',
    'less_than',
]


class Farm(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=255)

    class Meta:
        db_table = "farms"

    def __str__(self) -> str:
        return self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "image": self.image,
            "product_id": self.product_id
        }


class FarmConditions(models.Model):
    farm_id = models.ForeignKey(Farm, on_delete=models.CASCADE)
    condition_type = models.CharField(
        max_length=15, null=False)
    condition_rule = models.CharField(
        max_length=12,  null=False)
    notify_at = models.FloatField(max_length=255, null=False)

    class Meta:
        db_table = 'conditions'

    def __str__(self) -> str:
        return Farm.objects.get(id=self.farm_id)
    
    def serialize(self):
        return {
            "id": self.id,
            "farm_id_id": self.farm_id_id,
            "condition_type": self.condition_type,
            "condition_rule": self.condition_rule,
            "notify_at": self.notify_at
        }
