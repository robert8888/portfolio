from django.contrib import admin
from django import forms
from app_owner.models import CVDocumentEducation
from parler.admin import TranslatableStackedInline, TranslatableModelForm
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayTextareaWidget

from app_owner.models import (
    CVDocumentExperienceJob,
    CVDocumentExperience
)

class CVDocumentExperienceJobFrom(TranslatableModelForm):
    class Meta:
        model = CVDocumentExperienceJob
        fields = '__all__'
        widgets = {
            'description': DynamicArrayTextareaWidget(attrs={'cols': 50, 'rows': 2})
        }

class CVDocumentExperienceJobInlineAdmin(TranslatableStackedInline, DynamicArrayMixin):
    extra = 0
    model = CVDocumentExperienceJob
    form = CVDocumentExperienceJobFrom

@admin.register(CVDocumentExperience)
class CVDocumentExperienceAdmin(admin.ModelAdmin):
    def has_module_permission(self, request): return False
    inlines = [CVDocumentExperienceJobInlineAdmin]
    pass