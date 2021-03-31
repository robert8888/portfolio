from django.contrib import admin
from django import forms
from parler.admin import TranslatableModelForm, TranslatableAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from app_owner.models import (
    CVDocumentSummary,
)

class CVDocumentSummaryAdminFrom(TranslatableModelForm):
    summary_content = forms.CharField(
        widget=CKEditorUploadingWidget(attrs={'cols': 60, 'rows': 30})
    )

@admin.register(CVDocumentSummary)
class CVDocumentSummaryAdmin(TranslatableAdmin):
    def has_module_permission(self, request): return False
    form = CVDocumentSummaryAdminFrom
    fields = ['name', 'summary_title', 'summary_content']
    pass