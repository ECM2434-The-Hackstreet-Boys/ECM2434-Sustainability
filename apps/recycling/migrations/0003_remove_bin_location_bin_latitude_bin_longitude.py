# Generated by Django 5.1.6 on 2025-03-19 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycling', '0002_delete_items_alter_bin_qrcode_delete_qrcodes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bin',
            name='location',
        ),
        migrations.AddField(
            model_name='bin',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='bin',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
