# Generated by Django 3.2.8 on 2022-08-24 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0030_alter_roombooking_guest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.roomtype'),
        ),
    ]