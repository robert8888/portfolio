from django.contrib import admin

from app_owner.models import CVColorProfile

@admin.register(CVColorProfile)
class CV_Admin(admin.ModelAdmin):
    def has_module_permission(self, request): return False