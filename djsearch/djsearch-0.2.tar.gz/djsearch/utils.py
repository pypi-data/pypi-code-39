from functools import reduce
import operator

from django.apps import apps
from django.db.models import Q
from django.http import JsonResponse

def django_search_serializer(obj):
    if 'link' in obj.djresult_output.keys():
        link = obj.djresult_output['link']
    else:
        try:
            link = obj.get_absolute_url()
        except:
            link = ''

    serialized_data = {
        'link': link,
        'fields': {}
    }

    for f in obj.djresult_output['fields']:
        serialized_data['fields'][f] = obj.__dict__[f]
    return serialized_data

def search_db(query, format = 'dict', models = apps.get_models()):
    context = {
        'results':{}
    }

    # Loop through all models in INSTALLED_APPS
    for m in models:
        # Checks if the 'search_fields' attribute is defined.
        # If the 'search_fields' attribute is not defined, it will not search
        # the model
        if hasattr(m, 'djsearch_fields'):
            filter_kwargs = []

            # initialize an empty queryset for the model in question (m)
            qs = m.objects.none()

            # go through each field
            for s in m.djsearch_fields:

                # split words in search query to search for each one individually
                for word in query.split(' '):
                    filter_kwargs.append(Q(**{s + '__contains': word}))
                    qs = qs | m.objects.filter(reduce(operator.or_, filter_kwargs))
            if format != 'queryset':
                for i in qs.distinct():
                    context['results'][i.__str__()] = django_search_serializer(i)
    if format == 'queryset':
        return qs.distinct()
    return context
