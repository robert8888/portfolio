# Generated by Django 3.1.5 on 2021-04-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0049_auto_20210409_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvdocumentexperiencejob',
            name='to_date',
            field=models.DateField(blank=True, null=True, verbose_name='To'),
        ),
    ]
