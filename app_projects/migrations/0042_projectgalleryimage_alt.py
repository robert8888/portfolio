# Generated by Django 3.1.5 on 2021-05-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0041_auto_20210506_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectgalleryimage',
            name='alt',
            field=models.CharField(default='image', max_length=255),
        ),
    ]
