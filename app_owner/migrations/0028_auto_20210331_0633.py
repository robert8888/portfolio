# Generated by Django 3.1.5 on 2021-03-31 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0027_auto_20210331_0632'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cvdocumentpersonal',
            table='app_owner_cv_doc_personal',
        ),
        migrations.AlterModelTable(
            name='cvdocumentpersonalcontacts',
            table='app_owner_cv_doc_personal_contacts_rel',
        ),
    ]
