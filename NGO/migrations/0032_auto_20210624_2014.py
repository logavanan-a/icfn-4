# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2021-06-24 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NGO', '0031_auto_20210623_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='manualrecieptnodate',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'Mannual Recipt Creation Date'),
        ),
    ]
