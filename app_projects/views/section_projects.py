from django.utils.translation import get_language
from django.db import connection
from datetime import datetime
from django.utils.translation import gettext_lazy
from app_projects.models import ProjectGalleryImage
import pydash as py_
import re
from .projects import get as getProjects

def process(request, config, context, *args):
    params = {
        'order': request.GET.get('order', None),
        'type': request.GET.get('type', None),
        'search': request.GET.get('search', None)
    }
    return {
        **context,
        'projects': getProjects(request, params)
    }


