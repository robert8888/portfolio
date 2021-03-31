from django.db import models
from django.utils.translation import gettext_lazy

class CV(models.Model):
    Templates = (
        ('test', 'test'),
    )

    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Version name')
    )

    template = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('PDF template'),
        blank = True,
        choices = Templates,
    )

    data = models.ForeignKey(
        'CVDocument',
        on_delete = models.RESTRICT,
        null = True,
        blank = True
    )

    class Meta:
        verbose_name = "CV PDF"
        verbose_name_plural = "CV PDFs"