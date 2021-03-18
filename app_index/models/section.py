from django.db import models
from app_index.utils.getTemplateChoices import getTemplatesChoices
from app_index.utils.getTemplateStyle import getTemplateStyle
from .view import View
from .property import Property

class Section(models.Model):

    name = models.CharField(
        verbose_name = 'Section identification name',
        max_length = 255,
        help_text = 'only letters',
        unique = True,
    )

    template = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Section template name',
        choices = getTemplatesChoices('section')
    )

    style = models.CharField(
        max_length = 255,
        default = '',
        null = True,
    )

    def views(self):
        return View.objects.filter(section = self.id)

    def properties(self):
        return Property.objects.filter(section = self.id)

    def __str__(self):
        return self.name

    def save(self):
        self.style = getTemplateStyle('section', self.template)
        super(Section, self).save()

    class Meta:
        verbose_name = 'Section'
        ordering = ['name']

