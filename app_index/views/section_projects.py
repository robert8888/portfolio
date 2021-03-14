
def process(request, data, *args):
    print('process success')
    return {
        **data,
        'projects_data': True
    }