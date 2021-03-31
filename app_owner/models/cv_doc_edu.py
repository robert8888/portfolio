from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from django_better_admin_arrayfield.models.fields import ArrayField


class CVDocumentEducation(models.Model):

    id_name = models.CharField(
        verbose_name = gettext_lazy("Identification name"),
        max_length = 100
    )

    class Meta:
        verbose_name = gettext_lazy('CV document education')
        verbose_name_plural = gettext_lazy('CV documents educations')
        db_table = 'app_owner_cv_doc_edu'


class CVDocumentEducationSchool(TranslatableModel):

    education = models.ForeignKey(
        'CVDocumentEducation',
        on_delete = models.CASCADE,
    )

    from_date = models.DateField(
        auto_now = False,
        verbose_name = gettext_lazy('From')
    )

    to_date = models.DateField(
        auto_now = False,
        verbose_name = gettext_lazy('To')
    )

    translation = TranslatedFields(
        school = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('School name')
        ),

        field = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Field of study')
        ),

        description = models.TextField(
            verbose_name = gettext_lazy('Description')
        )
    )

    class Meta:
        verbose_name = gettext_lazy('School')
        verbose_name_plural = gettext_lazy('Schools')
        db_table = 'app_owner_cv_doc_edu_school'
