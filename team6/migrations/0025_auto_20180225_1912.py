# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-25 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team6', '0024_auto_20180225_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_pic',
            field=models.ImageField(default=b'team6/static/pic_folder/no.jpeg', upload_to=b'team6/static/pic_folder/'),
        ),
    ]
