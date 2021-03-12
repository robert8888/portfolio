from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
#     path('page/', views.PageView.as_view(), name='page'),
    re_path(r'^page/(?P<name>.*)$', views.PageView.as_view(), name='page'),
    path('api/contact-form', views.contactForm),
    path('api/contact-phone', views.contactPhone)
]