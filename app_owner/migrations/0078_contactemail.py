# Generated by Django 3.1.5 on 2021-05-16 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0077_remove_cv_on_main_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('contact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app_owner.contact')),
                ('email', models.CharField(max_length=100, verbose_name='Email address')),
            ],
            options={
                'verbose_name': 'Contact email',
            },
            bases=('app_owner.contact',),
        ),
    ]