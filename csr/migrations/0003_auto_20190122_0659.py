# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-01-22 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csr', '0002_auto_20190122_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csrcommunication',
            name='csr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='csr.CSR'),
        ),
    ]
