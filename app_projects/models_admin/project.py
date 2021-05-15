from django.contrib import admin
from django import forms
from app_projects.models import Project, ProjectLink, ProjectType
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from fieldsets_with_inlines import FieldsetsInlineMixin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from parler.admin import TranslatableModelForm, TranslatableAdmin
from adminsortable2.admin import SortableAdminMixin
from .actions import (
    addProjectAutocomplete,
    deleteProjectAutocomplete,
    updateProjectAutocomplete,
    update_project_json_ld,
)

class ProjectForm(TranslatableModelForm):
    description_short = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 15}))
    description_full = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30}))

@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request): return False


class ProjectLinksInline(DynamicArrayMixin, admin.StackedInline):
    extra = 0
    model = ProjectLink

@admin.register(Project)
class ProjectAdmin(DynamicArrayMixin,SortableAdminMixin, TranslatableAdmin):
    list_display = ('name', 'type', 'repo_link', )
    form = ProjectForm
    filter_horizontal = ['related']
    inlines = [ProjectLinksInline]
    fieldsets = (
        (None, {'fields': ['name']}),
        ('Meta', {
            'fields': ['meta_title', 'meta_description', 'application_cat', 'operating_system']
        }),
        ('Project', {
            'fields': ['title', 'subtitle', 'type', 'release_date',
             'update_date', 'gallery', 'autocomplete_hint', 'show_on_index']
        }),
        (None, {
            'fields': ['technology', 'related']
        }),
        (None, {
            'fields': [ 'description_short', 'description_full']
        })
    )
    actions = [
        addProjectAutocomplete,
        deleteProjectAutocomplete,
        updateProjectAutocomplete,
        update_project_json_ld
    ]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    pass

