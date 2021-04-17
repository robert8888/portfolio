from django.utils.translation import get_language
from app_index.models import Path, Page
from memoization import cached
import re
import exrex

def replace_capture_groups_with_values(pattern, args):
    output = ''
    for index, part in list(enumerate(re.split('\(\..*?\)', pattern))):
        output += part + (args[index] if index < len(args) else '')
    return output

@cached
def get_path_pattern(page_id=None, page_name = None):
    if not page_id and not page_name: return None
    elif not page_id and page_name:
        page_id_queryset = Page.objects.filter(name=page_name).values('id')
        if not len(page_id_queryset):
            return None
        page_id = page_id_queryset[0].get('id')

    path_queryset = Path.objects.filter(page = page_id, translations__language_code=get_language())

    if not len(path_queryset):
        return None
    path = path_queryset[0]
    return path.pattern

@cached
def revers_page_path(page_id=None, page_name = None, args = None):
    path_pattern = get_path_pattern(page_id=page_id, page_name=page_name)

    if not path_pattern:
        return ''
    pattern = replace_capture_groups_with_values(path_pattern, args ) if args else path_pattern
    return exrex.getone(pattern)

