# Generated by Django 5.1.5 on 2025-03-22 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play_screen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizlocation',
            name='quizID',
            field=models.IntegerField(default=0),
        ),
    ]
