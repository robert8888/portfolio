from django.utils.translation import gettext, ugettext
from django.contrib import messages
from django.db import connection
from .execute_action import executeAction
from .delete_technology_autocomplete import buildQueryDelete

def buildQueryInsert(ids):
    return f"""
    INSERT INTO app_projects_project_search_auto (
        term,
        language_code,
        type,
        source_id,
        search_vector
    )
    SELECT
        app_projects_technology.name as "term",
        '' as language_code,
        'technology' as "type",
        app_projects_technology.id as "source_id",
        to_tsvector(app_projects_technology.name) as search_vector
        FROM app_projects_technology
        WHERE app_projects_technology.id IN ({ids})
    """

def addTechnologyAutocomplete(modeladmin, request, queryset):
    ids = ",".join([str(item.get('id')) for item in queryset.values('id')])

    query_delete = buildQueryDelete(ids)

    query_insert = buildQueryInsert(ids)

    msg = {
        'success': ugettext('Add to autocomplete dictionary. Removed %d term and added %(0) terms'),
        'fail': gettext('Adding to autocomplete dictionary fail')
    }

    executeAction(modeladmin, request, [query_delete, query_insert], msg=msg)

addTechnologyAutocomplete.short_description = gettext("Add to autocomplete")