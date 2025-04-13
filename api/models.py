import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4, 
        editable=False
    )

    def __str__(self):
        return self.username

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile_Picture(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
