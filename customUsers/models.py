from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.


class CustomUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'custom_users'  # Optional: specify custom database table name

    def __str__(self):
        return self.username


class CustomToken(models.Model):
    token = models.CharField(max_length=255, unique=True, primary_key=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'custom_tokens'

    @classmethod
    def generate_token(cls, custom_user):
        token_key = get_random_string(length=64)  # Generate a random token key
        custom_token = cls(token=token_key, custom_user=custom_user)
        custom_token.save()
        return token_key
