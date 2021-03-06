# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 23:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team6', '0036_auto_20180323_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='carid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='drop_date',
            field=models.DateField(default=datetime.datetime(2018, 3, 23, 23, 46, 10, 604000)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='drop_time',
            field=models.TimeField(default=datetime.datetime(2018, 3, 23, 23, 46, 10, 604000)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_date',
            field=models.DateField(default=datetime.datetime(2018, 3, 23, 23, 46, 10, 604000)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_time',
            field=models.TimeField(default=datetime.datetime(2018, 3, 23, 23, 46, 10, 604000)),
        ),
    ]
