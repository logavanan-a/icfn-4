# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-11-11 06:25
from __future__ import unicode_literals

import csr.views
from django.db import migrations
import mcms.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('mcms', '0004_annualreport_filetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annualreport',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='front_image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='homebanner',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/images/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='iccontentdetails',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, help_text='Image size should be 930x300 pixels', null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='ourinitiatives',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
        migrations.AlterField(
            model_name='section',
            name='icon',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d', validators=[csr.views.validate_image]),
        ),
    ]
