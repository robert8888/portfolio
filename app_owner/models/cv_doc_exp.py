from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from django_better_admin_arrayfield.models.fields import ArrayField

class CVDocumentExperience(models.Model):

    id_name = models.CharField(
        verbose_name = gettext_lazy("Identification name"),
        max_length = 100
    )

    def __str__(self):
        return self.id_name

    class Meta:
        verbose_name = gettext_lazy('CV document experience')
        verbose_name_plural = gettext_lazy('CV documents experiences')
        db_table = 'app_owner_cv_doc_exp'

class CVDocumentExperienceJob(TranslatableModel):

    experience = models.ForeignKey(
        'CVDocumentExperience',
        on_delete = models.CASCADE,
    )

    company = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Company')
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
        description = ArrayField(
            models.TextField(
                verbose_name = gettext_lazy('Description'),
            ),
        )
    )

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = gettext_lazy('Job')
        verbose_name_plural = gettext_lazy('Jobs')
        db_table = 'app_owner_cv_doc_exp_job'

