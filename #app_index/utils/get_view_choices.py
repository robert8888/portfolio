from portfolio.utils.getAppsViewsList import getAppsViewsList
import re

def getViewChoices(pattern = '^section.*'):
    view_list = getAppsViewsList(pattern)
    def formatName(name):
        name = re.sub('\.py', "", name)
        name = re.sub('_', " ", name)
        return ''.join(name[:1].upper() +  name[1:])
    choices = [(item[1], formatName(item[0]))for item in view_list]
    return choices