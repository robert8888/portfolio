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
from django.core.cache import cache
import pydash as py_
import importlib
import re
import os
import json



def build_select_path_query(path):
    return f"""
    SELECT
    app_cms_path.page_id as "page_id",
    app_cms_path_translation.pattern as "pattern",
    app_cms_path_translation.language_code as "lang"
    FROM app_cms_path
    LEFT JOIN app_cms_path_translation ON app_cms_path.id = app_cms_path_translation.master_id
    WHERE ( '{path}' ~ app_cms_path_translation.pattern)
    """

def build_select_page_query(page_id):
    return f"""
    SELECT
    name,
    template
    FROM app_cms_page
    WHERE id = {page_id}
    """

def build_select_page_menus_query(page_id, lang):
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

def build_select_section_query(page_id):
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

def build_select_section_prop_query(section_ids, lang):
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

def build_select_page_meta_query(page_id, lang):
    return f'''
    SELECT
    app_cms_page_meta_translation.title as "title",
    app_cms_page_meta_translation.meta_title as "meta_title",
    app_cms_page_meta_translation.meta_description as "meta_description"
    FROM app_cms_page_meta 
    LEFT JOIN app_cms_page_meta_translation ON app_cms_page_meta_translation.master_id = app_cms_page_meta.id
    WHERE app_cms_page_meta.page_id = {page_id} AND app_cms_page_meta_translation.language_code = '{lang}'
    '''


class PageView(View):

    @minified_response
    def get(self, request, path):
        start = datetime.now()
        tokens = {
           'gCaptchaPublicKey':  os.getenv("GCAPTCHA_PUBLIC_KEY"),
           'csrfToken': get_token(request)
        }
        cache_key = self.build_cache_key(request)
        template = cache.get(cache_key + '--template', None)
        context = cache.get(cache_key + '--context', None)

        if not template or not context:
            template, context = self.get_template_and_context(request, path)
            cache.set(cache_key + '--template', template, None)
            cache.set(cache_key + '--context', context, None)

        if context.get('redirect'):
            return HttpResponseRedirect(context.get('redirect'))

        print("---page render", datetime.now() - start)
        return render(request, template, context = {**context, **tokens})

    def get_template_and_context(self, request, path):
        try:
            context = {}
            if re.match('.*\.\w{,5}$', path): #file
                return HttpResponse(status=404)

            route = self.process_path(sqlescape(path), request)

            if route.get('redirect'):
                return [None, {'redirect': route.get('redirect')}]

            if route.get('not_found'):
                raise LookupError('not found')

            page_id = route.get('page_id')
            pattern = route.get('pattern')

            page_name, page_template = self.get_page_raw(page_id)

            params = self.get_groups(pattern, path)
            sections = self.get_page_sections_raw(page_id)

            views = self.import_views(sections)

            views_context = {
                'page_id': page_id
            }

            views_data = self.process_views(request, views, views_context, params)

            context = {
                **context,
                **views_data,
                'sections': sections['view_data'],
                'menus': self.get_menus_raw(page_id),
                'meta': self.get_page_meta(page_id)
            }

            return [page_template, context]
        except (Page.DoesNotExist, IndexError, LookupError):
            context = {
                'meta': {
                    'title': 'Page not found',
                    'meta_title': 'Page not found',
                    'meta_description': 'Page not found'
                }
            }
            return ['page_404.html', context]

    @staticmethod
    def get_groups(regex, str):
        match = re.match(regex, str)
        if match and len(match.groups()):
            return match.groups()
        return []

    def import_views(self, sections):
        views = ViewModel.objects.filter(section__id__in = sections['section_ids'])
        views = [ {
            "module": self.import_module(view.module_name),
            "config": view.config
        } for view in views]
        return views

    @staticmethod
    def import_module(module_name):
        module_name = re.sub('\.py', '', module_name)
        return importlib.import_module(module_name)

    @staticmethod
    def process_views(request, views, context, params):
        context_data = {**context}
        for view in views:
            context_data = view['module'].process(request, view['config'], context_data, params)
        return context_data

    @staticmethod
    def process_path(path, request):
        default_language = settings.PARLER_DEFAULT_LANGUAGE_CODE
        prefix_default = settings.PREFIX_DEFAULT_LANGUAGE

        query = build_select_path_query(path)
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

    @staticmethod
    def get_page_raw(page_id):
        query = build_select_page_query(page_id)
        page, success, *_ = execute_query(query)
        return [page[0].get('name'), page[0].get('template')] if success else []

    @staticmethod
    def get_menus_raw(page_id):
        query = build_select_page_menus_query(page_id, get_language())
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
        return list(menus.values())


    def get_page_sections_raw(self, page_id):
        sections = self.get_sections_raw(page_id)
        section_ids = [section.get("id") for section in sections]
        props = self.get_section_props_raw(section_ids)

        sections_view_data = [{
            'template': section.get("template"),
            'style': section.get("style"),
            'props': props.get(section.get("id"))
        } for section in sections]

        return {
            'view_data': sections_view_data,
            'section_ids': section_ids,
        }

    @staticmethod
    def get_sections_raw(page_id):
        query = build_select_section_query(page_id)
        data, success, *_ = execute_query(query)
        return data

    @staticmethod
    def get_section_props_raw(ids):
        section_ids = '(' + ','.join([str(id) for id in ids]) + ')'
        query = build_select_section_prop_query(section_ids, get_language())
        data, success, *_ = execute_query(query)
        props = {}
        for prop in data:
            props.setdefault(prop['id'], {})[prop['name']] = prop['value']

        return props

    @staticmethod
    def get_page_meta(page_id):
        query = build_select_page_meta_query(page_id, get_language())
        data, success, *_ = execute_query(query)
        return data[0] if success and len(data) else {}

    @staticmethod
    def build_cache_key(request):
        key = request.path + '--' + '_'.join([key + '-' + value for key, value in request.GET.items()])
        return key