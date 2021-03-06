# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-13 20:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team6', '0048_merge_20180329_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='cartype',
            field=models.CharField(default=b'compact', max_length=25),
        ),
        migrations.AddField(
            model_name='car',
            name='passengerCapacity',
            field=models.IntegerField(default=b'10'),
        ),
        migrations.AlterField(
            model_name='car',
            name='pickuplocation',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='car',
            name='priceperhour',
            field=models.IntegerField(default=b''),
        ),
        migrations.AlterField(
            model_name='car',
            name='user',
            field=models.ForeignKey(default=b'', on_delete=django.db.models.deletion.CASCADE, to='team6.Reg'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='carid',
            field=models.ForeignKey(default=b'', on_delete=django.db.models.deletion.CASCADE, to='team6.Car'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='drop_date',
            field=models.DateField(default=datetime.datetime(2018, 4, 13, 20, 15, 12, 553000)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='drop_time',
            field=models.TimeField(default=datetime.datetime(2018, 4, 13, 20, 15, 12, 553000)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_date',
            field=models.DateField(default=datetime.datetime(2018, 4, 13, 20, 15, 12, 553000)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_time',
            field=models.TimeField(default=datetime.datetime(2018, 4, 13, 20, 15, 12, 553000)),
        ),
    ]
