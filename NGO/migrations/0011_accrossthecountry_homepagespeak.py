# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-27 08:51
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import mcms.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('NGO', '0010_donationreceipts_topeventawards'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccrossTheCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(blank=True, max_length=350, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name=b'description')),
                ('banner', mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to=b'static/v2/%Y/%m/%d')),
                ('video', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePageSpeak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('headline', models.CharField(blank=True, max_length=350, null=True, verbose_name=b'Headline')),
                ('title', models.CharField(blank=True, max_length=350, null=True)),
                ('video', models.URLField()),
                ('speach', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name=b'speach')),
                ('byline', models.CharField(blank=True, max_length=350, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
