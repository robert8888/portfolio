from django.db import models
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    author = models.ForeignKey(
            'Owner', 
            on_delete = models.CASCADE
        )
    
    name = models.CharField(
            max_length = 100, 
            help_text = "Enter project name", 
            verbose_name = "Project name"
        )

    class ProjectType(models.TextChoices):
        LIBRARY = 'LIB', _('Library')
        API = 'API', _('Api')
        WEBPAGE = 'WEB', _('Webpage')

    type = models.CharField(
            max_length=3,
            choices=ProjectType.choices,
            default=ProjectType.WEBPAGE,
        )

    on_page = models.BooleanField(
             verbose_name = "Is on displayed on main page ?",
             default = False,
         )

    short_description = models.TextField(
            help_text = "Enter short project description", 
            verbose_name = "Short project description"
        )

    full_description = models.TextField(
            help_text = "Enter full project description", 
            verbose_name = "Full project descritpion"
        )

    repository = models.CharField(
            max_length = 500,
            help_text = "Enter url of project repository",
            verbose_name = "Repository"
        )

    demo = models.CharField(
            max_length = 500,
            help_text = "Enter url of demo page"
        )

    technologies = models.ManyToManyField(
            'Technology', 
            help_text="Select technology for this project",
            blank=True
        )

    related = models.ManyToManyField(
            'self',
            help_text = "Select related projects",
            blank = True,
        )
    
    def main_technologies(self):
        return ', '.join(technology.name for technology in self.technologies.all()[:5])
    
    main_technologies.short_description = 'Technologies'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
