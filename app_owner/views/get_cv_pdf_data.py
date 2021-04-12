from ..models import CV
from dotted_dict import DottedDict
from inspect import getmembers

def process(req, slug):
    cv_queryset = CV.objects.filter(slug = slug).select_related('color_profile', 'data')

    if not len(cv_queryset):
        return DottedDict({
            'success': False
        })

    return DottedDict({
        'success': True,
        'data': {
            'cv': cv_queryset[0]
        }
    })
