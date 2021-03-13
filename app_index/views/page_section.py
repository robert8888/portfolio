from app_index.models import PageSections

def getPageSections(page):
    sections = [relation.section for relation in PageSections.objects.filter(page = page.id).order_by('order')]
    sections_data = []
    for section in sections:
        props = {}
        for prop in section.properties():
            props[prop.name] = prop.value
        section_data = {
            'template': section.template,
            'style': section.style,
            'props': props
        }
        sections_data.append(section_data)
    return sections_data