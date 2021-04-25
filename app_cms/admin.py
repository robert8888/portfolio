from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Page, Section, Menu
from .models_admin import PageAdmin, SectionAdmin, MenuAdmin


admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Menu, MenuAdmin)