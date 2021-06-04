from django.db import models
from ..utils.get_view_choices import get_view_choices

class View(models.Model):
    section = models.ForeignKey(
        'Section',
        on_delete = models.CASCADE,
        related_name = 'section'
    )

    module_name = models.CharField(
        max_length = 255,
        choices = get_view_choices(),
        default = '',
        null = True,
    )

    config = models.JSONField(
        verbose_name = "View json configuration",
        default = dict,
        blank = True
    )