from portfolio.utils.execute_db_queries import execute_queries
from django.contrib import messages
from django.utils.translation import gettext

def executeAction(modeladmin, request, queries, msg):
    results = execute_queries(queries)
    queries_affects =  tuple([result.get("affected") for result in results.get("resultEach")])
    print(results)
    if results.get("successAll"):
        modeladmin.message_user(request,
        msg.get("success") % queries_affects,
        messages.SUCCESS)
    else:
         modeladmin.message_user(request,
         msg.get("fail"),
         messages.ERROR)

#         gettext(f"""
#             Rebuilt autocomplete dictionary. Removed {results.get("resultEach")[0].get("affected", "-")}
#             term and added {results.get("resultEach")[1].get("affected", "-")} terms
#         """),

#          gettext('Rebuild autocomplete dictionary fail'),