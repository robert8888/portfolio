# Generated by Django 3.1.5 on 2021-05-06 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0040_auto_20210502_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttranslation',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Project page meta description'),
        ),
        migrations.AddField(
            model_name='projecttranslation',
            name='meta_title',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Project page meta title'),
        ),
    ]