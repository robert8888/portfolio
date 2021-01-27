from django.contrib import admin
from projects.models import ProjectImage, Project

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    readonly_fields = ['width', 'height']

class TechnologiesInline(admin.TabularInline):
    model = Project.technologies.through

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_technologies', 'repository', 'demo')
    inlines = [ProjectImageInline]
    filter_horizontal = ['technologies']