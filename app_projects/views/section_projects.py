from django.utils.translation import get_language
from django.db import connection
from datetime import datetime
from django.utils.translation import gettext_lazy
from app_projects.models import ProjectGalleryImage
import pydash as py_
import re
import json
from .projects import get as getProjects

def process(request, config, context, *args):
    params = {
        'order': request.GET.get('order', None),
        'type': request.GET.get('type', None),
        'search': request.GET.get('search', None)
    }
    projects = getProjects(request, params)

    json_ld = {
        "@context": "http://schema.org",
        "@type": "ItemList",
        "numberOfItems": len(projects),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "item": json.loads(project["json_ld"])
            } for index, project in enumerate(projects)
        ]
    }

    return {
        **context,
        'projects': projects,
        'json_ld': json_ld
    }


