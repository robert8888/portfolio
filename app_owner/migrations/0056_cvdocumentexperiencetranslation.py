# Generated by Django 3.1.5 on 2021-04-09 21:20

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0055_cvdocumentskillstranslation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CVDocumentExperienceTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('section_title', models.CharField(max_length=255, verbose_name='Section title')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='app_owner.cvdocumentexperience')),
            ],
            options={
                'verbose_name': 'CV document experience Translation',
                'db_table': 'app_owner_cv_doc_exp_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
