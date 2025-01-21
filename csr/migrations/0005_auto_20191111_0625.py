# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-11-11 06:25
from __future__ import unicode_literals

import csr.views
from django.db import migrations
import mcms.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('csr', '0004_auto_20190122_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csr',
            name='icon',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, help_text=b'Upload Logo of size 90x120.', null=True, upload_to=b'static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
    ]
