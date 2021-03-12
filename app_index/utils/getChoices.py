from portfolio.utils.readConfigJson import readConfigJson

def getTemplatesChoices(name):
    templates = readConfigJson(['templates', 'TEMPLATES.json'])[name]
    choices = []
    for template in templates:
        choices.append((template['path'], template['name']))
    return choices

def getViewChoices():
    views = readConfigJson(['views', 'VIEWS.json'])["section"]
    choices = []
    for view in views:
        choices.append((view['sysName'], view['name']))
    return choices