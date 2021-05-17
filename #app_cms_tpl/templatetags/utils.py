from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
import ast
import re
import json

@register.simple_tag
def to_list(*args):
    return args

@register.simple_tag
def concat_all(*args):
    return ''.join(map(str, args))

@register.simple_tag
def get_dict_value(_dict, key):
    return _dict.get(key, None)

@register.filter
def get_dict_value(_dict, key):
    return _dict.get(key, None)


import ast
@register.simple_tag
def create_dict(str_dict):
    _dict = ast.literal_eval(str_dict)
    return _dict

@register.filter
def to_camel_case(input_str):
    parts = re.split('[_-]', input_str)
    return parts[0] + ''.join([x.title() for x in parts[1:]])

@register.filter
def pretty_json(json_input):
    if isinstance(json_input, str):
        return json.dumps(json.loads(json_input), indent=4)
    elif isinstance(json_input, dict):
        return json.dumps(json_input, indent=4)
    else:
        return json_input

@register.simple_tag(takes_context=True)
def support_webp(context):
    request = context['request']
    return request.META.get('HTTP_ACCEPT').find('image/webp') != -1