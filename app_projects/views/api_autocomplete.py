from django.http import JsonResponse
from django.utils.translation import get_language
from django.db import connection
from sqlescapy import sqlescape
import json



def build_query(input):
    input = sqlescape(input)
    print('input', input)
    word_list = [word.strip() for word in input.split(' ') if not word == '']
    last_word = word_list[-1] if len(word_list) else input
    phrase = " <-> ".join(word_list[:-1] if len(word_list) else [])
    if phrase:
        phrase += " <-> "
    ts_query = phrase + last_word + ':*' + ' | ' + last_word + ':*'
    print(ts_query)
    lang = get_language()
    return f"""
    SELECT
    ts_headline(match.term, to_tsquery('{ts_query}'), 'MinWords = 5, MaxWords = 10') as term,
    match.rank
    FROM (
      SELECT
      term as "term",
      ts_rank_cd(
        search_vector,
        to_tsquery('{ts_query}')
      ) AS "rank"
      From app_projects_project_search_auto
      WHERE language_code = '{lang}' OR language_code = ''
      ORDER BY rank DESC
      LIMIT 10
    ) as match WHERE match.rank > 0
    """

def parse_data(rows):
    autocomplete_list = [row[0] for row in rows]
    no_duplicate = list(set(autocomplete_list))
    return no_duplicate

def process(request):
    body_data = json.loads(request.body)
    input = body_data.get('input')
    if not input:
        return JsonResponse({
           'success': False,
           'errors': ['No input string for autocomplete']
        })

    query = build_query(input)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        data = parse_data(rows)
        return JsonResponse({
           'success': True,
           'data': data
        })
    except:
        return JsonResponse({
           'success': False,
           'errors': ['Server database query error']
        })

