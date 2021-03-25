# Generated by Django 3.1.5 on 2021-03-23 12:09

import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0024_projecttranslation_search_vector'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSearchAutocomplete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=16)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
            options={
                'db_table': 'app_projects_project_search_auto',
            },
        ),
    ]
