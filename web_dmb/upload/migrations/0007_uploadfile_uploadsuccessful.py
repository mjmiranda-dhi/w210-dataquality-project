# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_auto_20170418_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='uploadSuccessful',
            field=models.BooleanField(default=False),
        ),
    ]
