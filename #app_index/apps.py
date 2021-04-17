from django.apps import AppConfig
from django.utils.translation import gettext_lazy

class IndexAppConfig(AppConfig):
    name = 'app_index'
    verbose_name = gettext_lazy("Pages - CMS")
