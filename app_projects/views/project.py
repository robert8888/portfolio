from django.shortcuts import render;

def project(request):
    context = {

    }
    return render(request, "project.html", context = context)
