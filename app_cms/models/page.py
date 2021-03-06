from django.db import models
from ..utils.get_template_choices import get_templates_choices
from django_better_admin_arrayfield.models.fields import ArrayField
import re


class Page(models.Model):

    name = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Page name',
        blank = False,
        unique = True
    )

    template = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Page template name',
        choices = get_templates_choices('page')
    )


    section = models.ManyToManyField(
        'Section',
        verbose_name = 'Page sections',
        through = 'PageSections'
    )

    menu = models.ManyToManyField(
        'Menu',
        verbose_name = 'Page menus',
        blank = True
    )

    def sections(self):
        return ', '.join(section.name for sections in self.sections.all())

    sections.short_description = 'Sections'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Page'

