# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-18 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20170513_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthDate',
            field=models.DateField(auto_now_add=True),
        ),
    ]