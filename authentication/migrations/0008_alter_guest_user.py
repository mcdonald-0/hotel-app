# Generated by Django 3.2.8 on 2022-08-21 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_guest_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guest', to=settings.AUTH_USER_MODEL),
        ),
    ]
