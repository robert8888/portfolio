from django.db import models
from app_index.utils.getChoices import getViewChoices

class View(models.Model):
    section = models.ForeignKey(
        'Section',
        on_delete = models.CASCADE,
        related_name = 'section'
    )

    module_name = models.CharField(
        max_length = 255,
        choices = getViewChoices(),
        default = '',
        null = True,
    )

    config = models.JSONField(
        verbose_name = "View json configuration",
        default = dict,
        blank = True
    )