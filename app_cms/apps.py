from django.apps import AppConfig
from django.utils.translation import gettext_lazy

class CmsAppConfig(AppConfig):
    name = 'app_cms'
    verbose_name = gettext_lazy("Pages - CMS")

    def ready(self):
        import app_cms.signals
