from django import template

register = template.Library()

@register.filter
def group_and_sort(technologies):
    return sorted(
        technologies,
        key=lambda tech: (tech.type.weight, tech.weight, -tech.skill_level)
    )
