from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager

class MenuItem(TranslatableModel):
    default_manager = TranslatableManager()

    menu = models.ForeignKey(
        'Menu',
        on_delete = models.CASCADE
    )

    translations = TranslatedFields(
        text = models.CharField(
            max_length = 255,
            verbose_name = 'Menu item text',
            default = ''
        ),
        url = models.CharField(
            max_length = 255,
            verbose_name = 'Url',
            default = ''
        )
    )

    def __str__(self):
        return ""

    @property
    def text_translated(self):
        lang = self.get_current_language()
        return self.translations.filter(language_code = lang).values('text')[0]['text']