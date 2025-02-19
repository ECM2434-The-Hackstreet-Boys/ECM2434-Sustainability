# Generated by Django 5.1.5 on 2025-02-19 16:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0003_delete_garden'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('gardenID', models.AutoField(primary_key=True, serialize=False)),
                ('filePath', models.FilePathField()),
                ('rating', models.FloatField(default=0)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
