# Generated by Django 3.1.5 on 2021-03-20 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0021_technology_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projecttype',
            old_name='name',
            new_name='value',
        ),
    ]
