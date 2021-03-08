from django.shortcuts import render

def projects(request):
    context = {

    }

    return render(request, "projects.html", context = context)