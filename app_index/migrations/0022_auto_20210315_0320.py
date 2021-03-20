# Generated by Django 3.1.5 on 2021-03-15 02:20

from django.db import migrations
import django.db.models.deletion
import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_index', '0021_auto_20210315_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitemtranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='app_index.menuitem'),
        ),
    ]