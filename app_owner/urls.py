from django.urls import path, re_path
from .views.api_contact_phone import process as processContactPhoneRequest

urlpatterns = [
    path('api/contact-phone', processContactPhoneRequest),
]