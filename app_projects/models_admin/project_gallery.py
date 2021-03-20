from django.contrib import admin
from django import forms
from app_projects.models import ProjectGallery
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
)
from app_projects.models import (
    ProjectGallery,
    ProjectGalleryImage
)
from imagefield.widgets import PreviewAndPPOIMixin

class ProjectGalleryImageForm(forms.ModelForm):
    class Meta:
        widgets = {
            'order': forms.HiddenInput()
        }

class ProjectGalleryImageInlineAdmin(PreviewAndPPOIMixin, NestedStackedInline):
    extra = 0
    sortable_field_name = 'order'
    fields = ['ppoi', 'image', 'order']
    model = ProjectGalleryImage
    form = ProjectGalleryImageForm

@admin.register(ProjectGallery)
class ProjectGalleryAdmin(NestedModelAdmin):
    model = ProjectGallery
    inlines = [ProjectGalleryImageInlineAdmin]
    pass