# Generated by Django 4.2.5 on 2024-04-27 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_management', '0017_rename_is_visible_item_visible_to_customers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='visible_to_customers',
            field=models.BooleanField(blank=True),
        ),
    ]