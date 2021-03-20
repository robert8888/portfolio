# Generated by Django 3.1.5 on 2021-03-19 13:26

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0011_auto_20210319_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Project name')),
                ('slug', models.SlugField(max_length=255)),
                ('title', models.CharField(max_length=255, verbose_name='Project title')),
                ('subtitle', models.CharField(max_length=255, verbose_name='Project subtitle')),
                ('description_short', models.TextField(verbose_name='Description short')),
                ('description_full', models.TextField(verbose_name='Description long')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='app_projects.project')),
            ],
            options={
                'verbose_name': 'Project Translation',
                'db_table': 'app_projects_project_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]