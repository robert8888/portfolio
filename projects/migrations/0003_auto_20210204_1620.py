# Generated by Django 3.1.5 on 2021-02-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20210127_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='photo_height',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='owner',
            name='photo_width',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='technology',
            name='logo_height',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='technology',
            name='logo_width',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='owner',
            name='photo',
            field=models.ImageField(height_field='photo_height', help_text='Select author photo', max_length=255, upload_to='author', verbose_name='Photo', width_field='photo_width'),
        ),
        migrations.AlterField(
            model_name='technology',
            name='logo',
            field=models.ImageField(height_field='logo_width', max_length=255, upload_to='technology', width_field='logo_height'),
        ),
    ]