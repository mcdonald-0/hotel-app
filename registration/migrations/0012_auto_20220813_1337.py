# Generated by Django 3.2.8 on 2022-08-13 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0021_auto_20220813_1337'),
        ('registration', '0011_auto_20220813_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='room_variety',
        ),
        migrations.DeleteModel(
            name='RoomType',
        ),
    ]
