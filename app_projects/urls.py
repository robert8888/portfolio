from django.urls import path
from .views import api_projects
from .views.api_projects import process as processProjectsRequest

urlpatterns = [
    path('api/projects', processProjectsRequest , name='projects'),
]