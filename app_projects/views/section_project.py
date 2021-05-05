from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import get_language
from app_projects.models import Project
from app_cms.utils.revers_path import revers_page_path


def group_technologies_by_type(technologies):
    technology_grouped = {}
    for tech in technologies:
        group = technology_grouped.get(tech.type.name, [])
        group.append(tech)
        technology_grouped[tech.type.name] = group
    return technology_grouped

def process(request, config, context, *args):
    slug = args[0][0]
    lang = get_language()


    projects = Project.objects.filter(translations__slug=slug, translations__language_code=lang)

    if not slug or not len(projects):
        path = '/'.join(request.path.split('/')[:-1])
        return {
            'redirect': path
        }

    context['project'] = projects[0]
    context['project_technologies'] = group_technologies_by_type(projects[0].technology.all().order_by('type__weight'))

    return context