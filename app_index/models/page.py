from django.db import models

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
        verbose_name = 'Page template name'
    )

#     section = models.ManyToManyField(
#         'Section',
#         verbose_name = 'Page sections',
#         blank = True
#     )

    menus = models.ManyToManyField(
        'Menu',
        verbose_name = 'Page menus',
        blank = True
    )

    def sections(self):
        return ', '.join(section.name for sections in self.sections.all())

    sections.short_description = 'Sections'

    class Meta:
        verbose_name = 'Page'