from functools import reduce
import operator

from .utils import django_search_serializer, search_db

def search(request):
    q = request.GET['q']
    context = search_db(q)
    return JsonResponse(context)
