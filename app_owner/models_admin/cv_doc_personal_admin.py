from django.contrib import admin
from django import forms
from parler.admin import TranslatableModelForm, TranslatableAdmin
from nested_admin import NestedModelAdmin, NestedStackedInline, SortableHiddenMixin


from app_owner.models import (
    CVDocumentPersonal,
    CVDocumentPersonalContacts
)

class CVDocumentPersonalContactsAdmin(SortableHiddenMixin, NestedStackedInline):
    extra = 0
    model = CVDocumentPersonalContacts
    sortable_field_name = 'order'

@admin.register(CVDocumentPersonal)
class CVDocumentSummaryAdmin(NestedModelAdmin):
    def has_module_permission(self, request): return False
    inlines = [CVDocumentPersonalContactsAdmin]
    pass