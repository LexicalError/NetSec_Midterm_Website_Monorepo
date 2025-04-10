from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.username
    
class Message(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title