# Generated by Django 3.1.5 on 2021-03-20 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0019_project_type'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='projecttype',
            table='app_projects_project_type',
        ),
    ]
