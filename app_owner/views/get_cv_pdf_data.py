from ..models import CV
from dotted_dict import DottedDict

def process(req, slug):
    cv_queryset = CV.objects.filter(slug = slug).select_related('color_profile', 'data')
    print(cv_queryset[0].color_profile.colors)

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
