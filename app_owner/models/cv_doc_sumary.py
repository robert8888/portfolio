from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy

class CvDocumentSummary(TranslatableModel):

    document = models.ForeignKey(
        'Document',
        on_delete = models.CASCADE,
    )

    name = CharField(
        verbose_name = gettext_lazy('Identification name'),
        max_length = 255
    )

    translations = TranslatedFields(
        summary_title = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Summary section tittle')
        )
        summary_content = models.TextField(
            verbose_name = gettext_lazy('Summary content')
        )
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy('Cv document Summary')