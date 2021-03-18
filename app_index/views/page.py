from django.http import HttpResponse
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import render
from app_index.models import Page, PageSections, Path, View as ViewModel, Property
from django.utils.translation import get_language
from portfolio.utils.getAppsViewsList import getAppsViewsList
from sqlescapy import sqlescape
from django.http import HttpResponse
import importlib
import re
from datetime import datetime
from django.db import connection

class PageView(View):
    greeting = "Good Day"

    def get(self, request, path):
        context = {
           'gCaptchaPublicKey': '6LfPq2QaAAAAAGpz3x-4KiBjNF3zffwFOVhlXHjD',
           'csrfToken': get_token(request)
        }

        try:
            print("page start", datetime.now())
            if re.match('.*\.\w{,5}$', path): #file
                return HttpResponse(status=404)

            page_id, pattern = self.processPath(sqlescape(path))
            page_name, page_template = self.getPageRaw(page_id)

            if not page_id:
                raise LookupError('not found')

            params = self.getGroups(pattern, path)
            sections = self.getPageSectionsRaw(page_id)
            views = self.importViews(sections)
            views_data = self.processViews(request, views, params)
            context = {
                **context,
                **views_data,
                'sections': sections['view_data'],
                'menus': self.getMenusRaw(page_id)
            }
            print("page end", datetime.now())
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

    def processViews(self, request, views, params):
        context_data = {}
        for view in views:
            context_data = view['module'].process(request, view['config'], context_data, params)
        return context_data

    def processPath(self, path):
        query = f"""
        SELECT
        "app_index_path"."page_id",
         "app_index_path"."pattern"
         FROM "app_index_path"
         WHERE ( '{path}' ~* pattern) LIMIT 1
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return row if row else []


    def getPageRaw(self, page_id):
        query = f"""
        SELECT
        name,
        template
        FROM app_index_page
        WHERE id = {page_id}
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
        return row if row else []

    def getMenusRaw(self, page_id):
        lang = get_language()
        query = f"""
        SELECT
        "app_index_menu"."id",
        "app_index_menu"."name",
        "app_index_menu"."template",
        "app_index_menu"."style",
        "app_index_menuitem_translation"."text",
        "app_index_menuitem_translation"."url"
        FROM "app_index_page_menu"
        LEFT JOIN "app_index_menu" ON "app_index_menu"."id" = "app_index_page_menu"."menu_id"
        LEFT JOIN "app_index_menuitem" ON "app_index_menuitem"."menu_id" = "app_index_menu"."id"
        LEFT JOIN "app_index_menuitem_translation" ON "app_index_menuitem_translation"."master_id" = "app_index_menuitem"."id"
        WHERE "app_index_page_menu"."page_id" = {page_id}
        AND "app_index_menuitem_translation"."language_code" = '{lang}'
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        menus = {}
        for row in rows:
            current = menus.get(row[0])
            if not current:
                current = []
            current.append(row)
            menus[row[0]] = current

        return [
            {
                "id": menu[0][0],
                "name": menu[0][1],
                "template": menu[0][2],
                "style": menu[0][3],
                "items": [{
                    "text": menu_item[4],
                    "url": menu_item[5],
                } for menu_item in menu]
            }
            for menu in menus.values()
        ]

    def getPageSectionsRaw(self, page_id):
#         print('--section-raw-start', datetime.now())
        sections = self.getSectionsRaw(page_id)
        section_ids = [section.get("id") for section in sections]
        props = self.getSectionPropsRaw(section_ids)

        sections_view_data = []
        for section in sections:
            section_data = {
                'template': section.get("template"),
                'style': section.get("style"),
                'props': props.get(section.get("id"))
            }
            sections_view_data.append(section_data)

        return {
            'view_data': sections_view_data,
            'section_ids': section_ids,
        }

    def getSectionsRaw(self, page_id):
        query = f"""
        SELECT
        "app_index_section"."id" as "id",
        "app_index_section"."name" as "name",
        "app_index_section"."template" as "tempalte",
        "app_index_section"."style" as "style"
        FROM  "app_index_pagesections"
        LEFT JOIN "app_index_section" ON "app_index_section"."id" = "app_index_pagesections"."section_id"
          WHERE "app_index_pagesections"."page_id" = {page_id}
          ORDER BY "app_index_pagesections"."order"
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [{
                "id": row[0],
                "name": row[1],
                "template": row[2],
                "style": row[3]
            } for row in rows
        ]

    def getSectionPropsRaw(self, ids):
#         print("raw start", datetime.now())
        section_ids = '(' + ','.join([str(id) for id in ids]) + ')'
        lang = get_language()
        query =  f'''
        SELECT
        "app_index_property"."section_id",
        "app_index_property"."name",
        "app_index_propertytext_translation"."value" as "text",
        "app_index_propertytextrich_translation"."value" as "text_rich",
        "app_index_propertytextlong_translation"."value" as "text_long"
        FROM  "app_index_property"
        LEFT JOIN "app_index_propertytextrich" ON "app_index_propertytextrich"."property_ptr_id" =  "app_index_property"."id"
        LEFT JOIN "app_index_propertytextrich_translation" ON "app_index_propertytextrich_translation"."master_id" = "app_index_propertytextrich"."property_ptr_id"
        LEFT JOIN "app_index_propertytextlong" ON "app_index_propertytextlong"."property_ptr_id" =  "app_index_property"."id"
        LEFT JOIN "app_index_propertytextlong_translation" ON "app_index_propertytextlong_translation"."master_id" = "app_index_propertytextlong"."property_ptr_id"
        LEFT JOIN "app_index_propertytext" ON "app_index_propertytext"."property_ptr_id" =  "app_index_property"."id"
        LEFT JOIN "app_index_propertytext_translation" ON "app_index_propertytext_translation"."master_id" = "app_index_propertytext"."property_ptr_id"
           WHERE
           "app_index_property"."section_id" IN  {section_ids}
           AND "app_index_propertytextrich_translation"."language_code" = '{lang}'
           OR "app_index_propertytextlong_translation"."language_code" = '{lang}'
           OR "app_index_propertytext_translation"."language_code" = '{lang}'
       '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        props = {}
        for row in rows:
            current = props.get(row[0])
            props[row[0]] = {
                **(current if current else {}),
                row[1] : next(value for value in row[2:] if value is not None)
            }
        return props