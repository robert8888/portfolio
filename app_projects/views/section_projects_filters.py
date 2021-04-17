from app_projects.models import ProjectType
from datetime import datetime
from .projects import ordering

def process(request, config, context, *args):
    context = {
        **context,
        'project_types': ProjectType.objects.all(),
        'project_ordering': [
            {
                'text': type.get('text'),
                'text_type': type.get('textType'),
                'value': type.get('value')
            }
            for type in ordering
        ]
    }
    return context