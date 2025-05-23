# Generated by Django 5.2 on 2025-04-14 14:16

import django.core.validators
import re
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, validators=[django.core.validators.ProhibitNullCharactersValidator, django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^[-\\w]+\\Z'), 'Enter a valid “slug” consisting of Unicode letters, numbers, underscores, or hyphens.', 'invalid'), django.core.validators.ProhibitNullCharactersValidator, django.core.validators.MaxLengthValidator(255), django.core.validators.MinLengthValidator(1), django.core.validators.RegexValidator(message='Content can only contain letters, numbers, and spaces.', regex='^[\\w\\s]+$')]),
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999999999), django.core.validators.ProhibitNullCharactersValidator]),
        ),
        migrations.AlterField(
            model_name='message',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, validators=[django.core.validators.ProhibitNullCharactersValidator, django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='profile_picture',
            name='profile_picture',
            field=models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator(schemes=['https']), django.core.validators.ProhibitNullCharactersValidator, django.core.validators.MaxLengthValidator(500), django.core.validators.MinLengthValidator(1)]),
        ),
    ]
