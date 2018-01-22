# Generated by Django 2.0.1 on 2018-01-16 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_expiration_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='expired_message',
            field=models.TextField(blank=True, help_text='\n    Message to display to users after this survey has expired.\n    ', verbose_name='Expiration Message'),
        ),
    ]
