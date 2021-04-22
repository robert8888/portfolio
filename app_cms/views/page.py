from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import render
from app_cms.models import Page, PageSections, Path, View as ViewModel, Property
from portfolio.utils.execute_db_queries import execute_query
from django.utils.translation import get_language
from portfolio.utils.getAppsViewsList import getAppsViewsList
from htmlmin.decorators import minified_response
from django.conf import settings
from sqlescapy import sqlescape
from django.http import HttpResponse
from datetime import datetime
from django.db import connection
import pydash as py_
import importlib
import re
import os



def buildSelectPathQuery(path):
    return f"""
    SELECT
    app_cms_path.page_id as "page_id",
    app_cms_path_translation.pattern as "pattern",
    app_cms_path_translation.language_code as "lang"
    FROM app_cms_path
    LEFT JOIN app_cms_path_translation ON app_cms_path.id = app_cms_path_translation.master_id
    WHERE ( '{path}' ~ app_cms_path_translation.pattern)
    """

def buildSelectPageQuery(page_id):
    return f"""
    SELECT
    name,
    template
    FROM app_cms_page
    WHERE id = {page_id}
    """

def buildSelectPageMenusQuery(page_id, lang):
    return f"""
    SELECT
    "app_cms_menu"."id" as "id",
    "app_cms_menu"."name" as "name",
    "app_cms_menu"."template" as "template",
    "app_cms_menu"."style" as "style",
    "app_cms_menuitem_translation"."text" as "item_text",
    "app_cms_menuitem_translation"."url"  as "item_url"
    FROM "app_cms_page_menu"
    LEFT JOIN "app_cms_menu" ON "app_cms_menu"."id" = "app_cms_page_menu"."menu_id"
    LEFT JOIN "app_cms_menuitem" ON "app_cms_menuitem"."menu_id" = "app_cms_menu"."id"
    LEFT JOIN "app_cms_menuitem_translation" ON "app_cms_menuitem_translation"."master_id" = "app_cms_menuitem"."id"
    WHERE "app_cms_page_menu"."page_id" = {page_id}
    AND "app_cms_menuitem_translation"."language_code" = '{lang}'
    """

def buildSelectSectionQuery(page_id):
    return f"""
    SELECT
    "app_cms_section"."id" as "id",
    "app_cms_section"."name" as "name",
    "app_cms_section"."template" as "template",
    "app_cms_section"."style" as "style"
    FROM  "app_cms_pagesections"
    LEFT JOIN "app_cms_section" ON "app_cms_section"."id" = "app_cms_pagesections"."section_id"
      WHERE "app_cms_pagesections"."page_id" = {page_id}
      ORDER BY "app_cms_pagesections"."order"
    """

def buildSelectSectionPropQuery(section_ids, lang):
    return f'''
    SELECT
    "app_cms_property"."section_id" as "id",
    "app_cms_property"."name" as "name",
    COALESCE(
      "app_cms_propertytext_translation"."value",
      "app_cms_propertytextrich_translation"."value",
      "app_cms_propertytextlong_translation"."value",
      ''
    ) as "value"
    FROM  "app_cms_property"
    LEFT JOIN "app_cms_propertytextrich" ON "app_cms_propertytextrich"."property_ptr_id" =  "app_cms_property"."id"
    LEFT JOIN "app_cms_propertytextrich_translation" ON "app_cms_propertytextrich_translation"."master_id" = "app_cms_propertytextrich"."property_ptr_id"
    LEFT JOIN "app_cms_propertytextlong" ON "app_cms_propertytextlong"."property_ptr_id" =  "app_cms_property"."id"
    LEFT JOIN "app_cms_propertytextlong_translation" ON "app_cms_propertytextlong_translation"."master_id" = "app_cms_propertytextlong"."property_ptr_id"
    LEFT JOIN "app_cms_propertytext" ON "app_cms_propertytext"."property_ptr_id" =  "app_cms_property"."id"
    LEFT JOIN "app_cms_propertytext_translation" ON "app_cms_propertytext_translation"."master_id" = "app_cms_propertytext"."property_ptr_id"
       WHERE
       "app_cms_property"."section_id" IN  {section_ids}
       AND "app_cms_propertytextrich_translation"."language_code" = '{lang}'
       OR "app_cms_propertytextlong_translation"."language_code" = '{lang}'
       OR "app_cms_propertytext_translation"."language_code" = '{lang}'
   '''

