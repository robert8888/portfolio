# Generated by Django 3.1.5 on 2021-04-08 11:51

from django.db import migrations, models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0035_project_show_on_index'),
        ('app_owner', '0038_cv_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvdocument',
            name='additional',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='app_owner.CVDocumentAdditional', verbose_name='Additional'),
        ),
        migrations.AlterField(
            model_name='cvdocumentskills',
            name='technologies',
            field=models.ManyToManyField(to='app_projects.Technology', verbose_name='Technologies'),
        ),
    ]
