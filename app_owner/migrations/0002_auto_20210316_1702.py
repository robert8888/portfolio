# Generated by Django 3.1.5 on 2021-03-16 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='image',
        ),
        migrations.RemoveField(
            model_name='contactimage',
            name='is_sprite',
        ),
        migrations.AddField(
            model_name='contact',
            name='id',
            field=models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactimage',
            name='contact',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app_owner.contact'),
            preserve_default=False,
        ),
    ]
