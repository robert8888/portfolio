from projects.views.index import *


def index(request):
    context = {}
    return render(request, 'index.html', context=context)