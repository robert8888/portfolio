# Generated by Django 3.1.5 on 2021-05-01 15:19

from django.db import migrations
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField 

class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0037_auto_20210409_2320'),
    ]

    operations = [
        AlterSortedManyToManyField (
            model_name='project',
            name='technology',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='app_projects.Technology', verbose_name='Technologies'),
        ),
    ]