from django import template
from ..utils.revers_path import revers_page_path
register = template.Library()

@register.simple_tag
def get_path(*args, page_id = None, page_name = None ):
    try:
        return revers_page_path(page_id = page_id, page_name = page_name, args = args)
    except:
        return ''

