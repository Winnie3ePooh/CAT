# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-14 16:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0011_auto_20170513_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='name',
        ),
    ]
