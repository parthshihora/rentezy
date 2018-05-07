# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-25 00:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team6', '0010_auto_20180225_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='user1',
        ),
        migrations.AddField(
            model_name='car',
            name='user',
            field=models.ForeignKey(default=b'0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]