class PageView(View):

    @minified_response
    def get(self, request, path):
        context = {
           'gCaptchaPublicKey':  os.getenv("GCAPTCHA_PUBLIC_KEY"),
           'csrfToken': get_token(request)
        }

        try:
            start = datetime.now()
            if re.match('.*\.\w{,5}$', path): #file
                return HttpResponse(status=404)

            route = self.processPath(sqlescape(path), request)

            if route.get('redirect'):
                return HttpResponseRedirect(route.get('redirect'))

            if route.get('not_found'):
                raise LookupError('not found')

            page_id = route.get('page_id')
            pattern = route.get('pattern')

            page_name, page_template = self.getPageRaw(page_id)

            params = self.getGroups(pattern, path)
            sections = self.getPageSectionsRaw(page_id)

            views = self.importViews(sections)

            views_context = {
                'page_id': page_id
            }

            views_data = self.processViews(request, views, views_context,  params)

            context = {
                **context,
                **views_data,
                'sections': sections['view_data'],
                'menus': self.getMenusRaw(page_id)
            }

            if context.get('redirect'):
                return context.get('redirect')

            print("---page render", datetime.now() - start)
            return  render(request, page_template, context = context)

        except (Page.DoesNotExist, IndexError, LookupError):
            return  render(request, 'page_404.html', context = {})

    def getGroups(self, regex, str):
        match = re.match(regex, str)
        if match and len(match.groups()):
            return match.groups()
        return []

    def importViews(self, sections):
        views = ViewModel.objects.filter(section__id__in = sections['section_ids'])
        views = [ {
            "module": self.importModule(view.module_name),
            "config": view.config
        } for view in views]
        return views

    def importModule(self, module_name):
        module_name = re.sub('\.py', '', module_name)
        return importlib.import_module(module_name)

    def processViews(self, request, views, context, params):
        context_data = {**context}
        for view in views:
            context_data = view['module'].process(request, view['config'], context_data, params)
        return context_data

    def processPath(self, path, request):
        default_language = settings.PARLER_DEFAULT_LANGUAGE_CODE
        prefix_default = settings.PREFIX_DEFAULT_LANGUAGE

        query = buildSelectPathQuery(path)
        data, success, *_ = execute_query(query)

        path_item = py_.find(data, lambda item: item['lang'] == get_language())

        if not path_item and len(data):
            lang_code = data[0]['lang']
            protocol = request.scheme + '://'
            redirect = ''
            if lang_code == default_language and not prefix_default:
                redirect = request.get_host() + '/' + path
            else:
                redirect = request.get_host() + '/' + lang_code + '/' + path

            query = '?' + request.META.get('QUERY_STRING') if request.META.get('QUERY_STRING') else ''

            return {
                'redirect': protocol + redirect + query
            }

        if not path_item:
            return {
                'not_found': True
            }

        return {
            'page_id': path_item.get('page_id'),
            'pattern': path_item.get('pattern')
        }


    def getPageRaw(self, page_id):
        query = buildSelectPageQuery(page_id)
        page, success, *_ = execute_query(query)
        return [page[0].get('name'), page[0].get('template')] if success else []

    def getMenusRaw(self, page_id):
        query = buildSelectPageMenusQuery(page_id, get_language())
        data, success, *_ = execute_query(query)
        menus = {}
        for row in data:
            menus.setdefault(row.get('id'), {
               'id': row['id'],
               'name': row['name'],
               'template': row['template'],
               'style': row['style'],
               'items': []
            })['items'].append({
               'text': row['item_text'],
               'url': row['item_url']
            })
        return menus.values()

    def getPageSectionsRaw(self, page_id):
        sections = self.getSectionsRaw(page_id)
        section_ids = [section.get("id") for section in sections]
        props = self.getSectionPropsRaw(section_ids)

        sections_view_data = [{
            'template': section.get("template"),
            'style': section.get("style"),
            'props': props.get(section.get("id"))
        } for section in sections]

        return {
            'view_data': sections_view_data,
            'section_ids': section_ids,
        }

    def getSectionsRaw(self, page_id):
        query = buildSelectSectionQuery(page_id)
        data, success, *_ = execute_query(query)
        return data

    def getSectionPropsRaw(self, ids):
        section_ids = '(' + ','.join([str(id) for id in ids]) + ')'
        query = buildSelectSectionPropQuery(section_ids, get_language())
        data, success, *_ = execute_query(query)
        props = {}
        for prop in data:
            props.setdefault(prop['id'], {})[prop['name']] = prop['value']

        return props
