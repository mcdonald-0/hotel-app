# Generated by Django 3.2.8 on 2022-08-06 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0014_room_room_number_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room_number_slug',
            new_name='slug',
        ),
    ]
