from django.shortcuts import render
from projects.models import Technology, Project
from django.db.models import Count
from projects.queries import get_top_technology
from django.middleware.csrf import get_token

def index(request):
    technologies_ordered = get_top_technology()

    context = {
        'gCaptchaPublicKey': '6LfPq2QaAAAAAGpz3x-4KiBjNF3zffwFOVhlXHjD',
        'csrfToken': get_token(request)
    }
    return render(request, 'index.html', context = context)