from django.shortcuts import render
from projects.models import Technology, Project
from django.db.models import Count
from projects.queries import get_top_technology

def index(request):
    technologies_ordered = get_top_technology()

    context = {}
    return render(request, 'index.html', context = context)