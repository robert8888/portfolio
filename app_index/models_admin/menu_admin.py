from django.contrib import admin
from app_index.models import Menu, MenuItem
from parler.admin import TranslatableStackedInline, TranslatableModelForm, TranslatableInlineModelAdmin, TranslatableAdmin

class MenuItemInline(TranslatableStackedInline):
    extra = 0
    base_form = TranslatableModelForm
    model = MenuItem

class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemInline,)
    exclude = ['style']