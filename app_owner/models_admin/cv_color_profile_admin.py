from django.contrib import admin

from app_owner.models import CVColorProfile

@admin.register(CVColorProfile)
class CV_Admin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['id_name']}),
        ('Base',{
            'fields': ['background', 'text', 'text_focus']}
        ),
        ('Primary',{
            'fields': ['primary', 'text_primary', 'text_primary_focus']
        }),
        ('Secondary', {
            'fields': ['secondary', 'text_secondary', 'text_secondary_focus']
        })
    )
    def has_module_permission(self, request): return False