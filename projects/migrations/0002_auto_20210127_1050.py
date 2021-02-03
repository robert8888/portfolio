# Generated by Django 3.1.5 on 2021-01-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='technology',
            options={'verbose_name': 'Technologie'},
        ),
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(blank=True, help_text='Select technology for this project', to='projects.Technology'),
        ),
    ]