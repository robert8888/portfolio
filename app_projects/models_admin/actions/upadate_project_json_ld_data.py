from django.utils.translation import gettext, ugettext
from django.contrib import messages

def update_project_json_ld(modeladmin, request, queryset):
    try:
        for Project in queryset:
            Project.update_json_ld()

        modeladmin.message_user(
            request,
            ugettext('Updated json ld structure data of %d projects') % len(queryset),
            messages.SUCCESS
        )
    except:
        modeladmin.message_user(
            request,
            ugettext('Updated json ld structure data of %d projects - FAIL') % len(queryset),
            messages.ERROR
        )


update_project_json_ld.short_description = gettext("Update SEO structure data")