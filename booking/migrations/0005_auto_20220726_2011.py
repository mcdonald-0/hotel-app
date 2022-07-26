# Generated by Django 3.2.8 on 2022-07-26 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20220726_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roombooking',
            name='is_booked',
        ),
        migrations.AddField(
            model_name='roombooking',
            name='date_checked_in',
            field=models.DateField(null=True),
        ),
    ]
