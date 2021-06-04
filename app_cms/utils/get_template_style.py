from portfolio.utils.read_config_json import read_config_json

def getTemplateStyle(type, template_path):
    templates = read_config_json(['templates', 'TEMPLATES.json'])[type]
    for template in templates:
        if template['path'] == template_path:
            return template.get('style')
    return None