from django.db import models
from users.models import CustomUser
from farm.models import Farm


class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    farm_id = models.ForeignKey(Farm, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'notification'

    def __str__(self) -> str:
        return self.title

    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id_id,
            'farm': self.farm_id.title,
            'created_at': self.created_at,
        }
