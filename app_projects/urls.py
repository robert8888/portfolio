from django.urls import path
from .views import api_projects
from .views.api_projects import process as processProjectsRequest
from .views.api_autocomplete import process as processAutocompleteRequest

urlpatterns = [
    path('api/projects', processProjectsRequest , name='projects'),
    path('api/autocomplete', processAutocompleteRequest, name='autocomplete')
]