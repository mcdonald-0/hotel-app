# Generated by Django 3.2.8 on 2022-08-02 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_alter_room_room_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roombooking',
            name='room_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.room'),
        ),
    ]