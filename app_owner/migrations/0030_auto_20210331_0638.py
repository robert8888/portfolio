# Generated by Django 3.1.5 on 2021-03-31 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0029_auto_20210331_0637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cvdocumentpersonal',
            old_name='id_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='cvdocument',
            name='personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app_owner.cvdocumentpersonal', verbose_name='Personal data'),
        ),
    ]
