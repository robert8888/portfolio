from django.contrib import admin
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline
from app_index.models import Variable, VariableText, VariableTextLong, VariableTextRich

class VariableInline(StackedPolymorphicInline):
    class VariableTextInline(StackedPolymorphicInline.Child):
        model = VariableText

    class VariableTextLongInline(StackedPolymorphicInline.Child):
            model = VariableTextLong

    class VariableTextRichInline(StackedPolymorphicInline.Child):
            model = VariableTextRich

    model = Variable

    child_inlines = (
        VariableTextInline,
        VariableTextLongInline,
        VariableTextRichInline,
    )

class SectionAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = (VariableInline,)