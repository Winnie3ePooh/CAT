# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 17:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_auto_20170513_1827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='isVisible',
            new_name='isPassed',
        ),
    ]