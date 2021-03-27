from django.db import models
from django.utils.translation import gettext_lazy
from django_better_admin_arrayfield.models.fields import ArrayField

class ProjectLink(models.Model):
    type_of_links = (
        ('host', gettext_lazy('Host')),
        ('repo', gettext_lazy('Repository')),
        ('demo', gettext_lazy('Demo')),
        ('docs', gettext_lazy('Documentation'))
    )

    project = models.ForeignKey(
        'Project',
        on_delete = models.CASCADE,
    )

    type = models.CharField(
        max_length = 255,
        choices = type_of_links
    )

    url = ArrayField(
        models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Link')
        )
    )

    class Meta:
        verbose_name = gettext_lazy('Project link')
        verbose_name_plural = gettext_lazy('Project links')
        db_table = 'app_project_project_link'