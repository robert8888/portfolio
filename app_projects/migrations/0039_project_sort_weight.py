# Generated by Django 3.1.5 on 2021-05-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0038_auto_20210501_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sort_weight',
            field=models.PositiveIntegerField(default=0, verbose_name='Default sort weight'),
        ),
    ]