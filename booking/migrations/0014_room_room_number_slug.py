# Generated by Django 3.2.8 on 2022-08-06 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_alter_room_room_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_number_slug',
            field=models.SlugField(null=True),
        ),
    ]
