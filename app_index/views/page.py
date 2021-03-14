from django.http import HttpResponse
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import render
from app_index.models import Page, PageSections, Path, View as ViewModel
from portfolio.utils.getAppsViewsList import getAppsViewsList
from sqlescapy import sqlescape
from django.http import HttpResponse
import importlib
import re

class PageView(View):
    greeting = "Good Day"

    def get(self, request, path):
        context = {
           'gCaptchaPublicKey': '6LfPq2QaAAAAAGpz3x-4KiBjNF3zffwFOVhlXHjD',
           'csrfToken': get_token(request)
        }

        try:
            print("page view", path)
            if re.match('.*\.\w{,5}$', path): #file
                return HttpResponse(status=404)

            paths = Path.objects.extra(where = ['%s ~ pattern'], params=[sqlescape(path)])

            if not len(paths):
                raise LookupError('not found')

            page = paths[0].page
            params = self.getGroups(paths[0].pattern, path)

#             page = Page.objects.get(id=1)
            sections = self.getPageSections(page)
            views = self.importViews(sections)
            views_data = self.processViews(request, views, params)

            context = {
                **context,
                **views_data,
                'sections': sections['view_data'],
                'menus': self.getMenus(page)
            }

            return  render(request, page.template, context = context)

        except (Page.DoesNotExist, IndexError, LookupError):
            return  render(request, 'page_404.html', context = {})

    def getGroups(self, regex, str):
        match = re.match(regex, str)
        if match and len(match.groups()):
            return match.groups()
        return []

    def importViews(self, sections):
        views = ViewModel.objects.filter(section__id__in = sections['section_ids'])
        return [self.importModule(view.module_name) for view in views]

    def importModule(self, module_name):
        module_name = re.sub('\.py', '', module_name)
        return importlib.import_module(module_name)

    def processViews(self, request, views, params):
        data = {}
        for view in views:
            data = view.process(request, data, params)
        return data

    def getPageSections(self, page):
        sections = [
            relation.section
            for relation in
                PageSections.objects.filter(page = page.id).order_by('order')
        ]
        sections_view_data = []
        for section in sections:
            props = {}
            for prop in section.properties():
                props[prop.name] = prop.value
            section_data = {
                'template': section.template,
                'style': section.style,
                'props': props
            }
            sections_view_data.append(section_data)

        return {
            'view_data': sections_view_data,
            'section_ids': [section.id for section in sections]
        }

    def getMenus(self, page):
        def transformMenu(menu):
            return {
                'name': menu.name,
                'template': menu.template,
                'style': menu.style,
                'items': [{
                    'url': item.url,
                    'text': item.text.get(language_code = item.get_current_language()).value
                } for item in menu.items()]
            }
        menus = list(map(transformMenu, page.menu.all()))
        return menus