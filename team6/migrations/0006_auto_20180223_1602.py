# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-23 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team6', '0005_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='car',
            name='car_pic',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'pic_folder/'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
