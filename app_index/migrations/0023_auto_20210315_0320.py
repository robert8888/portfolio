# Generated by Django 3.1.5 on 2021-03-15 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_index', '0022_auto_20210315_0320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitemtranslation',
            old_name='value',
            new_name='text',
        ),
    ]