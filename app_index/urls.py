from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/contact-form', views.contactForm),
#     path('api/contact-phone', views.contactPhone),
    re_path(r'^(?!api)(?P<path>.*)$', views.PageView.as_view(), name='page'),
]