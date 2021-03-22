from django.db import models
from django.utils.translation import gettext_lazy

from django.contrib.postgres.fields import ArrayField

class ProjectGallery(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Project gallery")
        verbose_name_plural = gettext_lazy("Projects gallery")
        db_table = 'app_projects_project_gallery'

