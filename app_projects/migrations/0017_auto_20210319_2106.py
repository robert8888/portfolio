# Generated by Django 3.1.5 on 2021-03-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0016_technology_show_on_index_all'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='related',
            field=models.ManyToManyField(blank=True, to='app_projects.Project', verbose_name='Related'),
        ),
        migrations.AlterField(
            model_name='projecttranslation',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Project name'),
        ),
        migrations.AlterField(
            model_name='projecttranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Project title'),
        ),
    ]
