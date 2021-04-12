from portfolio.utils.execute_db_queries import execute_queries
from django.urls import reverse

def buildQuery():
    return """
    SELECT
    slug as "slug"
    FROM app_owner_cv
    WHERE on_main_page = TRUE
    """

def process(request, config, context, *args):
    query_results = execute_queries([buildQuery()])

    if not query_results['successAll']:
        return context

    cv = query_results['resultEach'][0]['data']
    if not len(cv):
        return context

    slug = cv[0].get('slug', None)

    if not slug:
        return context

    path = reverse('cv', kwargs={'slug': slug})

    context['cv_download_url'] = request.scheme + '://' + request.get_host() + path

    return context