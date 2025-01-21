# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-09 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NGO', '0014_classification_cso_classification_relation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsoClassificationKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cso_classification_relation',
            name='keywords',
            field=models.ManyToManyField(blank=True, null=True, to='NGO.CsoClassificationKeyword'),
        ),
    ]
