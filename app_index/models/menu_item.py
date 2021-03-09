from django.db import models

class MenuItem(models.Model):

    menu = models.ForeignKey(
        'Menu',
        on_delete = models.CASCADE
    )

    text = models.CharField(
        max_length = 255,
        verbose_name = 'Text',
        default = ''
    )

    url = models.CharField(
        max_length = 255,
        verbose_name = 'Url',
        default = ''
    )