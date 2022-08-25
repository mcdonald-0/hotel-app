# Generated by Django 3.2.8 on 2022-08-16 13:29

import booking.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0025_room_room_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_images',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('room_images', models.ImageField(blank=True, max_length=255, null=True, upload_to=booking.models.get_room_type_images_filepath)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.room')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
