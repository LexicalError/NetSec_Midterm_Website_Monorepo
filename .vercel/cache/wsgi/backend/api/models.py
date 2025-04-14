import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4, 
        editable=False,
        validators=[
            validators.ProhibitNullCharactersValidator,
            validators.validate_slug,
        ]
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Message(models.Model):
    id = models.AutoField(primary_key=True, validators = [
        validators.MinValueValidator(1),
        validators.MaxValueValidator(9999999999),
        validators.ProhibitNullCharactersValidator,
    ])
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, validators = [
        validators.ProhibitNullCharactersValidator,
        validators.validate_slug,
    ])
    content = models.CharField(max_length=255, validators = [
        validators.ProhibitNullCharactersValidator,
        validators.MaxLengthValidator(255),
        validators.MinLengthValidator(1),
        validators.RegexValidator(
            regex=r'^[\w\s]+$',
            message='Content can only contain letters, numbers, and spaces.'
        ),
    ])
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Profile_Picture(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=500, blank=True, null=True, validators = [
        validators.URLValidator(schemes=['https']),
        validators.ProhibitNullCharactersValidator,
        validators.MaxLengthValidator(500),
        validators.MinLengthValidator(1),
    ])
    
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
