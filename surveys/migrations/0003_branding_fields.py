# Generated by Django 2.0.1 on 2018-01-16 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_field_lengths_type_and_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='brand_link',
            field=models.URLField(blank=True, help_text='\n        The logo and text will link out to this url,\n        e.g. https://www.wnycstudios.org/shows/deathsexmoney.\n    ', verbose_name='Brand Link'),
        ),
        migrations.AddField(
            model_name='survey',
            name='brand_link_label',
            field=models.CharField(blank=True, max_length=200, verbose_name='Link Text'),
        ),
        migrations.AddField(
            model_name='survey',
            name='brand_logo',
            field=models.ImageField(blank=True, help_text='This image should be a square.', upload_to='media/surveys/logos', verbose_name='Brand Logo'),
        ),
    ]
