# Generated by Django 3.1.5 on 2021-04-09 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0051_remove_cvdocument_additional'),
    ]

    operations = [
        migrations.AddField(
            model_name='cvdocument',
            name='additional',
            field=models.ManyToManyField(blank=True, to='app_owner.CVDocumentAdditional', verbose_name='Additional'),
        ),
    ]
