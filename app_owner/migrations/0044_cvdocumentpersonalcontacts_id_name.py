# Generated by Django 3.1.5 on 2021-04-09 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0043_cvdocument_additional'),
    ]

    operations = [
        migrations.AddField(
            model_name='cvdocumentpersonalcontacts',
            name='id_name',
            field=models.CharField(default='', max_length=255, verbose_name='Identification name'),
            preserve_default=False,
        ),
    ]
