# Generated by Django 3.1.5 on 2021-04-10 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0063_auto_20210410_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cvdocumentpersonaltranslation',
            name='age',
        ),
        migrations.AddField(
            model_name='cvdocumentpersonaltranslation',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Birthday'),
        ),
    ]
