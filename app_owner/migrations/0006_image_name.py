# Generated by Django 3.1.5 on 2021-03-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0005_auto_20210316_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(default=1, max_length=255, verbose_name='Image identification name'),
            preserve_default=False,
        ),
    ]