from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from sortedm2m.fields import SortedManyToManyField
from app_index.utils.getTemplateChoices import getTemplatesChoices

class CVDocument(models.Model):

    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    photo = models.ForeignKey(
        'CVDocumentPhoto',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Photo')
    )

    contact = models.ForeignKey(
        'CVDocumentContact',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Contact data')
    )

    summary = models.ForeignKey(
        'CVDocumentSummary',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Summary')
    )

    education = models.ForeignKey(
        'CVDocumentEducation',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Education')
    )

    experience = models.ForeignKey(
        'CVDocumentExperience',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Experience')
    )

    skills = models.ForeignKey(
        'CVDocumentSkills',
        on_delete = models.RESTRICT,
        verbose_name = gettext_lazy('Skills')
    )

    additional = SortedManyToManyField(
        'CVDocumentAdditional',
        verbose_name = gettext_lazy('Additional'),
    )

    class Meta:
        verbose_name = gettext_lazy('CV Document')
        verbose_name_plural = gettext_lazy('CV Documents')
        db_table = 'app_owner_cv_doc'

