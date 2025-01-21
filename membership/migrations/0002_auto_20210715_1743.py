# Generated by Django 3.2 on 2021-07-15 17:43

from django.db import migrations, models
import mcms.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='members',
            name='documnt',
            field=models.FileField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='members',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='members',
            name='image',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='members',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile'),
        ),
        migrations.AlterField(
            model_name='members',
            name='pincode',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Pincode'),
        ),
    ]
