from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager

class MenuItem(TranslatableModel):
    default_manager = TranslatableManager()

    menu = models.ForeignKey(
        'Menu',
        on_delete = models.CASCADE
    )

    url = models.CharField(
        max_length = 255,
        verbose_name = 'Url',
        default = ''
    )

    text = TranslatedFields(
        value = models.CharField(
            max_length = 255,
            verbose_name = 'Menu item text',
            default = ''
        )
    )

    @property
    def text_translated(self):
        lang = self.get_current_language()
        return self.text.filter(language_code = lang).values('value')[0]['value']