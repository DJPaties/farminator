from django.db import models
from users.models import CustomUser
from farm.models import Farm


class Reminder(models.Model):
    description = models.CharField(max_length=10000)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    date_time = models.DateTimeField()

    class Meta:
        db_table = 'reminder'

    def __str__(self) -> str:
        return self.farm_id

    def serialize(self):
        return {
            'description': self.description,
            'user_id': self.user_id,
            'farm': self.farm.title,
            'date_time': self.date_time,
        }
