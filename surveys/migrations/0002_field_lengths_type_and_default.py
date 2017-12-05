# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='question',
            name='short_name',
            field=models.SlugField(max_length=100),
        ),
        migrations.AlterField(
            model_name='survey',
            name='starts_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Starts At'),
        ),
    ]