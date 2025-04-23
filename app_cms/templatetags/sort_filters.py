from django import template

register = template.Library()

@register.filter
def group_and_sort(technologies):
    return sorted(
        technologies,
        key=lambda tech: ( tech.weight_cv)
    )
