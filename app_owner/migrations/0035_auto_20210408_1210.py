# Generated by Django 3.1.5 on 2021-04-08 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0034_auto_20210407_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cvcolorprofile',
            name='background',
        ),
        migrations.RemoveField(
            model_name='cvcolorprofile',
            name='primary',
        ),
        migrations.RemoveField(
            model_name='cvcolorprofile',
            name='secondary',
        ),
        migrations.RemoveField(
            model_name='cvcolorprofile',
            name='text_primary',
        ),
        migrations.RemoveField(
            model_name='cvcolorprofile',
            name='text_primary_focus',
        ),
        migrations.RemoveField(
            model_name='cvcolorprofile',
            name='text_secondary',
        ),
        migrations.RemoveField(
            model_name='cvcolorprofile',
            name='text_secondary_focus',
        ),
    ]
