# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quake', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quakedbs',
            name='date',
            field=models.DateTimeField(blank=True, help_text='Date Published'),
        ),
    ]
