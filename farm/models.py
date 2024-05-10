from django.db import models
from users.models import CustomUser
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os 
import uuid
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

def get_image_upload_path(instance, filename):
    unique_filename = str(uuid.uuid4())[:8]
    ext = os.path.splitext(filename)[1]
    return os.path.join('farm/static/', f'{instance.title}_{unique_filename}{ext}')

class Farm(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(max_length=1000000, upload_to=get_image_upload_path,
                              storage=FileSystemStorage(location=settings.STATIC_ROOT))
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
            "image": "/".join(self.image.url.split("/")[-2:]),
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
