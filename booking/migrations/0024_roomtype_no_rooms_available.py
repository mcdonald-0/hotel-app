# Generated by Django 3.2.8 on 2022-08-15 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0023_auto_20220814_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='no_rooms_available',
            field=models.BooleanField(default=False),
        ),
    ]
