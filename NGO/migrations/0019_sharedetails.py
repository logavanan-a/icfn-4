# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-08-16 08:58
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NGO', '0018_foreignerdonationdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('key', models.CharField(blank=True, max_length=2000, null=True)),
                ('title', models.CharField(max_length=150, verbose_name=b'Name of the CSO')),
                ('description', ckeditor.fields.RichTextField(help_text=b'Should not exceed 210 characters', verbose_name=b'Mission Statement*')),
                ('image', models.CharField(blank=True, max_length=3000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
