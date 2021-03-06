from portfolio.utils.read_config_json import read_config_json
from ..models import CVColorProfile
from django.conf import settings
import os

def process(request, config, context, *args):
    context['cv_template_names'] = [
        (tpl.get('slug'), tpl.get('name')) for tpl in read_config_json(['templates', 'TEMPLATES.json']).get('pdf', None)
        if os.path.exists(os.path.join(settings.BASE_DIR, 'assets', 'img', 'pdf', 'cv_preview', tpl.get('slug') + '.svg'))
    ]
    context['cv_color_profiles'] = CVColorProfile.objects.all()

    return context