# Generated by Django 3.1.5 on 2021-02-04 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210204_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='url',
            field=models.CharField(blank=True, default='', help_text='Technology url eg. official page', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='technology',
            name='description',
            field=models.CharField(blank=True, default='', help_text='Technology description', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='technology',
            name='name',
            field=models.CharField(default='', help_text='Technology name', max_length=255),
        ),
    ]
