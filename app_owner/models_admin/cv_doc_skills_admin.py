from django.contrib import admin
from app_owner.models import CVDocumentEducation

from parler.admin import (
    TranslatableStackedInline,
    TranslatableModelForm,
    TranslatableAdmin
)

from nested_admin import (
    NestedPolymorphicModelAdmin,
    NestedStackedPolymorphicInline
)

from app_owner.models import (
    CVDocumentSkills,
    CVDocumentSkill,
    CVDocumentSkillLanguage,
    CVDocumentSkillOther
)

class CVDocumentSkillInline(NestedStackedPolymorphicInline):
    class CVDocumentSkillLanguageInline(TranslatableStackedInline,  NestedStackedPolymorphicInline.Child ):
        base_from = TranslatableModelForm
        model = CVDocumentSkillLanguage

    class CVDocumentSkillOtherInline(TranslatableStackedInline,  NestedStackedPolymorphicInline.Child ):
        base_from = TranslatableModelForm
        model = CVDocumentSkillOther

    model = CVDocumentSkill

    child_inlines = (
        CVDocumentSkillLanguageInline,
        CVDocumentSkillOtherInline
    )


@admin.register(CVDocumentSkills)
class CVDocumentEducationAdmin(NestedPolymorphicModelAdmin,TranslatableAdmin):
    def has_module_permission(self, request): return False
    inlines = [CVDocumentSkillInline]
    fields = ['id_name', 'section_title', 'technologies']
    pass