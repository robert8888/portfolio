from django.contrib import admin
from parler.admin import TranslatableAdmin

from app_owner.models import (
    CVDocumentPersonal
)

@admin.register(CVDocumentPersonal)
class CVDocumentSummaryAdmin(TranslatableAdmin):
    def has_module_permission(self, request): return False
    pass