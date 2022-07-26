# Generated by Django 3.2.8 on 2022-08-11 19:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20220811_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='next_of_kin_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(regex='(^[0]\\d{10}$)|(^[\\+]?[234]\\d{12}$)')]),
        ),
        migrations.AlterField(
            model_name='guest',
            name='phone_number',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(regex='(^[0]\\d{10}$)|(^[\\+]?[234]\\d{12}$)')]),
        ),
    ]
