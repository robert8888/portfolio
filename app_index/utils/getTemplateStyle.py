from portfolio.utils.readConfigJson import readConfigJson

def getTemplateStyle(type, template_path):
    templates = readConfigJson(['templates', 'TEMPLATES.json'])[type]
    for template in templates:
        if template['path'] == template_path:
            return template.get('style')
    return None