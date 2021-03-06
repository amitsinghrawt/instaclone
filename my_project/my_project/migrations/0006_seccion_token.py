# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 23:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_project', '0005_auto_20170804_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seccion_token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=255)),
                ('last_request_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_project.UserModel')),
            ],
        ),
    ]
