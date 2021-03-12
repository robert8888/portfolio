from app_index.models import PageSections

def getPageSections(page):
    sections = [relation.section for relation in PageSections.objects.filter(page = page.id).order_by('order')]
    sections_data = []
    for section in sections:
        section_data = {
            'template': section.template,
            'props': [{
                'name': prop.name,
                'value': prop.value
            } for prop in section.properties()]
        }
        sections_data.append(section_data)
    return sections_data