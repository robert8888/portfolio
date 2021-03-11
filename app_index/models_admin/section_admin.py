from django.contrib import admin
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline
from app_index.models import Property, PropertyText, PropertyTextLong, PropertyTextRich
from parler.admin import TranslatableStackedInline, TranslatableModelForm, TranslatableInlineModelAdmin

class PropertyInline(TranslatableStackedInline, StackedPolymorphicInline):
    base_form = TranslatableModelForm

    class PropertyTextInline(TranslatableStackedInline, StackedPolymorphicInline.Child):
        base_form = TranslatableModelForm
        base_model = PropertyText
        model = PropertyText

    class PropertyTextLongInline(StackedPolymorphicInline.Child):
            model = PropertyTextLong

    class PropertyTextRichInline(StackedPolymorphicInline.Child):
            model = PropertyTextRich

    model = Property

    child_inlines = (
        PropertyTextInline,
        PropertyTextLongInline,
        PropertyTextRichInline,
    )

class SectionAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = (PropertyInline,)