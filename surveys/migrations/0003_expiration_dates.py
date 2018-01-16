# Generated by Django 2.0.1 on 2018-01-16 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_field_lengths_type_and_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ends At'),
        ),
        migrations.AddField(
            model_name='survey',
            name='expired_message',
            field=models.TextField(blank=True, help_text='\n    Message to display to users after this survey has expired.\n    ', verbose_name='Expiration Message'),
        ),
    ]
