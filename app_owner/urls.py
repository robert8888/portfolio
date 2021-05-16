from django.urls import path, re_path
from .views.api_contact_phone import process as processContactPhoneRequest
from .views.api_contact_email import process as processContactEamilRequest
from .views.api_contact_form import process as processContactFormRequest
from .views.api_cv_pdf import CvPdf

urlpatterns = [
    path('api/contact-phone', processContactPhoneRequest),
    path('api/contact-email', processContactEamilRequest),
    path('api/contact-form', processContactFormRequest),
    path('download/cv/<slug:slug>', CvPdf.as_view(), name='cv'),
    path('api/get-cv', CvPdf.as_view())
]