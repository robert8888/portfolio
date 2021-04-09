from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy
from django_better_admin_arrayfield.models.fields import ArrayField

class CVDocumentAdditional(TranslatableModel):

    id_name = models.CharField(
        verbose_name = gettext_lazy("Identification name"),
        max_length = 100
    )

    Type = (
        ('hobby', gettext_lazy('Hobby')),
        ('strength', gettext_lazy('Strengths')),
        ('achievements', gettext_lazy('Achievements')),
        ('other', gettext_lazy('Other'))
    )

    type = models.CharField(
        max_length = 50,
        verbose_name = gettext_lazy('Type'),
        choices = Type,
    )

    translation = TranslatedFields(
        title = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Title')
        ),
        items = ArrayField(
            models.CharField(
                max_length = 255,
                verbose_name = gettext_lazy('Items')
            )
        )
    )

    def __str__(self):
        return self.id_name + ' - ' + self.type

    class Meta:
        verbose_name = gettext_lazy('CV document additional info')
        verbose_name_plural = gettext_lazy('CV document additional infos')
        db_table = 'app_owner_cv_doc_add'