from django.utils.translation import get_language
from ..models import Path, Page
from django.conf import settings
from memoization import cached
from itertools import chain
import re
import exrex

def replace_capture_groups_with_values(pattern, args):
    output = ''
    for index, part in list(enumerate(re.split('\(\..*?\)', pattern))):
        output += part + (args[index] if index < len(args) else '')
    return output

def get_page_id(page_name):
    if not page_name:
        return None

    page_id_queryset = Page.objects.filter(name=page_name).values('id')

    if not len(page_id_queryset):
        return None

    return page_id_queryset[0].get('id')

@cached
def get_path_pattern(page_id=None, page_name = None):
    if not page_id and not page_name:
        return None
    elif not page_id and page_name:
        page_id = get_page_id(page_name)

    path_queryset = Path.objects.filter(page_id = page_id, translations__language_code=get_language())


    if not len(path_queryset):
        return None
    path = path_queryset[0]

    return path.pattern

@cached
def get_path_patterns(page_id=None, page_name=None):
    if not page_id and not page_name:
        return None
    page_id = page_id if page_id else get_page_id(page_name)
    path_querysets = [
        Path.objects.filter(page_id = page_id).language(lang_code)
        for lang_code, _ in settings.LANGUAGES
    ]
    return list(chain(*path_querysets))


@cached
def revers_page_path(page_id=None, page_name = None, args = None):
    path_pattern = get_path_pattern(page_id=page_id, page_name=page_name)
    if not path_pattern:
        return ''
    pattern = replace_capture_groups_with_values(path_pattern, args ) if args else path_pattern
    path = exrex.getone(pattern)
    return "/" + path if not path.startswith("/") else path


@cached
def revers_page_paths(page_name = None, lang_args = None):
    paths_queries = [(path.pattern, path.language_code )for path in get_path_patterns(page_name = page_name)]
    paths = []

    for path in paths_queries:
        lang = path[1]
        args = lang_args.get(lang, None)
        pattern = replace_capture_groups_with_values(path[0], args) if args else path[0]
        for url in exrex.generate(pattern):
            paths.append((url, path[1]))

    return paths