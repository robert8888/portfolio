from django.db import models
from app_index.utils.getChoices import getViewChoices

class View(models.Model):
    section = models.ForeignKey(
        'Section',
        on_delete = models.CASCADE,
    )

    name = models.CharField(
        max_length = 255,
        choices = getViewChoices(),
        default = '',
        null = True,
    )