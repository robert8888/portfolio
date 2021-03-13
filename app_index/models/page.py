from django.db import models
from app_index.utils.getChoices import getTemplatesChoices

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

class Page(models.Model):

    name = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Page name',
        blank = False,
        unique = True
    )

    address = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Pager url address',
        unique = True
    )

    template = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Page template name',
        choices = getTemplatesChoices('page')
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

    class Meta:
        verbose_name = 'Page'

