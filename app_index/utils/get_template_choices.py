from portfolio.utils.readConfigJson import readConfigJson


def getTemplatesChoices(name):
    templates = readConfigJson(['templates', 'TEMPLATES.json']).get(name, None)
    if not templates: return []
    choices = []
    for template in templates:
        choices.append((template['path'], template['name']))
    return choices
