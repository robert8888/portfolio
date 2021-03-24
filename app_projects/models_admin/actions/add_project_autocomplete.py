from django.utils.translation import gettext, ugettext
from .execute_action import executeAction
from .delete_project_autocomplete import buildQueryDelete

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
        terms.term,
        terms.language_code,
        'project' as "type",
        terms.project_id as "source_id",
        to_tsvector(terms.term) as search_vector
        FROM (
          SELECT
          app_projects_project_translation.title as "term",
          app_projects_project_translation.language_code as "language_code",
          app_projects_project_translation.master_id as "project_id"
          FROM app_projects_project_translation
          WHERE app_projects_project_translation.master_id IN ({ids})
          UNION
          SELECT app_projects_project_translation.subtitle as "term",
          app_projects_project_translation.language_code as "language_code",
          app_projects_project_translation.master_id as "project_id"
          FROM app_projects_project_translation
          WHERE app_projects_project_translation.master_id IN ({ids})
          UNION
          SELECT
          unnest(app_projects_project_translation.autocomplete_hint) as "term",
          app_projects_project_translation.language_code as "language_code",
          app_projects_project_translation.master_id as "project_id"
          FROM app_projects_project_translation
          WHERE app_projects_project_translation.master_id IN ({ids})
        ) as terms
    """

def addProjectAutocomplete(modeladmin, request, queryset):
    ids = ",".join([str(item.get('id')) for item in queryset.values('id')])

    query_delete = buildQueryDelete(ids)

    query_insert = buildQueryInsert(ids)

    msg = {
        'success': ugettext('Add to autocomplete dictionary. Removed %d term and added %d terms'),
        'fail': gettext('Adding to autocomplete dictionary fail')
    }

    executeAction(
        modeladmin,
        request,
        [query_delete, query_insert],
        msg= msg
    )

addProjectAutocomplete.short_description = gettext("Add to autocomplete")

