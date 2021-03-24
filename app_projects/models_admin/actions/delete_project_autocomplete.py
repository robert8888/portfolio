from django.utils.translation import gettext, ugettext
from .execute_action import executeAction

def buildQueryDelete(ids):
    which = '' if len(ids) == 0 else  f"AND source_id IN ({ids})"
    query_delete = f"""
        DELETE FROM app_projects_project_search_auto
        WHERE type='project' {which}
    """
    print('query delete', query_delete)
    return query_delete

def deleteProjectAutocomplete(modeladmin, request, queryset):
    ids = ",".join([str(item.get('id')) for item in queryset.values('id')])

    query_delete = buildQueryDelete(ids)

    msg = {
        'success': ugettext('Delete %d terms from autocomplete dictionary'),
        'fail': gettext('Removing terms from dictionary fail')
    }

    executeAction(
        modeladmin,
        request,
        [query_delete],
        msg=msg
    )

deleteProjectAutocomplete.short_description = gettext("Delete from autocomplete")