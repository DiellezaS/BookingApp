# Generated by Django 5.1.6 on 2025-02-19 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('property_type', models.CharField(choices=[('apartamente', 'Apartamente'), ('villa', 'Villa'), ('suita', 'Suita')], max_length=20)),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=12)),
                ('location', models.CharField(max_length=255)),
                ('square_meters', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('max_guests', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('listed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
