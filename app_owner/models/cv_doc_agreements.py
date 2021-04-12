from django.db import models
from django.utils.translation import gettext_lazy
from parler.models import TranslatableModel,TranslatedFields

class CVDocumentAgreements(TranslatableModel):
    id_name = models.CharField(
        max_length = 255,
        verbose_name = gettext_lazy('Identification name')
    )

    translation = TranslatedFields(
        text = models.TextField(
            verbose_name = gettext_lazy('Agreements text')
        )
    )

    def __str__(self):
        return self.id_name

    class Meta:
        verbose_name = gettext_lazy('Cv document agreements')
        verbose_name_plural = gettext_lazy('Cv document agreements')
        db_table = 'app_owner_cv_doc_agreements'