from django.db import models
from customUsers.models import CustomUser

class RemoteSystemRegister(models.Model):
    class Meta:
        db_table = "remote_systems"
        
    custom_token = models.CharField(max_length=255)
    user_id_connected = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True
    )