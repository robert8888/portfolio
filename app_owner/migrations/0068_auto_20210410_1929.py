# Generated by Django 3.1.5 on 2021-04-10 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_owner', '0067_auto_20210410_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvdocument',
            name='additional',
            field=models.ManyToManyField(through='app_owner.CVDocument_additional', to='app_owner.CVDocumentAdditional', verbose_name='Additional'),
        ),
        migrations.AlterField(
            model_name='cvdocumentadditional',
            name='type',
            field=models.CharField(choices=[('hobby', 'Hobby'), ('strength', 'Strengths'), ('achievement', 'Achievements'), ('other', 'Other')], max_length=50, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='cvdocumentadditionaltranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Section title'),
        ),
    ]
