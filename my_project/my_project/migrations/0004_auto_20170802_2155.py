# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 04:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_project', '0003_auto_20170802_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
