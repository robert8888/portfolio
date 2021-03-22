from django.http import JsonResponse
import json
from .projects import get as getProjects

def process(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(request.body)
    print(body_data)
    projects = getProjects(request, body_data, doSerialization = True)

    return JsonResponse({
       'success': True,
       'data': projects
    })
