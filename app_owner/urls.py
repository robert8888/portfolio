from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/contact-phone', views.contactPhone),
]