from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy
from django.conf import settings
import re
from app_owner.models import (
    CV,
)


languages = [lang_pair[0] for lang_pair in settings.LANGUAGES]
pure_url = lambda url: re.sub('^\/(' + '|'.join(languages) + ')', '', url)
build_link_form_field = lambda url, display_url: format_html("<a href={} target='_blank'>{}</a>", url , display_url)

@admin.register(CV)
class CV_Admin(admin.ModelAdmin):
    list_display = ('name', 'data', 'template', 'color_profile', 'full_path_en', 'full_path_pl')

    def get_queryset(self, request):
        qs = super(CV_Admin, self).get_queryset(request)
        self.request = request
        return qs

    def getattr(self, *args, **kwargs):
        print(args, kwargs)
        super(CV_Admin, self).getattr(*args, **kwrags)

    def get_fields(self, request, obj=None):
        fields = ['full_path_' + lang for lang in languages]
        fields += ['reset_slug', 'name',  'template', 'color_profile', 'data']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['full_path_' + lang for lang in languages]
        fields += ['slug']
        return fields

    def build_url(self,  url):
        return self.request.scheme + '://' + self.request.get_host() + url

    def full_path_en(self, instance):
        if not 'en' in languages:
            return ''
        url = pure_url(instance.url)
        return build_link_form_field(self.build_url(url), url)

    full_path_en.short_description = gettext_lazy('Download link en')


    def full_path_pl(self, instance):
        if not 'pl' in languages:
            return ''

        url = '/pl' + pure_url(instance.url)
        return build_link_form_field(self.build_url(url), url)

    full_path_pl.short_description = gettext_lazy('Download link pl')
