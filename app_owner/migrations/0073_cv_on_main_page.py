# Generated by Django 3.1.5 on 2021-04-11 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0072_auto_20210411_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='on_main_page',
            field=models.BooleanField(default=False),
        ),
    ]
