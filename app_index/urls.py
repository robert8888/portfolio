from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/contact-form', views.contactForm),
    path('api/contact-phone', views.contactPhone)
]