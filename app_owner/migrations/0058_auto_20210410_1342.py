# Generated by Django 3.1.5 on 2021-04-10 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0057_cvdocumentpersonaltranslation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cvdocumentpersonal',
            name='age',
        ),
        migrations.RemoveField(
            model_name='cvdocumentpersonal',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cvdocumentpersonal',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='cvdocumentpersonal',
            name='surname',
        ),
    ]
