# Generated by Django 4.2.5 on 2024-03-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_evaluator',
            field=models.BooleanField(default=False),
        ),
    ]