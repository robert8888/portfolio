from django.shortcuts import render

def handler404(request, exception):
    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 404
    print('hellow')
    return response