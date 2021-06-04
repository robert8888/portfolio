from portfolio.utils.get_apps_views_list import get_apps_views_list
import re

def get_view_choices(pattern = '^section.*'):
    view_list = get_apps_views_list(pattern)
    def formatName(name):
        name = re.sub('\.py', "", name)
        name = re.sub('_', " ", name)
        return ''.join(name[:1].upper() +  name[1:])
    choices = [(item[1], formatName(item[0]))for item in view_list]
    return choices