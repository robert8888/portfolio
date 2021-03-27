from .projects import get as getProjects

def process(request, config, context, *args):
    params = {
        'on_index': True
    }
    return {
        **context,
        'projects': getProjects(request, params)
    }
