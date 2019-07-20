#!/usr/bin/env python
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

"""
{% load gist %}

{{ post.body|embed_gist }}
"""

def repl(m):
    if "https://gist.github.com/" not in m[0]:
        return m[0]
    a = re.compile('<a[^>]* href="([^"]*)"')
    url = a.match(m[0]).group(1)
    print("")
    print("url = %s" % url)
    print("""<script src="%s.js"></script>""" % url)
    return """<script src="%s.js"></script>""" % url

@register.filter
def embed_gist(html):
    return re.sub(r'<a.*?>(.+?)</a>', repl, html)
