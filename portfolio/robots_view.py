from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render

def process_request(request):
   if request.get_host in settings.INDEXED_DOMAINS:
       return render(request, 'robots.txt', content_type='text/plain')
   else:
       return render(request, 'robots_no-indexed.txt', content_type='text/plain')
