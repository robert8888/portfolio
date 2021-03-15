# Generated by Django 3.1.5 on 2021-03-10 23:14

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True, verbose_name='Menu identification name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Menu description')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True, verbose_name='Page name')),
                ('address', models.CharField(default='', max_length=255, unique=True, verbose_name='Pager url address')),
                ('template', models.CharField(default='', max_length=255, verbose_name='Page template name')),
                ('menus', models.ManyToManyField(blank=True, to='app_index.Menu', verbose_name='Page menus')),
            ],
            options={
                'verbose_name': 'Page',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_app_index.property_set+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Property',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='only letters', max_length=255, unique=True, verbose_name='Section identification name')),
                ('template', models.CharField(default='', max_length=255, verbose_name='Section template name')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Position')),
                ('page', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_index.page')),
            ],
            options={
                'verbose_name': 'Section',
                'ordering': ['position', 'name'],
            },
        ),
        migrations.CreateModel(
            name='PropertyText',
            fields=[
                ('property_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_index.property')),
            ],
            options={
                'verbose_name': 'Property Text',
            },
            bases=('app_index.property', parler.models.TranslatableModelMixin, models.Model),
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='PropertyTextLong',
            fields=[
                ('property_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_index.property')),
                ('value', models.TextField(default='', verbose_name='Text value')),
            ],
            options={
                'verbose_name': 'Property Text Long',
            },
            bases=('app_index.property',),
        ),
        migrations.CreateModel(
            name='PropertyTextRich',
            fields=[
                ('property_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_index.property')),
                ('value', models.TextField(default='', verbose_name='Text value')),
            ],
            options={
                'verbose_name': 'Property Text Rich',
            },
            bases=('app_index.property',),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('projects', 'Projects'), ('stack', 'Stack'), ('contact', 'Contact')], default='', max_length=255, null=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_index.section')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_index.section'),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=255, verbose_name='Text')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_index.menu')),
            ],
            bases = (parler.models.TranslatableModelMixin, models.Model)
        ),
        migrations.CreateModel(
            name='PropertyTextTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('value', models.CharField(default='', max_length=255, verbose_name='Text value')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='app_index.propertytext')),
            ],
            options={
                'verbose_name': 'Property Text Translation',
                'db_table': 'app_index_propertytext_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
