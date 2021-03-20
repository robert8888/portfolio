# Generated by Django 3.1.5 on 2021-03-19 11:59

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import parler

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('app_projects', '0006_auto_20210319_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Image identification name')),
                ('source', models.ImageField(height_field='height', upload_to='portals', width_field='width')),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Image',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Project name')),
                ('slug', models.SlugField(max_length=255)),
                ('title', models.CharField(max_length=255, verbose_name='Project title')),
                ('subtitle', models.CharField(max_length=255, verbose_name='Project subtitle')),
                ('description_short', models.TextField(verbose_name='Description short')),
                ('description_full', models.TextField(verbose_name='Description long')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Technology name')),
                ('link', models.CharField(max_length=255, verbose_name='Technology link')),
                ('show_on_index', models.BooleanField(default=False, verbose_name='Show on main page')),
            ],
            options={
                'verbose_name': 'Technology',
                'verbose_name_plural': 'Technologies',
            },
        ),
        migrations.CreateModel(
            name='TechnologyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_projects.technology')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_projects.image')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_app_projects.technologyimage_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='TechnologyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Technology type',
                'verbose_name_plural': 'Technology types',
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='TechnologyImageSprite',
            fields=[
                ('technologyimage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_projects.technologyimage')),
                ('top', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Top')),
                ('left', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Left')),
                ('width', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Width')),
                ('height', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Height')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('app_projects.technologyimage',),
        ),
        migrations.CreateModel(
            name='TechnologyImageStd',
            fields=[
                ('technologyimage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_projects.technologyimage')),
            ],
            options={
                'verbose_name': 'Technology image',
            },
            bases=('app_projects.technologyimage',),
        ),
        migrations.AddField(
            model_name='technology',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_projects.technologytype'),
        ),
        migrations.CreateModel(
            name='ProjectLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('host', 'Host'), ('repo', 'Repository'), ('demo', 'Demo'), ('docs', 'Documentation')], max_length=255)),
                ('links', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Link'), size=None)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_projects.project')),
            ],
            options={
                'verbose_name': 'Project link',
                'verbose_name_plural': 'Project links',
                'db_table': 'app_project_project_link',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='technology',
            field=models.ManyToManyField(to='app_projects.Technology', verbose_name='Technologies'),
        ),
    ]
