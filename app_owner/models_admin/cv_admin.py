from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy
from app_owner.models import (
    CV,
)

@admin.register(CV)
class CV_Admin(admin.ModelAdmin):
    list_display = ('name', 'full_path')
    readonly_fields = ('full_path', 'slug')
    fields = ['full_path', 'reset_slug', 'name',  'template', 'color_profile', 'data']

    def get_queryset(self, request):
        qs = super(CV_Admin, self).get_queryset(request)
        self.request = request
        return qs

    def full_path(self, instance):
        url =  self.request.scheme + '://' + self.request.get_host() + instance.url
        return format_html(
            "<a href={} target='_blank'>{}</a>", url , url
        )

    full_path.short_description = gettext_lazy('Download link')

    pass