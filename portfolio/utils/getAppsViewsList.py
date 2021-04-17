from django.apps import apps
from functools import reduce
import os
import re
def getAppsViewsList(pattern = '.*'):
    regex = re.compile(pattern)

    view_dir_path = lambda path: os.path.join(path, 'views')

    app_dirs = [
        {'path': view_dir_path(app.path), 'name': app.name}
        for app in apps.get_app_configs()
            if app.name.startswith('app') and os.path.isdir(view_dir_path(app.path))
    ]

    views_list = []
    for app in app_dirs:
         views_list += [
            (view_name, app['name'] + '.views.' + view_name)
            for view_name in os.listdir(app['path'])
                if regex.search(view_name)
        ]
    return views_list
