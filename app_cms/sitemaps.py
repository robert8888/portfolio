from django.contrib.sitemaps import Sitemap
from .models import Path
from django.conf import settings
import exrex
from itertools import chain

class NotParameterizedViewSitemap(Sitemap):
    def items(self):
        paths =  [
            # catch only this one that doesn't have open group in pattern
            Path.objects.exclude(translations__pattern__contains = '.*').language(lang_code)
            for lang_code, _ in settings.LANGUAGES
        ]
        items = []
        for path in list(chain(*paths)):
            patterns = list(exrex.generate(path.pattern))
            for pattern in patterns:
                items.append((pattern, path.language_code))

        return items

    def location(self, item):
        path, lang = item
        prefix = lang if not settings.PARLER_DEFAULT_LANGUAGE_CODE == lang and not settings.PREFIX_DEFAULT_LANGUAGE else ''

        url = '/'
        if prefix:
            url += prefix + '/'
        url += path

        return url


