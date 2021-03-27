from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
import re

class Path(TranslatableModel):

    page = models.ForeignKey(
        'Page',
        on_delete = models.CASCADE
    )

    translations = TranslatedFields(
        url = models.CharField(
            max_length = 255,
            verbose_name = 'Regex url pattern - groups as parameters',
            null = True,
            blank = True,
        ),
        pattern = models.CharField(
            max_length = 255,
            verbose_name = 'Regex path pattern - groups as parameters'
        )
    )

    def getPage(self):
        return self.page

    def __str__(self):
        return ""

    def save(self):
        url = self.url[1:] if self.url.startswith('/') else self.url
        self.pattern = '^' + re.sub('(?<![\\/])\/', '\/', url + '$')
        super(Path, self).save()
