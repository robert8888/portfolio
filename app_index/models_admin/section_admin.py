from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline
from app_index.models import Property, PropertyText, PropertyTextLong, PropertyTextRich
from parler.admin import TranslatableStackedInline, TranslatableModelForm, TranslatableInlineModelAdmin, TranslatableAdmin
import nested_admin

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

class PropertyInline(NestedStackedPolymorphicInline):

    class PropertyTextInline(TranslatableStackedInline, NestedStackedPolymorphicInline.Child ):
        base_form = TranslatableModelForm
        model = PropertyText

    class PropertyTextLongInline(TranslatableStackedInline, NestedStackedPolymorphicInline.Child):
        base_form = TranslatableModelForm
        model = PropertyTextLong

    class PropertyTextRichInline(TranslatableStackedInline, NestedStackedPolymorphicInline.Child):
        class PropertyTextRichFrom(TranslatableModelForm):
            value =  forms.CharField(
                widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30})
            )
            class Meta:
                model = PropertyTextRich
                fields = "__all__"
        model = PropertyTextRich
        form = PropertyTextRichFrom

    model = Property

    child_inlines = (
        PropertyTextInline,
        PropertyTextLongInline,
        PropertyTextRichInline,
    )


class ViewInline(NestedStackedInline):
    extra = 0
    model = View

class SectionAdmin(nested_admin.NestedPolymorphicModelAdmin):
    inlines = [ViewInline, PropertyInline]
    exclude = ['style']