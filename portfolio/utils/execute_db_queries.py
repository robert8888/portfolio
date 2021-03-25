from django.db import connection

def execute_queries(queries = []):
    result_each = []
    success_all = True
    with connection.cursor() as cursor:
        for query in queries:
            try:
                cursor.execute(query)
                affected = cursor.rowcount
                result_each.append({
                    'success': True,
                    'affected': affected
                })
            except BaseException as error:
#                 print(error)
                result_each.append({
                    'success': False,
                })
                success_all = False
    return {
        "successAll": success_all,
        "resultEach": result_each
    }