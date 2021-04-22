from ..models import CV, CVDocument, CVColorProfile
from dotted_dict import DottedDict
from inspect import getmembers

def process(req, data):
    if data.get('slug', None):
        cv_queryset = CV.objects.filter(slug = data['slug']).select_related('color_profile', 'data')
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


    color_profile = CVColorProfile.objects.get(pk = data['colorProfileId'])
    cv_data = CVDocument.objects.filter(on_main_page = True)

    if not color_profile or not len(cv_data):
        return DottedDict({
            'success': False
        })

    return DottedDict({
        'success': True,
        'data': {
            'cv': {
                'color_profile': color_profile,
                'data': cv_data[0]
            }
        }
    })

