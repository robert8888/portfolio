from django.urls import path, re_path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    re_path(r'^(?!(api))(?P<path>.*)$', views.PageView.as_view(), name='page'),
]