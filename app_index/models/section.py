from django.db import models
from app_index.utils.getChoices import getTemplatesChoices
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

    position = models.PositiveIntegerField(
        verbose_name = 'Position',
        default = 0,
    )

    def views(self):
        return View.objects.filter(section = self.id)

    def properties(self):
        return Property.objects.filter(section = self.id)


    def __str__(self):
        return self.name

#     def variables(self):
#         return ' - '.join(variable.name for variable in self.variable.all())
#
#     variables.short_description = 'Variables'

    class Meta:
        verbose_name = 'Section'
        ordering = ['position', 'name']

