from django.db import models
from django.utils.translation import gettext_lazy

class CvDocumentContact(models.Model):
    document = models.ForeignKey(
        'Document',
        on_delete = models.CASCADE,
    )

    name = models.CharField(
        verbose_name = gettext_lazy('Name')
        max_length = 100
    )

    surname = models.CharField(
        verbose_name = gettext_lazy('Surname')
        max_length = 100
    )

    contacts = models.ManyToManyField(
        'Contact',
        verbose_name = gettext_lazy
    )

    class Meta:
        verbose_name = gettext_lazy('Cv Document contact')