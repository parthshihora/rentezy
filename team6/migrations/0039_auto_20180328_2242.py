# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-28 22:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team6', '0038_auto_20180323_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='drop_date',
            field=models.DateField(default=datetime.datetime(2018, 3, 28, 22, 42, 6, 713805)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='drop_time',
            field=models.TimeField(default=datetime.datetime(2018, 3, 28, 22, 42, 6, 713827)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_date',
            field=models.DateField(default=datetime.datetime(2018, 3, 28, 22, 42, 6, 713750)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_time',
            field=models.TimeField(default=datetime.datetime(2018, 3, 28, 22, 42, 6, 713781)),
        ),
    ]
