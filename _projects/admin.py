from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models_admin import OwnerAdmin, ProjectAdmin, PortalAdmin, TechnologyAdmin
from .models import Owner, Project, Portal, Technology


admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.

# class TechnologyAdmin(admin.ModelAdmin):
#     def has_module_permission(self, request):
#         return False


admin.site.register(Owner, OwnerAdmin)
#admin.site.register(Portal, PortalAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology, TechnologyAdmin)