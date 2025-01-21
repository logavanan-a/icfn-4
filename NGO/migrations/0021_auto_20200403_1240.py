# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-04-03 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NGO', '0020_auto_20191111_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duplicatecorporates',
            name='team',
            field=models.CharField(blank=True, choices=[(b'Team-10', b'Team-10'), (b'Team-12', b'Team-12'), (b'Team-15', b'Team-15'), (b'Team-25', b'Team-25'), (b'Team-30', b'Team-30'), (b'Team-40', b'Team-40'), (b'Team-45', b'Team-45'), (b'Team-60', b'Team-60'), (b'Team-100', b'Team-100')], max_length=200, null=True, verbose_name=b'Select Team'),
        ),
    ]
