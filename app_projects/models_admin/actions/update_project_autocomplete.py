from django.utils.translation import gettext, ugettext
from .execute_action import executeAction

from .add_project_autocomplete import buildQueryInsert
from .delete_project_autocomplete import buildQueryDelete

def updateProjectAutocomplete(modeladmin, request, queryset):
    ids = ",".join([str(item.get('id')) for item in queryset.values('id')])

    query_delete = buildQueryDelete(ids)

    query_insert = buildQueryInsert(ids)

    msg = {
        'success': ugettext('Updated terms in autocomplete dictionary. Rebuild %(0) term and added %(1) terms'),
        'fail': gettext('Updating autocomplete dictionary fail')
    }

    executeAction(
        modeladmin,
        request,
        [query_delete, query_insert],
        msg=msg
    )

updateProjectAutocomplete.short_description = gettext("Update autocomplete")