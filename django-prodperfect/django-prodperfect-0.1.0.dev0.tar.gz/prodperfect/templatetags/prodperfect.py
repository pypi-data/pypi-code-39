"""
prodperfect
Created by Lemuel Boyce on 2019-07-15
"""

import json

from django import template

from prodperfect.settings import settings

register = template.Library()


@register.inclusion_tag('prodperfect/tracking_snippet.html', takes_context=True)
def tracking_snippet(context):
    context['prodperfect_host'] = settings.HOST
    context['prodperfect_write_key'] = settings.WRITE_KEY
    context['prodperfect_project_id'] = settings.PROJECT_ID
    context['prodperfect_tracking_lib'] = settings.TRACKING_LIBRARY_URL
    context['prodperfect_request_type'] = settings.REQUEST_TYPE
    context['prodperfect_options'] = json.dumps(settings.OPTIONS)
    return context
