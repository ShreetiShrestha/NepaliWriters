# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 17:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20171031_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 31, 23, 5, 19, 93092)),
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
