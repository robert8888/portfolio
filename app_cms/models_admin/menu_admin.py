from django.contrib import admin
from ..models import Menu, MenuItem

from parler.admin import (
    TranslatableStackedInline,
    TranslatableModelForm,
    TranslatableAdmin
)

from nested_admin import (
    NestedStackedInline,
)

class MenuItemInline(TranslatableStackedInline, NestedStackedInline):
    extra = 0
    base_form = TranslatableModelForm
    model = MenuItem
    sortable_field_name = "order"

class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemInline,)
    exclude = ['style']