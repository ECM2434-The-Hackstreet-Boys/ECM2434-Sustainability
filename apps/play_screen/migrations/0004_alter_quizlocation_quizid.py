# Generated by Django 5.1.5 on 2025-03-22 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play_screen', '0003_alter_quizlocation_quizid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizlocation',
            name='quizID',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
