# Generated by Django 3.1.5 on 2021-03-20 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_index', '0033_auto_20210320_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view',
            name='module_name',
            field=models.CharField(choices=[('app_projects.views.section_projects.py', 'Section projects'), ('app_projects.views.section_projects_filters.py', 'Section projects filters'), ('app_owner.views.section_contact.py', 'Section contact')], default='', max_length=255, null=True),
        ),
    ]