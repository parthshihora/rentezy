# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-27 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team6', '0030_auto_20180227_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_pic',
            field=models.FileField(upload_to=b''),
        ),
    ]