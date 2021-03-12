from django import template

register = template.Library()

# def tpl_url(value, prefix = 'includes/'):
#     print(value)
#     return value
#     return prefix + value + '.html'
#
# register.filter('tpl_url', tpl_url)

@register.simple_tag
def tpl_url(value, prefix = 'includes/'):
    return prefix + value + '.html'

