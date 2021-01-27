from django.db import models

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

    short_description = models.TextField(
            max_length = 255, 
            help_text = "Enter short project description", 
            verbose_name = "Short project description"
        )

    full_description = models.TextField(
            max_length = 1000, 
            help_text = "Enter full project description", 
            verbose_name = "Full project descritpion"
        )
    
    technologies = models.ManyToManyField(
            'Technology', 
            help_text="Select technology for this project",
            blank=True
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
    
    def main_technologies(self):
        return ','.join(technology.name for technology in self.technologies.all()[:3])
    
    main_technologies.short_description = 'Technologies'

    def __str__(self):
        return "Project"

    class Meta:
        verbose_name = "Project"
