from django.http import HttpResponse
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import render
from app_index.models import Page, PageSections
from .page_menus import getMenus
from .page_section import getPageSections

class PageView(View):
    greeting = "Good Day"


    def get(self, request, name):
        print(name)

        context = {
           'gCaptchaPublicKey': '6LfPq2QaAAAAAGpz3x-4KiBjNF3zffwFOVhlXHjD',
           'csrfToken': get_token(request)
        }

        try:
            page = Page.objects.get(address = '/' + name )
            print(getPageSections(page))
            context['sections'] = getPageSections(page)
            context['menus'] = getMenus(page)

            return  render(request, page.template, context = context)
        except Page.DoesNotExist:
            return  render(request, '404.html', context = {})


