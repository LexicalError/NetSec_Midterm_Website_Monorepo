# Generated by Django 5.2 on 2025-04-14 15:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customuser_id_alter_message_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.CharField(max_length=255, validators=[django.core.validators.ProhibitNullCharactersValidator, django.core.validators.MaxLengthValidator(255), django.core.validators.MinLengthValidator(1), django.core.validators.RegexValidator(message='Content can only contain letters, numbers, and spaces.', regex='^[\\w\\s]+$')]),
        ),
    ]
