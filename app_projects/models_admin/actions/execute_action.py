from portfolio.utils.execute_db_queries import execute_queries
from django.contrib import messages
from django.utils.translation import gettext

def executeAction(modeladmin, request, queries, msg):
    results = execute_queries(queries)

    queries_affects = {}
    for index, result in enumerate(results.get("resultEach")):
        queries_affects[str(index)] = result.get("affected", 0)


    if results.get("successAll"):
        modeladmin.message_user(request,
        msg.get("success") % queries_affects,
        messages.SUCCESS)
    else:
         modeladmin.message_user(request,
         msg.get("fail"),
         messages.ERROR)
