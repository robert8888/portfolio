# Generated by Django 3.1.5 on 2021-05-14 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cms', '0010_auto_20210502_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagemetatranslation',
            name='json_ld',
            field=models.JSONField(blank=True, null=True, verbose_name='Json ld'),
        ),
    ]
