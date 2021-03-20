from django.utils.translation import get_language
from django.db import connection
from datetime import datetime
from app_projects.models import ProjectGalleryImage

ordering = [{
    "column": "app_projects_project.name",
    "value": "data_asc",
    "text": "Date",
    "textType": "Z-A"
},{
    "column": "app_projects_project.name",
    "value": "date_dsc",
    "text": "Date",
    "textType": "Z-A"
},{
    "column": "app_projects_project.name",
    "value": "name_asc",
    "text": "Name",
    "textType": "A-Z"
},{
    "column": "app_projects_project.name",
    "value": "name_dsc",
    "text": "Name",
    "textType": "Z-A"
},{
    "column": "app_projects_project.name",
    "value": "type_asc",
    "text": "Type",
    "textType": "A-Z"
},{
    "column": "app_projects_project.name",
    "value": "type_dsc",
    "text": "Type",
    "textType": "Z-A"
}]


def process(request, config, context, *args):
    lang = get_language()
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
        app_projects_project.gallery_id
        from app_projects_project
        LEFT JOIN app_projects_project_translation ON app_projects_project_translation.master_id = app_projects_project.id
        LEFT JOIN app_projects_project_type  ON app_projects_project_type.id = app_projects_project.type_id
        WHERE app_projects_project_translation.language_code = 'en'
        """
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
                'description_short': row[5],
                'type': row[6],
                'gallery': row[7]
            }
        return projects

    def getProjectsTechnologies(project_ids):
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
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        projects_technologies = {}
        for row in rows:
            current = projects_technologies.get(row[0], [])
            current.append({
                'name': row[1],
                'link': row[2],
                'color': row[3]
            })
            projects_technologies[row[0]] = current
        return projects_technologies

    def getProjectsGalleries(projects):
        galleries_ids = [project.get('gallery') for project in projects.values()]
        images = ProjectGalleryImage.objects.filter(gallery__in = galleries_ids)
        galleries = {}
        for image in images:
            gallery = galleries.get(image.gallery_id, [])
            gallery.append(image)
            galleries[image.gallery_id] = gallery
        return galleries

#     print('---projects start', datetime.now())
    projects = getProjects()
    projects_technologies = getProjectsTechnologies(list(projects.keys()))
    projects_galleries = getProjectsGalleries(projects)
    def projectsCombine(project):
        project['technologies'] = projects_technologies.get(project.get('id'))
        project['images'] = projects_galleries.get(project.get('gallery'))
        return project

#     print('---projects end', datetime.now())
#     print(list(map(projectsCombine, projects.values())))
    return {
        **context,
        'projects': list(map(projectsCombine, projects.values()))
    }


