from app_projects.models import Technology
from django.utils.translation import get_language
from portfolio.utils.execute_db_queries import execute_queries
from portfolio.s3proxy import generatePresignedUrl
from django.conf import settings

# code below made in django way const 1s of rendering
# def process(request, config, context, *args):
#     technologies = Technology.objects.all().order_by('type__weight')
#     main = Technology.objects.filter(show_on_index = True).order_by('type__weight')
#     main = group_technologies_by_type(main)
#
#     all = Technology.objects.filter(show_on_index_all = True).order_by('type__weight')
#     all = group_technologies_by_type(all)
#
#     context['technologies_main'] = main
#     context['technologies_all'] = all
#     print(Technology.objects.select_related().first())
#
#     return context

def buildQuery():
    lang = get_language()
    return f"""
    SELECT
    app_projects_technologytype_translation.name as "technology_type",
    app_projects_technology.name as "name",
    app_projects_technology.show_on_index as "show_on_index",
    app_projects_technology.show_on_index_all as "show_on_index_all",
    app_projects_technology.color as "color",
    app_projects_technology.link as "link",
    app_projects_image.source as "image_url",
    app_projects_technologyimagesprite.left as "left",
    app_projects_technologyimagesprite.top as "top",
    (CASE
      WHEN app_projects_technologyimagesprite.width IS NOT NULL
      THEN app_projects_technologyimagesprite.width
      ELSE app_projects_image.width
    END) as "width",
    (CASE
      WHEN app_projects_technologyimagesprite.height IS NOT NULL
      THEN app_projects_technologyimagesprite.height
      ELSE app_projects_image.height
    END) as "height",
    (CASE
      WHEN app_projects_technologyimagesprite.width IS NOT NULL
        THEN TRUE
      ELSE FALSE
    END) as "is_image_sprite"
    FROM app_projects_technology
    LEFT JOIN app_projects_technologyimage ON app_projects_technologyimage.technology_id = app_projects_technology.id
    LEFT JOIN app_projects_technologyimagestd ON app_projects_technologyimagestd.technologyimage_ptr_id = app_projects_technologyimage.id
    LEFT JOIN app_projects_technologyimagesprite ON app_projects_technologyimagesprite.technologyimage_ptr_id = app_projects_technologyimage.id
    LEFT JOIN app_projects_image ON app_projects_technologyimage.image_id = app_projects_image.id
    LEFT JOIN app_projects_technologytype ON app_projects_technology.type_id = app_projects_technologytype.id
    LEFT JOIN app_projects_technologytype_translation ON app_projects_technologytype_translation.master_id = app_projects_technologytype.id
    WHERE (app_projects_technology.show_on_index = TRUE
    OR app_projects_technology.show_on_index_all = TRUE)
    AND app_projects_technologytype_translation.language_code = '{lang}'
    ORDER BY app_projects_technologytype.weight
    """
def map_images(technology):
    if technology['image_url']:
        technology['image_url'] = generatePresignedUrl(settings.MEDIA_ROOT_PATH + technology['image_url'])
    return technology

def group_by_type(technologies):
    technologies_grouped = {}
    for technology in technologies:
        group = technologies_grouped.get(technology['technology_type'], [])
        group.append(technology)
        technologies_grouped[technology['technology_type']] = group
    return technologies_grouped

def process(request, config, context, *args):
    try:
        data = execute_queries([buildQuery()])
        if not data.get('successAll'):
            return context

        technologies = data['resultEach'][0]['data']
        technologies = [map_images(technology) for technology in technologies]

        main = []
        all = []
        for technology in technologies:
            if technology['show_on_index']:
                main.append(technology)
            if technology['show_on_index_all']:
                all.append(technology)

        context['technologies_main'] = group_by_type(main)
        context['technologies_all'] = group_by_type(all)
        print(group_by_type(all))
    except BaseException as error:
        print(error)
    finally:
        return context
