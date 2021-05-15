from django.contrib.sitemaps import Sitemap
from app_cms.utils.revers_path import revers_page_paths
from django.conf import settings
from .models import Project
from itertools import chain

class ProjectViewSitemap(Sitemap):
    def items(self):
        projects  = list(chain(*[Project.objects.all().language(lang_code) for lang_code, _ in settings.LANGUAGES]))

        slugs = {}
        for project in projects:
            key = project.id
            slugs[key] = {
                **slugs.get(key, {}),
                project.language_code: [project.slug]
            }

        items = []
        for lang_slugs in list(slugs.values()):
            paths = revers_page_paths(page_name='Project', lang_args= lang_slugs)
            for path in paths:
                items.append(path)

        return items

    def location(self, item):
        path, lang = item
        prefix = lang if not settings.PARLER_DEFAULT_LANGUAGE_CODE == lang and not settings.PREFIX_DEFAULT_LANGUAGE else ''

        url = '/'
        if prefix:
            url += prefix + '/'
        url += path

        return url
