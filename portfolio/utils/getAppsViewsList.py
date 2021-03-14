from django.apps import apps
from functools import reduce
import os
import re
def getAppsViewsList(pattern = '.*'):
    regex = re.compile(pattern)
    app_dirs = [
        {'path': os.path.join(app.path, 'views'), 'name': app.name}
        for app in apps.get_app_configs()
            if app.verbose_name.startswith('App')
    ]
    views_list = []
    for app in app_dirs:
         views_list += [
            (view_name, app['name'] + '.views.' + view_name)
            for view_name in os.listdir(app['path'])
                if regex.search(view_name)
        ]
    return views_list
