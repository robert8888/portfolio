from django.utils.translation import get_language
from django.db import connection
from django.utils.translation import gettext_lazy
from app_projects.models import ProjectGalleryImage
from app_cms.utils.revers_path import revers_page_path
from sqlescapy import sqlescape
from portfolio.utils.execute_db_queries import execute_queries
import pydash as py_
import re

ordering = [{
    "column": "app_projects_project.sort_weight",
    "type": "ASC",
    "value": "weight",
    "text": gettext_lazy("Default"),
    "textType": "-",
    "default": True
},{
    "column": "app_projects_project.release_date",
    "type": "ASC",
    "value": "data_asc",
    "text": gettext_lazy("Release date"),
    "textType": "↑"
},{
    "column": "app_projects_project.release_date",
    "type": "DESC",
    "value": "date_dsc",
    "text": gettext_lazy("Release date"),
    "textType": "↓"
},{
    "column": "app_projects_project_translation.name",
    "type": "ASC",
    "value": "name_asc",
    "text": gettext_lazy("Name"),
    "textType": "A-Z"
},{
    "column": "app_projects_project_translation.name",
    "type": "DESC",
    "value": "name_dsc",
    "text": gettext_lazy("Name"),
    "textType": "Z-A"
},{
    "column": "app_projects_project_type.value",
    "type": "ASC",
    "value": "type_asc",
    "text": gettext_lazy("Type"),
    "textType": "A-Z"
},{
    "column": "app_projects_project_type.value",
    "type": "DESC",
    "value": "type_dsc",
    "text": gettext_lazy("Type"),
    "textType": "Z-A"
}]

def build_get_projects_query(lang, filter, order, project_page_path):
    return f"""
    SELECT
    app_projects_project.id as "id",
    app_projects_project_translation.name as "name",
    app_projects_project_translation.slug as "slug",
    app_projects_project_translation.title as "title",
    app_projects_project_translation.subtitle as "subtitle",
    app_projects_project_translation.description_short as "description",
    app_projects_project_translation.json_ld as "json_ld",
    app_projects_project_type.display as "type",
    app_projects_project_type.value as "typeValue",
    app_projects_project.gallery_id as "gallery",
    concat('{project_page_path}/', app_projects_project_translation.slug) as "path",
    '{gettext_lazy('get more')}' as "moreText"
    from app_projects_project
    LEFT JOIN app_projects_project_translation ON app_projects_project_translation.master_id = app_projects_project.id
    LEFT JOIN app_projects_project_type  ON app_projects_project_type.id = app_projects_project.type_id
    WHERE app_projects_project_translation.language_code = '{lang}'
    {filter}
    {order}
    """

def build_search_products_query(lang, input, filter, project_page_path):
    search_phrase = re.sub('([^\w\s]|((?<=[\s])\d+))', '', sqlescape(input))
    words = [word.strip() for word in search_phrase.split(' ') if not word == ""]
    ts_query_phrase = ' <-> '.join(words)
    ts_query_words = ' | '.join(words)
    return f"""
    SELECT
    project.id as "id",
    ts_headline(project.name, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as name,
    project.slug as "slug",
    ts_headline(project.title, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as title,
    ts_headline(project.subtitle, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as subtitle,
    ts_headline(project.description, to_tsquery('{ts_query_phrase} | {ts_query_words}'), 'MinWords=200 MaxWords=500') as description,
    project.type as "type",
    project.type_value as "typeValue",
    project.gallery as "gallery",
    ts_headline(project.technologies, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as "technologies",
    project.path as "path",
    '{gettext_lazy('get more')}' as "moreText"
    FROM (SELECT
    app_projects_project.id AS "id",
    app_projects_project_translation.name AS "name",
    app_projects_project_translation.slug AS "slug",
    app_projects_project_translation.title AS "title",
    app_projects_project_translation.subtitle AS "subtitle",
    app_projects_project_translation.description_short AS "description",
    app_projects_project_translation.json_ld as "json_ld",
    app_projects_project_type.display AS "type",
    app_projects_project_type.value AS "type_value",
    app_projects_project.gallery_id AS "gallery",
    STRING_AGG(app_projects_technology.name, ',') AS "technologies",
    concat('{project_page_path}/', app_projects_project_translation.slug) as "path",
    ts_rank_cd(
      app_projects_project_translation.search_vector,
      to_tsquery('{ts_query_words}')
    ) + 2 *
    ts_rank_cd(
      app_projects_project_translation.search_vector,
      to_tsquery('{ts_query_phrase}')
    ) AS "rank"
    FROM app_projects_project
    LEFT JOIN app_projects_project_translation ON app_projects_project_translation.master_id = app_projects_project.id
    LEFT JOIN app_projects_project_type  ON app_projects_project_type.id = app_projects_project.type_id
    LEFT JOIN app_projects_project_technology ON app_projects_project_technology.project_id = app_projects_project.id
    LEFT JOIN app_projects_technology ON app_projects_technology.id = app_projects_project_technology.technology_id
    WHERE app_projects_project_translation.language_code = '{lang}'
    {filter}
    GROUP BY
    app_projects_project.id,
    app_projects_project_translation.name,
    app_projects_project_translation.slug,
    app_projects_project_translation.title,
    app_projects_project_translation.subtitle,
    app_projects_project_translation.description_short,
    app_projects_project_type.display,
    app_projects_project_type.value,
    app_projects_project_translation.search_vector
    ORDER BY rank DESC
    ) as project where project.rank > 0.00001
    """

