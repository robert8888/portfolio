from django.utils.translation import gettext, ugettext
from .execute_action import executeAction
from .delete_technology_autocomplete import buildQueryDelete
from .add_technology_autocomplete import buildQueryInsert

def updateTechnologyAutocomplete(modeladmin, request, queryset):
    ids = ",".join([str(item.get('id')) for item in queryset.values('id')])

    query_delete = buildQueryDelete(ids)

    query_insert = buildQueryInsert(ids)

    msg = {
        'success': ugettext('Add to autocomplete dictionary. Removed %d term and added %d terms'),
        'fail': gettext('Adding to autocomplete dictionary fail')
    }

    executeAction(modeladmin, request, [query_delete, query_insert], msg=msg)

updateTechnologyAutocomplete.short_description = gettext("Update autocomplete")