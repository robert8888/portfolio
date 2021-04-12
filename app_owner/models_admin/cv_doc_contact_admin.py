from django.contrib import admin
from django import forms
from parler.admin import TranslatableModelForm, TranslatableAdmin
from nested_admin import NestedModelAdmin, NestedStackedInline, SortableHiddenMixin, NestedModelAdminMixin


from app_owner.models import (
    CVDocumentContact,
    CVDocumentContactContacts
)

class CVDocumentContactContactsAdmin(SortableHiddenMixin, NestedStackedInline):
    extra = 0
    model = CVDocumentContactContacts
    sortable_field_name = 'order'

@admin.register(CVDocumentContact)
class CVDocumentSummaryAdmin(NestedModelAdminMixin, TranslatableAdmin):
    def has_module_permission(self, request): return False
    inlines = [CVDocumentContactContactsAdmin]
    pass