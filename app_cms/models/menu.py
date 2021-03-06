from django.db import models
from .menu_item import MenuItem
from ..utils.get_template_choices import get_templates_choices
from ..utils.get_template_style import getTemplateStyle

class Menu(models.Model):
    name = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Menu identification name',
        unique = True
    )

    template = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Menu template',
        choices = get_templates_choices('menu')
    )

    style = models.CharField(
        max_length = 255,
        default = '',
        null = True,
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

    def save(self):
        self.style = getTemplateStyle('menu', self.template)
        super(Menu, self).save()