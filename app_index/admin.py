from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Page
from .models_admin import PageAdmin

from .models import Section
from .models_admin import SectionAdmin

admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)