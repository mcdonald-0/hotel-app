# Generated by Django 3.2.8 on 2022-07-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_roombooking_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='roombooking',
            name='date_booked',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='roombooking',
            name='date_checked_out',
            field=models.DateField(null=True),
        ),
    ]
