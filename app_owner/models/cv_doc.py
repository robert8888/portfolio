from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy

class Document(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    class Meta:
        verbose_name = gettext_lazy('Cv document')