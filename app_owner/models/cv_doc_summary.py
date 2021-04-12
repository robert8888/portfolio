from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy

class CVDocumentSummary(TranslatableModel):

    id_name = models.CharField(
        verbose_name = gettext_lazy('Identification name'),
        max_length = 255
    )

    translations = TranslatedFields(
        summary_title = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Summary section tittle')
        ),

        summary_content = models.TextField(
            verbose_name = gettext_lazy('Summary content')
        )
    )

    def __str__(self):
        return self.id_name

    class Meta:
        verbose_name = gettext_lazy('CV document Summary')
        db_table = 'app_owner_cv_doc_sum'