# Generated by Django 3.2.8 on 2022-08-14 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20220813_1337'),
        ('booking', '0021_auto_20220813_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='roombooking',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.roomtype'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='hotel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_types', to='registration.hotel'),
        ),
    ]
