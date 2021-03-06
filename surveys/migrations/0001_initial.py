# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-06 16:39
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_type', models.CharField(choices=[('t', 'Simple Text'), ('x', 'Longer Text'), ('e', 'Email'), ('a', 'Audio')], default='t', max_length=1, verbose_name='Question Type')),
                ('label', models.CharField(max_length=100, verbose_name='User-friendly Label')),
                ('short_name', models.CharField(max_length=100)),
                ('question_text', models.TextField(blank=True, max_length=100)),
                ('required', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('answers', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(blank=True)),
                ('thank_you', models.TextField(blank=True, verbose_name='Thank You Message')),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='surveys.Survey'),
        ),
    ]
