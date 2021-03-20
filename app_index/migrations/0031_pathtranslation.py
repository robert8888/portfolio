# Generated by Django 3.1.5 on 2021-03-18 19:54

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_index', '0030_auto_20210318_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Regex url pattern - groups as parameters')),
                ('pattern', models.CharField(max_length=255, verbose_name='Regex path pattern - groups as parameters')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='app_index.path')),
            ],
            options={
                'verbose_name': 'path Translation',
                'db_table': 'app_index_path_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
