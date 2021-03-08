from django.contrib import admin
from projects.models import ProjectImage, Project
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    readonly_fields = ['width', 'height']

class TechnologiesInline(admin.TabularInline):
    model = Project.technologies.through

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

class ProjectAdminForm(forms.ModelForm):
    short_description = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 15}))
    full_description = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30}))
    on_page = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, widget=forms.Select(), initial = '')

    class Meta:
        model = Project
        fields = "__all__"

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_technologies', 'repository', 'demo')
    inlines = [ProjectImageInline]
    filter_horizontal = ['technologies', 'related']
    form = ProjectAdminForm