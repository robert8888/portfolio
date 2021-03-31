from django.contrib import admin
from app_owner.models import CVDocumentEducation
from parler.admin import TranslatableStackedInline, TranslatableModelForm
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayTextareaWidget

from app_owner.models import (
    CVDocumentEducationSchool,
    CVDocumentEducation
)


class CVDocumentEducationSchoolInlineAdmin(TranslatableStackedInline):
    extra = 0
    base_form = TranslatableModelForm
    model = CVDocumentEducationSchool

@admin.register(CVDocumentEducation)
class CVDocumentEducationAdmin(admin.ModelAdmin, DynamicArrayMixin):
    def has_module_permission(self, request): return False
    inlines = [CVDocumentEducationSchoolInlineAdmin]
    pass