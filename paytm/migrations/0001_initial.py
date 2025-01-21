# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-01-21 14:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaytmHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ORDERID', models.CharField(max_length=300, verbose_name=b'ORDER ID')),
                ('TXNDATE', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'TXN DATE')),
                ('TXNID', models.CharField(max_length=100, verbose_name=b'TXN ID')),
                ('BANKTXNID', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'BANK TXN ID')),
                ('BANKNAME', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'BANK NAME')),
                ('RESPCODE', models.IntegerField(verbose_name=b'RESP CODE')),
                ('PAYMENTMODE', models.CharField(blank=True, max_length=10, null=True, verbose_name=b'PAYMENT MODE')),
                ('CURRENCY', models.CharField(blank=True, max_length=4, null=True, verbose_name=b'CURRENCY')),
                ('GATEWAYNAME', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'GATEWAY NAME')),
                ('MID', models.CharField(max_length=40)),
                ('RESPMSG', models.TextField(max_length=250, verbose_name=b'RESP MSG')),
                ('TXNAMOUNT', models.FloatField(verbose_name=b'TXN AMOUNT')),
                ('STATUS', models.CharField(max_length=12, verbose_name=b'STATUS')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_payment_paytm', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
