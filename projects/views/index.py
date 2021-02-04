from django.shortcuts import render
from projects.models import Technology, Project

def index(request):
#     print("hello--------------------")
#     print(Project.technologies.through.objects.filter())
    context = {}
    return render(request, 'index.html', context = context)