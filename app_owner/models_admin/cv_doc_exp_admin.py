from django.contrib import admin
from django import forms
from app_owner.models import CVDocumentEducation
from parler.admin import TranslatableStackedInline, TranslatableModelForm, TranslatableAdmin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayTextareaWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from app_owner.models import (
    CVDocumentExperienceJob,
    CVDocumentExperience
)

class CVDocumentExperienceJobFrom(TranslatableModelForm):
    description =  forms.CharField(
        widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30})
    )
    class Meta:
        model = CVDocumentExperienceJob
        fields = ['company', 'address', 'position','from_date', 'to_date', 'description']

class CVDocumentExperienceJobInlineAdmin(TranslatableStackedInline, DynamicArrayMixin):
    extra = 0
    model = CVDocumentExperienceJob
    form = CVDocumentExperienceJobFrom

@admin.register(CVDocumentExperience)
class CVDocumentExperienceAdmin(TranslatableAdmin):
    def has_module_permission(self, request): return False
    inlines = [CVDocumentExperienceJobInlineAdmin]
    pass