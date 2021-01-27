from django.contrib import admin

class PortalAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')