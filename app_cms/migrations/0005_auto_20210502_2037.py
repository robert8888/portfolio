# Generated by Django 3.1.5 on 2021-05-02 18:37

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cms', '0004_auto_20210501_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Page meta',
                'verbose_name_plural': 'Page metas',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='page',
            name='meta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_cms.pagemeta', unique=True),
        ),
        migrations.CreateModel(
            name='PageMetaTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.CharField(default=',', max_length=255)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='app_cms.pagemeta')),
            ],
            options={
                'verbose_name': 'Page meta Translation',
                'db_table': 'app_cms_pagemeta_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
