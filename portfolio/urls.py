from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from app_projects import views as projectsViews

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    ## from plugins
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('_nested_admin/', include('nested_admin.urls')),
]

urlpatterns += i18n_patterns(
    path('projects/', projectsViews.projects),
    path('project', projectsViews.project),
    path('admin/', admin.site.urls),
    path('', include('app_index.urls')),
    prefix_default_language=False
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
