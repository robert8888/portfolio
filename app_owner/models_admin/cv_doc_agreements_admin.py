from django.contrib import admin
from django import forms
from parler.admin import TranslatableAdmin

from app_owner.models import (
    CVDocumentAgreements
)

@admin.register(CVDocumentAgreements)
class CVDocumentSummaryAdmin(TranslatableAdmin):
    def has_module_permission(self, request): return False
    pass