# Generated by Django 3.2.8 on 2022-08-16 12:51

import booking.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0024_roomtype_no_rooms_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_images',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=booking.models.image_filepath),
        ),
    ]
