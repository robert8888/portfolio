from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from polymorphic.admin import PolymorphicInlineAdminForm
from parler.admin import TranslatableStackedInline, TranslatableModelForm, TranslatableInlineModelAdmin, TranslatableAdmin

from app_index.models import (
    Page,
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



# class PropertyInline(NestedStackedPolymorphicInline):
#
#     class PropertyTextInline(TranslatableStackedInline, NestedStackedPolymorphicInline.Child ):
#         base_form = TranslatableModelForm
#         model = PropertyText
#
#     class PropertyTextLongInline(NestedStackedPolymorphicInline.Child):
#         model = PropertyTextLong
#
#     class PropertyTextRichInline(NestedStackedPolymorphicInline.Child):
#             class PropertyTextRichFrom(forms.ModelForm):
#                 value =  forms.CharField(
#                     widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30})
#                 )
#                 class Meta:
#                     model = PropertyTextRich
#                     fields = "__all__"
#             model = PropertyTextRich
#             form = PropertyTextRichFrom
#
#     model = Property
#
#     child_inlines = (
#         PropertyTextInline,
#         PropertyTextLongInline,
#         PropertyTextRichInline,
#     )
#
#
# class ViewInline(NestedStackedInline):
#     extra = 0
#     model = View

class SectionInline(NestedStackedInline):
    extra = 0
    model = Page.section.through
    sortable_field_name = "order"
#     inlines = [ViewInline, PropertyInline]

class PageAdmin(NestedModelAdmin):
    list_display = ('name', 'address', 'template')
    inlines = [SectionInline]
    filter_horizontal = ['menu']