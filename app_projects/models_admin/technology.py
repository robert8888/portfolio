from django.contrib import admin
from django import forms
from django.forms.widgets import TextInput
from parler.admin import TranslatableModelForm, TranslatableAdmin
from .actions import (
    addTechnologyAutocomplete,
    deleteTechnologyAutocomplete,
    updateTechnologyAutocomplete
)

from app_projects.models import (
    Image,
    Technology,
    TechnologyType,
    TechnologyImage,
    TechnologyImageStd,
    TechnologyImageSprite
)
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedPolymorphicInlineSupportMixin,
    NestedStackedPolymorphicInline,
    NestedPolymorphicModelAdmin,
    NestedModelAdminMixin
)

@admin.register(TechnologyType)
class TechnologyTypeAdmin(TranslatableAdmin):
    def has_module_permission(self, request): return False
    base_form = TranslatableModelForm

@admin.register(Image)
class Image(admin.ModelAdmin):
    def has_module_permission(self, request): return False
    exclude = ['width', 'height']


class TechnologyImageInline(NestedStackedPolymorphicInline):
    class ContactImageStdInline(NestedStackedPolymorphicInline.Child):
        model = TechnologyImageStd

    class TechnologyImageSpriteInline(NestedStackedPolymorphicInline.Child):
        model = TechnologyImageSprite
        fieldsets = (
            (None, {'fields': ['image']}),
            (None, {
                'fields': ['top', 'left'],
                'classes': ['form__contact-image__fieldset']
            }),
            (None, {
                'fields': ['width', 'height'],
                'classes': ['form__contact-image__fieldset']
            })
        )

    model = TechnologyImage

    child_inlines = (
        ContactImageStdInline,
        TechnologyImageSpriteInline,
    )

class TechnologyAdminForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color', 'data-test': 'value'})
        }

@admin.register(Technology)
class TechnologyAdmin(NestedPolymorphicModelAdmin):
    form = TechnologyAdminForm
    inlines = [TechnologyImageInline]
    actions = [addTechnologyAutocomplete, deleteTechnologyAutocomplete, updateTechnologyAutocomplete]
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    pass

