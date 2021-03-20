from django.contrib import admin
from django import forms
from app_projects.models import Project, ProjectLink, ProjectType
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from fieldsets_with_inlines import FieldsetsInlineMixin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from parler.admin import TranslatableModelForm, TranslatableAdmin

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
class ProjectAdmin(TranslatableAdmin):
    form = ProjectForm
    filter_horizontal = ['technology', 'related']
    inlines = [ProjectLinksInline]
    fieldsets = (
        (None, {
            'fields': ['name', 'title', 'subtitle', 'type', 'release_date', 'update_date', 'gallery']
        }),
        (None, {
            'fields': ['technology', 'related']
        }),
        (None, {
            'fields': [ 'description_short', 'description_full']
        })
    )
    pass
