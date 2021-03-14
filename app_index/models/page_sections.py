from django.db import models

class PageSections(models.Model):
    page = models.ForeignKey(
        'Page',
        on_delete = models.CASCADE
    )

    section = models.ForeignKey(
        'Section',
        on_delete = models.CASCADE
    )

    order = models.PositiveIntegerField(
        verbose_name = 'Order',
        default = 0,
    )