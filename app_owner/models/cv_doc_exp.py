from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from django_better_admin_arrayfield.models.fields import ArrayField

class CvDocumentExperience(models.Model):
    document = models.ForeignKey(
        'Document',
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name = gettext_lazy('Cv document experience')
        verbose_name_plural = gettext_lazy('Cv documents experiences')

class Job(TranslatableModel):

    experience = models.ForeignKey(
        'CvDocumentExperience',
        on_delete = models.CASCADE,
    )

    company = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Company')
    )

    from = models.DateField(
        auto_now = False,
        verbose_name = gettext_lazy('From')
    )

    to = models.DateField(
        auto_now = False,
        verbose_name = gettext_lazy('To')
    )

    translation = TranslatedFields(
        description = models.ArrayField(
            models.TextField(
                verbose_name = gettext_lazy('Description')
            )
        )
    )

    class Meta:
        verbose_name = gettext_lazy('Job')
        verbose_name_plural = gettext_lazy('Jobs')
