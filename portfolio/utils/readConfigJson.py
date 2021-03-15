from django.apps import apps
import os
import json
from functools import wraps

def readConfigJson(paths):
    apps_path = [app.path for app in apps.get_app_configs() if app.verbose_name.startswith('App')]
    template_files_paths = list(map(lambda path: os.path.join(path, *paths), apps_path))
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