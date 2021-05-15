from django.contrib import admin
from django.urls import include, re_path, path
from django.conf.urls import url

from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from app_projects import views as projectsViews
from django.views.generic import TemplateView
from .s3proxy import s3proxy
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns
from app_cms.sitemaps import NotParameterizedViewSitemap
from app_projects.sitemaps import ProjectViewSitemap

handler404 = 'app_cms.views.handler404'
handler500 = 'app_cms.views.handler500'

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('_nested_admin/', include('nested_admin.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': {
        'basic': NotParameterizedViewSitemap,
        'projects': ProjectViewSitemap
    }}),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

urlpatterns += i18n_patterns(
    path('s3image', s3proxy),
    path('admin/', admin.site.urls),
    url('', include('pwa.urls')),
    path('', include('app_owner.urls')),
    path('', include('app_projects.urls')),
    path('', include('app_cms.urls')),
    prefix_default_language= settings.PREFIX_DEFAULT_LANGUAGE
)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

