# Generated by Django 4.2.5 on 2024-05-06 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('item_management', '0022_payment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evaluation', '0005_evaluatorprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('state', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item_management.item')),
            ],
        ),
    ]
