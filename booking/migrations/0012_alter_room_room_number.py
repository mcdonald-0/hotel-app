# Generated by Django 3.2.8 on 2022-08-02 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_rename_room_number_roombooking_room_booked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_number',
            field=models.IntegerField(null=True),
        ),
    ]