def build_get_projects_technologies_query(projects_ids_list):
    ids = ",".join([str(id) for id in projects_ids_list])
    return f"""
    SELECT
    app_projects_project_technology.project_id as "project_id",
    app_projects_technology.name as "name",
    app_projects_technology.link as "link",
    app_projects_technology.color as "color"
    FROM app_projects_project_technology
    LEFT JOIN app_projects_technology ON app_projects_project_technology.technology_id = app_projects_technology.id
    WHERE app_projects_project_technology.project_id IN ({ids})
    ORDER BY sort_value ASC, app_projects_technology.show_on_index, app_projects_technology.show_on_index_all ASC
    """

def group_by(item_list, prop, force_list = False):
    _dict = {}
    for item in item_list:
        key = item[prop]
        current = _dict.get(key, None)
        if current:
            if type(current) == list:
                current.append(item)
                _dict[key] = current
            else:
                _list = [current, item]
                _dict[key] = _list
        else:
            _dict[key] = [item] if force_list else item
    return _dict

def get(request, params, doSerialization = False):
    lang = get_language()
    order_param = params.get('order', None)
    type_param = params.get('type', None)
    search_param = params.get('search', None)
    on_index_param = params.get('on_index', False)

    def order():
        if not order_param:
            order_conf = py_.find(ordering, {'default': True})
        else:
            order_conf = py_.find(ordering, {'value': order_param})
        if not order_conf: return ''
        return f"ORDER BY {order_conf.get('column')} {order_conf.get('type')}"

    def filter():
        if not type_param and not on_index_param: return ''
        where = ''
        if type_param:
            type_values = sqlescape(type_param).split(',')
            where += ' AND (' + ' OR '.join([f"app_projects_project_type.value='{value}'" for value in type_values]) + ')'
        if on_index_param:
            where += ' AND (app_projects_project.show_on_index = TRUE) '
        return where

    def get_projects(input):
        try:
            project_page_path = revers_page_path(page_name = 'Project').split('/')[0]
            if input:
                query = build_search_products_query(lang, input, filter(), project_page_path)
            else:
                query = build_get_projects_query(lang, filter(), order(), project_page_path)
            query_results = execute_queries([query])
            projects_list = query_results['resultEach'][0]['data']
            return group_by(projects_list, 'id')
        except:
            return {}

    def get_highlighted_technology_list(project):
        technologies = project.get('technologies', None)
        if not technologies: return []
        return [re.sub('\\<\/?b\\>', '', technology)
            for technology in technologies.split(',') if technology.startswith('<b>')]


    def get_projects_technologies(projects):
        projects_ids_list = list(projects.keys())

        query = build_get_projects_technologies_query(projects_ids_list)
        query_results = execute_queries([query])

        if not query_results['successAll']: return {}

        technology_list = query_results['resultEach'][0]['data']
        technologies = group_by(technology_list, 'project_id', force_list = True)

        for project_id, technology_list in technologies.items():
            highlightedTechnology = get_highlighted_technology_list(projects.get(project_id))
            for technology in technology_list:
                isHighlighted = technology['name'] in highlightedTechnology
                technology['isHighlighted'] =  isHighlighted
            technology_list.sort(key = lambda technology: not technology['isHighlighted'])

        return technologies


    def get_projects_galleries(projects):
        galleries_ids = [project.get('gallery') for project in projects.values()]
        images = ProjectGalleryImage.objects.filter(gallery__in = galleries_ids)
        galleries = {}
        for image in images:
            gallery = galleries.get(image.gallery_id, [])
            if doSerialization:
                gallery.append(image.toJson())
            else:
                gallery.append(image)
            galleries[image.gallery_id] = gallery
        return galleries



    try:
        projects = get_projects(search_param)

        projects_technologies = get_projects_technologies(projects)
        projects_galleries = get_projects_galleries(projects)

        def projects_combine(project):
            project['technologies'] = projects_technologies.get(project.get('id'))
            project['images'] = projects_galleries.get(project.get('gallery'))
            del project['id']
            del project['gallery']
            return project

        return list(map(projects_combine, projects.values()))
    except:
        return []
