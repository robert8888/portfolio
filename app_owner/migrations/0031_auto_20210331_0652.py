# Generated by Django 3.1.5 on 2021-03-31 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0030_auto_20210331_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='cvdocumentpersonal',
            name='age',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Age'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cvdocumentsummarytranslation',
            name='position_title',
            field=models.CharField(default=' ', max_length=255, verbose_name='Position title'),
            preserve_default=False,
        ),
    ]
