from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from polymorphic.admin import PolymorphicInlineAdminForm
from parler.admin import TranslatableStackedInline, TranslatableModelForm, TranslatableInlineModelAdmin, TranslatableAdmin
from fieldsets_with_inlines import FieldsetsInlineMixin

from parler.admin import (
    TranslatableStackedInline,
    TranslatableModelForm,
)

from ..models import (
    Page,
    Path,
    View,
    Section,
    Property,
    PropertyText,
    PropertyTextLong,
    PropertyTextRich
)
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedPolymorphicInlineSupportMixin,
    NestedStackedPolymorphicInline
)

class PathsInline(TranslatableStackedInline, NestedStackedInline):
    extra = 0
    model = Path
    base_form = TranslatableModelForm
    exclude = ['pattern']
    classes = ['page__path',]

class SectionInline(NestedStackedInline):
    extra = 0
    model = Page.section.through
    sortable_field_name = "order"

class PageAdmin(FieldsetsInlineMixin, NestedModelAdmin):
    filter_horizontal = ['menu']
    fieldsets_with_inlines = [
         (None, { 'fields': ['name', 'template']}),
         PathsInline,
         (None, { 'fields': ['menu']}),
         SectionInline,

    ]