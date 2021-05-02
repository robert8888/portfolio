from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from django.utils.translation import gettext_lazy

class PageMeta(TranslatableModel):
    page = models.OneToOneField(
        'Page',
        null = True,
        blank = True,
        on_delete = models.CASCADE
    )


    translation = TranslatedFields(
        title = models.CharField(
            max_length = 55,
            default = '',
            verbose_name = gettext_lazy('Page title')
        ),
        meta_title = models.CharField(
            max_length = 55,
            default = '',
            verbose_name=gettext_lazy('Page meta title')
        ),
        meta_description = models.CharField(
            max_length = 255,
            default = ',',
            verbose_name=gettext_lazy('Page meta description')
        )
    )

    class Meta:
        db_table = 'app_cms_page_meta'
        verbose_name = gettext_lazy('Page meta')
        verbose_name_plural = gettext_lazy('Page metas')