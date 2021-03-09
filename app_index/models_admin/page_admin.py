from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from app_index.models import (
    View,
    Section,
    Variable,
    VariableText,
    VariableTextLong,
    VariableTextRich
)
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedPolymorphicInlineSupportMixin,
    NestedStackedPolymorphicInline
)

class VariableInline(NestedStackedPolymorphicInline):
    class VariableTextInline(NestedStackedPolymorphicInline.Child):
        model = VariableText

    class VariableTextLongInline(NestedStackedPolymorphicInline.Child):
            model = VariableTextLong

    class VariableTextRichInline(NestedStackedPolymorphicInline.Child):
            class VariableTextRichFrom(forms.ModelForm):
                value =  forms.CharField(
                    widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30})
                )
                class Meta:
                    model = VariableTextRich
                    fields = "__all__"
            model = VariableTextRich
            form = VariableTextRichFrom

    model = Variable

    child_inlines = (
        VariableTextInline,
        VariableTextLongInline,
        VariableTextRichInline,
    )

class ViewInline(NestedStackedInline):
    extra = 0
    model = View

class SectionInline(NestedStackedInline):
    extra = 0
    model = Section
    sortable_field_name = "position"
    inlines = [ViewInline, VariableInline]

class PageAdmin(NestedPolymorphicInlineSupportMixin, NestedModelAdmin):
    list_display = ('name', 'address', 'template')
    inlines = [SectionInline]