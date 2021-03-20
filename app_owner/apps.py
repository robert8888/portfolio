from django.apps import AppConfig
from django.utils.translation import gettext_lazy

class AppOwnerConfig(AppConfig):
    name = 'app_owner'
    verbose_name = gettext_lazy('Owner')
