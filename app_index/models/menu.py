from django.db import models

class Menu(models.Model):

#     page = models.ForeignKey(
#         'Page',
#         default = None,
#         on_delete = models.CASCADE
#     )

    name = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Menu identification name',
        unique = True
    )

    description = models.TextField(
        verbose_name = 'Menu description',
        blank = True,
        null = True,
    )