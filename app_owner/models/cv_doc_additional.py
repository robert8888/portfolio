from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy

class CvDocumentAdditional(TranslatableModel):

    document = models.ForeignKey(
        'Document',
        on_delete = models.CASCADE,
    )

    Type = (
        ('hobby', gettext_lazy('Hobby')),
        ('other', gettext_lazy('Other'))
    )

    type = models.CharField(
        max_length = 50,
        verbose_name = gettext_lazy('Type')
    )

    translation = TranslatedFields(
        title = models.CharField(
            max_length = 255,
            verbose_name = gettext_lazy('Title')
        )
        items = ArrayField(
            models.CharField(
                max_length = 255,
                verbose_name = gettext_lazy('Items')
            )
        )
    )

    class Meta:
        verbose_name = gettext_lazy('Cv document additional info')
        verbose_name_plural = gettext_lazy('Cv document additional infos')