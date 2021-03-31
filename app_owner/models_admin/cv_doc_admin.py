from django.contrib import admin

from app_owner.models import CVDocument

@admin.register(CVDocument)
class CV_Admin(admin.ModelAdmin):
    pass