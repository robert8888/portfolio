from django.db import models

class Section(models.Model):

    page = models.ForeignKey(
        'Page',
        default = None,
        on_delete = models.CASCADE
    )

    name = models.CharField(
        verbose_name = 'Section identification name',
        max_length = 255,
        help_text = 'only letters',
        unique = True,
    )

    template = models.CharField(
        max_length = 255,
        default = '',
        verbose_name = 'Section template name'
    )

    position = models.PositiveIntegerField(
        verbose_name = 'Position',
        default = 0,
    )

#     def variables(self):
#         return ' - '.join(variable.name for variable in self.variable.all())
#
#     variables.short_description = 'Variables'

    class Meta:
        verbose_name = 'Section'
        ordering = ['position', 'name']

