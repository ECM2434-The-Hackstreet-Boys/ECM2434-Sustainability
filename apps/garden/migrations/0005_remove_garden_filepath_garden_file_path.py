# Generated by Django 5.1.5 on 2025-02-19 17:56

import apps.garden.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0004_garden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garden',
            name='filePath',
        ),
        migrations.AddField(
            model_name='garden',
            name='file_path',
            field=models.FileField(blank=True, null=True, upload_to=apps.garden.models.garden_file_path),
        ),
    ]
