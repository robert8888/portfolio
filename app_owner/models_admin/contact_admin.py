from django.contrib import admin
from django import forms

from app_owner.models import (
    Contact,
    ContactPortal,
    ContactNumber,
    ContactImage,
    ContactImageStandalone,
    ContactImageSprite,
    Image,
)

from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedPolymorphicInlineSupportMixin,
    NestedStackedPolymorphicInline,
    NestedModelAdminMixin
)

from polymorphic.admin import (
    PolymorphicInlineSupportMixin,
    StackedPolymorphicInline,
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin
)



@admin.register(Image)
class Image(admin.ModelAdmin):
    def has_module_permission(self, request): return False
    extra = 0
    model = Image
    exclude = ['width', 'height']



class ContactImageInline(NestedStackedPolymorphicInline):
    class ContactImageStandalone(NestedStackedPolymorphicInline.Child):
        model = ContactImageStandalone

    class ContactImageSprite(NestedStackedPolymorphicInline.Child):
        model = ContactImageSprite
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
    model = ContactImage

    child_inlines = (
        ContactImageStandalone,
        ContactImageSprite,
    )

@admin.register(ContactPortal)
class contactPortalAdmin(NestedPolymorphicInlineSupportMixin, NestedModelAdminMixin, PolymorphicChildModelAdmin):
    def has_module_permission(self, request): return False
    base_model = ContactPortal
    inlines = [ContactImageInline]

@admin.register(ContactNumber)
class contactNumberAdmin(NestedPolymorphicInlineSupportMixin, NestedModelAdminMixin, PolymorphicChildModelAdmin):
    def has_module_permission(self, request): return False
    base_model = ContactNumber
    inlines = [ContactImageInline]

@admin.register(Contact)
class contactAdmin(PolymorphicParentModelAdmin):
    polymorphic_list = True
    list_display = ['name', 'order', 'is_number_text']
    base_model = Contact
    child_models = (ContactPortal, ContactNumber)