# Generated by Django 5.1.6 on 2025-03-10 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0011_remove_property_photo_property_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='image',
            field=models.ImageField(default='property_photos/default_image.jpg', upload_to='media/'),
        ),
    ]
