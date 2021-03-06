# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 23:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quake', '0002_auto_20170625_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('emailAddress', models.EmailField(max_length=254)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='quakedbs',
            name='country',
            field=models.CharField(max_length=500, null=True, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='quakedbs',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='quakedbs',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
