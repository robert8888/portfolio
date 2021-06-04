from portfolio.utils.read_config_json import read_config_json


def get_templates_choices(name):
    templates = read_config_json(['templates', 'TEMPLATES.json']).get(name, None)
    if not templates: return []
    choices = []
    for template in templates:
        choices.append((template['path'], template['name']))
    return choices
