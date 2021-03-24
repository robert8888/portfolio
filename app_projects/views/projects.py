from django.utils.translation import get_language
from django.db import connection
from django.utils.translation import gettext_lazy
from app_projects.models import ProjectGalleryImage
from sqlescapy import sqlescape
import pydash as py_
import re

ordering = [{
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

def get(request, params, doSerialization = False):
    lang = get_language()
    order_param = params.get('order', None)
    type_param = params.get('type', None)
    search_param = params.get('search', None)

    def order():
        if not order_param: return ''
        order_conf = py_.find(ordering, {'value': order_param})
        if not order_conf: return ''
        return f"ORDER BY {order_conf.get('column')} {order_conf.get('type')}"

    def filter():
        if not type_param: return ''
        type_values = sqlescape(type_param.split(','))
        return ' AND (' + ' OR '.join([f"app_projects_project_type.value='{value}'" for value in type_values]) + ')'

    def getProjects():
        query = f"""
        SELECT
        app_projects_project.id,
        app_projects_project_translation.name,
        app_projects_project_translation.slug,
        app_projects_project_translation.title,
        app_projects_project_translation.subtitle,
        app_projects_project_translation.description_short,
        app_projects_project_type.display,
        app_projects_project_type.value AS type_value,
        app_projects_project.gallery_id
        from app_projects_project
        LEFT JOIN app_projects_project_translation ON app_projects_project_translation.master_id = app_projects_project.id
        LEFT JOIN app_projects_project_type  ON app_projects_project_type.id = app_projects_project.type_id
        WHERE app_projects_project_translation.language_code = '{lang}'
        {filter()}
        {order()}
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
            projects = {}
            for row in rows:
                projects[row[0]] = {
                    'id': row[0],
                    'name': row[1],
                    'slug': row[2],
                    'title': row[3],
                    'subtitle': row[4],
                    'description': row[5],
                    'type': row[6],
                    'typeValue': row[7],
                    'gallery': row[8]
                }
            return projects
        except:
            return {}

    def searchProjects(input):
        search_phrase = re.sub('([^\w\s]|((?<=[\s])\d+))', '', sqlescape(input))
        words = [word.strip() for word in search_phrase.split(' ') if not word == ""]
        ts_query_phrase = ' <-> '.join(words)
        ts_query_words = ' | '.join(words)
        query = f"""
        SELECT
        project.id,
        ts_headline(project.name, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as name,
        project.slug,
        ts_headline(project.title, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as title,
        ts_headline(project.subtitle, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as subtitle,
        ts_headline(project.description, to_tsquery('{ts_query_phrase} | {ts_query_words}'), 'MinWords=200 MaxWords=500') as descriptions,
        project.type,
        project.type_value,
        project.gallery,
        ts_headline(project.technologies, to_tsquery('{ts_query_phrase} | {ts_query_words}')) as technologies
        FROM (SELECT
        app_projects_project.id AS id,
        app_projects_project_translation.name AS name,
        app_projects_project_translation.slug AS slug,
        app_projects_project_translation.title AS title,
        app_projects_project_translation.subtitle AS subtitle,
        app_projects_project_translation.description_short AS description,
        app_projects_project_type.display AS type,
        app_projects_project_type.value AS type_value,
        app_projects_project.gallery_id AS gallery,
        STRING_AGG(app_projects_technology.name, ',') AS technologies,
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
        {filter()}
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
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
            projects = {}
            for row in rows:
                projects[row[0]] = {
                    'id': row[0],
                    'name': row[1],
                    'slug': row[2],
                    'title': row[3],
                    'subtitle': row[4],
                    'description': row[5],
                    'type': row[6],
                    'typeValue': row[7],
                    'gallery': row[8],
                    'technologies': row[9]
                }
            return projects
        except:
            return {}


    def getHighlightedTechnologyList(project):
        technologies = project.get('technologies', None)
        if not technologies: return []
        return [re.sub('\\<\/?b\\>', '', technology)
            for technology in technologies.split(',') if technology.startswith('<b>')]


    def getProjectsTechnologies(projects):
        project_ids = list(projects.keys())
        if len(project_ids) == 0: return {}
        ids = ",".join([str(id) for id in project_ids])
        query = f"""
        SELECT
        app_projects_project_technology.project_id,
        app_projects_technology.name,
        app_projects_technology.link,
        app_projects_technology.color
        FROM app_projects_project_technology
        LEFT JOIN app_projects_technology ON app_projects_project_technology.technology_id = app_projects_technology.id
        WHERE app_projects_project_technology.project_id IN ({ids})
        ORDER BY app_projects_technology.show_on_index, app_projects_technology.show_on_index_all ASC
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
            projects_technologies = {}
            for row in rows:
                id = row[0]
                highlightedTechnology = getHighlightedTechnologyList(projects.get(id))
                isHighlighted = row[1] in highlightedTechnology
                tech_list = projects_technologies.get(id, [])
                current = {
                    'name': row[1],
                    'link': row[2],
                    'color': row[3],
                    'isHighlighted': isHighlighted
                }
                if isHighlighted:
                    tech_list = [current, *tech_list]
                else:
                    tech_list = [*tech_list, current]
                projects_technologies[row[0]] = tech_list
            return projects_technologies
        except:
            return {}

    def getProjectsGalleries(projects):
        galleries_ids = [project.get('gallery') for project in projects.values()]
        images = ProjectGalleryImage.objects.filter(gallery__in = galleries_ids)
        galleries = {}
        for image in images:
            print(type(image))
            gallery = galleries.get(image.gallery_id, [])
            if doSerialization:
                gallery.append(image.toJson())
            else:
                gallery.append(image)
            galleries[image.gallery_id] = gallery
        return galleries

    projects = searchProjects(search_param) if search_param else getProjects()

    projects_technologies = getProjectsTechnologies(projects)
    projects_galleries = getProjectsGalleries(projects)

    def projectsCombine(project):
        project['technologies'] = projects_technologies.get(project.get('id'))
        project['images'] = projects_galleries.get(project.get('gallery'))
        del project['id']
        del project['gallery']
        return project

    return list(map(projectsCombine, projects.values()))