from django.contrib import admin
from ..models import Menu, MenuItem
from parler.admin import (
    TranslatableStackedInline,
    TranslatableModelForm,
    TranslatableAdmin
)

class MenuItemInline(TranslatableStackedInline):
    extra = 0
    base_form = TranslatableModelForm
    model = MenuItem

class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemInline,)
    exclude = ['style']