from django.apps import apps
from django.conf import settings
import os
import json
from functools import wraps

def readConfigJson(paths):
    template_files_paths = []

    if settings.TEMPLATES[0]['APP_DIRS']:
        apps_path = [app.path for app in apps.get_app_configs()]
        template_files_paths = list(map(lambda path: os.path.join(path, *paths), apps_path))
    if settings.TEMPLATES[0]['DIRS']:
        template_files_paths += list(map(lambda path: os.path.join(path, *[path for path in paths if not path == 'templates']), settings.TEMPLATES[0]['DIRS']))

    template_files_paths = [file_path for file_path in template_files_paths if os.path.exists(file_path)]

    data = {}
    for path in template_files_paths:
        with open(path) as json_file:
            part = json.load(json_file)
            data = merge(data, part)
    return data

def merge(base, head):
    for key in head:
        if base.get(key):
            base[key] = [*base[key], *head[key]]
        else:
            base[key] = head[key]
    return base