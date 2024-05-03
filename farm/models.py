from django.db import models
from customUsers.models import CustomUser
# Create your models here.
class Farm(models.Model):
    title = models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    image =models.CharField(max_length=255)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = "farms"
    
    def __str__(self) -> str:
        return self.title
    
    
    
        