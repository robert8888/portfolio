# Generated by Django 3.1.5 on 2021-04-22 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0076_auto_20210422_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cv',
            name='on_main_page',
        ),
    ]
