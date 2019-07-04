from django.conf import settings


def static_urls(request):
    """
    Adds value from ZNBSTATIC_VERSION to context.

    Add 'znbstatic.context_processors.static_urls' to the corresponding engine in
    OPTIONS.context_processors in settings.TEMPLATES, and then
    set ZNBSTATIC_VERSION and you can include {{ static_version }} in the template or use it from
    the context in a template tag.
    """
    static_version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
    return {'static_version': static_version}
