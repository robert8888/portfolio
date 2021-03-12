
def getMenus(page):
    def transformMenu(menu):
        return {
            'name': menu.name,
            'template': menu.template,
            'items': [{
                'url': item.url,
                'text': item.text.get(language_code = item.get_current_language()).value
            } for item in menu.items()]
        }
    menus = list(map(transformMenu, page.menu.all()))
    return menus