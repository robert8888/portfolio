# Generated by Django 3.1.5 on 2021-04-09 21:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_projects', '0035_project_show_on_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='skill_level',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Skill level'),
        ),
    ]