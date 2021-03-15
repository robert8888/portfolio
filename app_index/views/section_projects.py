
def process(request, config, context, *args):
    print('process success', config, context)
    return {
        **context,
        'projects_data': True
    }