from django.db import models
from .menu_item import MenuItem
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

    template = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Menu template'
    )

    description = models.TextField(
        verbose_name = 'Menu description',
        blank = True,
        null = True,
    )

    def items(self):
        return MenuItem.objects.filter(menu = self.id)

    def __str__(self):
        return self.name