# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 03:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20171129_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizsession',
            name='session_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 29, 3, 50, 9, 93384, tzinfo=utc)),
        ),
    ]
