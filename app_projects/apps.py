from django.apps import AppConfig
from django.utils.translation import gettext_lazy

class ProjectsAppConfig(AppConfig):
    name = 'app_projects'
    verbose_name = gettext_lazy('Projects')

