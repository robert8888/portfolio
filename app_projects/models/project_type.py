from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy

class ProjectType(models.Model):
    display = models.CharField(
        max_length = 255,
    )

    value = models.CharField(
        max_length = 255,
        unique = True
    )

    def __str__(self):
        return self.display.upper()

    def save(self):
        self.value = slugify(self.display)
        super(ProjectType, self).save()

    class Meta:
        verbose_name = gettext_lazy('Project type')
        verbose_name_plural = gettext_lazy('Project types')
        db_table = 'app_projects_project_type'