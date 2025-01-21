# Generated by Django 3.2 on 2021-07-15 17:43

import ckeditor.fields
from django.db import migrations, models
import mcms.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='how_project_will_solve_problem',
            field=ckeditor.fields.RichTextField(blank=True, help_text='maximum 200 characters', null=True, verbose_name='How will this project solve the problem?:'),
        ),
        migrations.AlterField(
            model_name='project',
            name='icon',
            field=mcms.thumbs.ImageWithThumbsField(blank=True, null=True, upload_to='static/v2/images/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='project',
            name='long_term_impact',
            field=ckeditor.fields.RichTextField(blank=True, help_text='maximum 200 characters', null=True, verbose_name='What is the long term impact of this project?:'),
        ),
        migrations.AlterField(
            model_name='project',
            name='problem',
            field=ckeditor.fields.RichTextField(blank=True, help_text='maximum 200 characters', null=True, verbose_name='The problem:'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Started'), (2, 'In Progress'), (3, 'Completed')], verbose_name='Project Status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='target_amount',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Goal'),
        ),
        migrations.AlterField(
            model_name='project',
            name='upload_pdf',
            field=models.FileField(blank=True, null=True, upload_to='static/v2/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='projectcause',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
