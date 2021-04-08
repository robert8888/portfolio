from django.urls import path, re_path
from .views.api_contact_phone import process as processContactPhoneRequest
from .views.api_contact_form import process as processContactFormRequest
from .views.download_cv import process as processDownloadCvRequest

urlpatterns = [
    path('api/contact-phone', processContactPhoneRequest),
    path('api/contact-form', processContactFormRequest),
    path('download/cv/<slug:slug>', processDownloadCvRequest, name='cv')
]