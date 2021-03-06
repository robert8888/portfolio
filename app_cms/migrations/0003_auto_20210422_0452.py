# Generated by Django 3.1.5 on 2021-04-22 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cms', '0002_auto_20210418_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view',
            name='module_name',
            field=models.CharField(choices=[('app_projects.views.section_project.py', 'Section project'), ('app_projects.views.section_projects.py', 'Section projects'), ('app_projects.views.section_projects_filters.py', 'Section projects filters'), ('app_projects.views.section_projects_slider.py', 'Section projects slider'), ('app_projects.views.section_technologies.py', 'Section technologies'), ('app_owner.views.section_contact_contacts.py', 'Section contact contacts'), ('app_owner.views.section_contact_cv_configurator.py', 'Section contact cv configurator'), ('app_owner.views.section_contact_cv_download.py', 'Section contact cv download')], default='', max_length=255, null=True),
        ),
    ]
