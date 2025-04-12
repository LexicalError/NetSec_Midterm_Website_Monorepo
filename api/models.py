from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)

#     def __str__(self):
#         return self.username




class Message(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile_Picture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
