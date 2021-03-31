from django.contrib import admin
from app_owner.models import CVDocumentPhoto
from imagefield.widgets import PreviewAndPPOIMixin

@admin.register(CVDocumentPhoto)
class CVDocumentEducationAdmin(admin.ModelAdmin, PreviewAndPPOIMixin):
    def has_module_permission(self, request): return False
    fields = ['id_name', 'ppoi', 'source']
    pass