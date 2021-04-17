# Generated by Django 3.1.5 on 2021-04-17 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_index', '0037_auto_20210328_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='template',
            field=models.CharField(choices=[('menus/menu-main.html', 'Main'), ('menus/menu-aside.html', 'Aside'), ('menus/menu-additional.html', 'Addtional'), ('menus/menu-main.html', 'Main'), ('menus/menu-aside.html', 'Aside'), ('menus/menu-additional.html', 'Addtional')], default='', max_length=255, verbose_name='Menu template'),
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.CharField(choices=[('page_index.html', 'Index'), ('page_index.html', 'Index'), ('page_projects.html', 'Projects'), ('page_project.html', 'Project')], default='', max_length=255, verbose_name='Page template name'),
        ),
        migrations.AlterField(
            model_name='section',
            name='template',
            field=models.CharField(choices=[('sections/section-footer.html', 'Section Footer'), ('sections/section-header.html', 'Section Header'), ('sections/section-welcome.html', 'Section Welcome'), ('sections/section-stack.html', 'Section Stack'), ('sections/section-projects.html', 'Section Project Slider'), ('sections/section-about.html', 'Section About'), ('sections/section-contact.html', 'Section Contact'), ('sections/section-footer.html', 'Section Footer'), ('sections/section-header.html', 'Section Header'), ('sections/section-welcome.html', 'Section Welcome'), ('sections/section-stack.html', 'Section Stack'), ('sections/section-projects.html', 'Section Project Slider'), ('sections/section-about.html', 'Section About'), ('sections/section-contact.html', 'Section Contact'), ('sections/section_projects_filters.html', 'Section Projects Filters'), ('sections/section_projects.html', 'Section Projects'), ('sections/section_project.html', 'Section Project')], default='', max_length=255, verbose_name='Section template name'),
        ),
        migrations.AlterField(
            model_name='view',
            name='module_name',
            field=models.CharField(choices=[('app_projects.views.section_project.py', 'Section project'), ('app_projects.views.section_projects.py', 'Section projects'), ('app_projects.views.section_projects_filters.py', 'Section projects filters'), ('app_projects.views.section_projects_slider.py', 'Section projects slider'), ('app_projects.views.section_technologies.py', 'Section technologies'), ('app_owner.views.section_contact.py', 'Section contact'), ('app_owner.views.section_cv_download.py', 'Section cv download')], default='', max_length=255, null=True),
        ),
    ]
