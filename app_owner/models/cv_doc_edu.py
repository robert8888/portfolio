from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from django_better_admin_arrayfield.models.fields import ArrayField


class CvDocumentEducation(models.Model):
    document = models.ForeignKey(
        'Document',
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name = gettext_lazy('Cv document education')
        verbose_name_plural = gettext_lazy('Cv documents educations')


class School(TranslatableModel):

    education = models.ForeignKey(
        'CvDocumentEducation',
        on_delete = models.CASCADE,
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
        school = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('School name')
        ),

        field = models.TextField(
            max_length = 255,
            verbose_name = gettext_lazy('Field of study')
        )

        description = models.TextField(
            verbose_name = gettext_lazy('Description')
        )
    )

    class Meta:
        verbose_name = gettext_lazy('School')
        verbose_name_plural = gettext_lazy('Schools')
