# Generated by Django 5.1.6 on 2025-02-27 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_property_listed_by_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('reserved', 'Reserved'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('pending', 'Pending')], default='reserved', max_length=50),
        ),
    ]
