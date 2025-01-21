# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2021-01-08 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0009_auto_20201222_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allow_fundraisers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='banner_title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name=b'Add a Banner header'),
        ),
        migrations.AddField(
            model_name='eventauditlogentry',
            name='allow_fundraisers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventauditlogentry',
            name='banner_title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name=b'Add a Banner header'),
        ),
    ]
