from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def execute_queries(queries = []):
    result_each = []
    success_all = True
    with connection.cursor() as cursor:
        for query in queries:
            try:
                cursor.execute(query)
                affected = cursor.rowcount
                try:
                    data = dictfetchall(cursor)
                except:
                    data = None
                result_each.append({
                    'success': True,
                    'affected': affected,
                    'data': data,
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