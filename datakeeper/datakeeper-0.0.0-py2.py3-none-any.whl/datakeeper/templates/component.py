"""Auto-generated module for the datakeeper package that creates a customized
component for a flask app.
"""
import sys
import logging
from flask import Blueprint, request
from flask_restplus import Resource
from datakeeper.utility import import_fqn
from datakeeper.api import create_parsers, Schema, apis
from datakeeper.settings import specs

log = logging.getLogger(__name__)

blueprint = Blueprint('{{ name }}',
                      '{{ package.name }}.{{ name }}',
                      url_prefix='{{ url_prefix }}')
"""Blueprint: component-level modularization of component for a global flask app.
"""
api = apis["{{ name }}"]
"""flask_restplus.Api: api object to handle the blueprint for this component.
"""
api.init_app(blueprint)

model_specs = specs["{{ name }}"]["models"]
"""list: of model spec `dict` instances with raw model schemas"""
models = Schema()
"""Schema: model schema definitions for the component.
"""
models.load("{{ name }}", model_specs)

parsers = create_parsers(specs["{{ name }}"].parsers)
"""dict: keys are parser names, values are :class:`flask_restplus.RequestParser`.
"""

ns_specs = specs["{{ name }}"].namespaces
"""dict: keys are namespace names; values are the raw specification `dict` for
that namespace.
"""
namespaces = {}
"""dict: keys are namespace names, values are :class:`flask_restplus.Namespace`
objects.
"""
for nspec in ns_specs:
    namespaces[nspec.name] = api.namespace(nspec.name)
{% for nspec in namespaces %}
ns_{{ nspec.name }} = namespaces["{{ nspec.name }}"]
{% endfor %}
#Reinitialize the keyword arguments for the namespace; these just affect
#attributes on the namespace object, which will retain its pointer.
_nspeclookup = {s.name: s for s in ns_specs}
for nsname, ns in namespaces.items():
    nspec = _nspeclookup[nsname]
    ns.description = nspec.get("description", None)
    ns._path = nspec.get("path", None)
    ns._validate = nspec.get("validate", None)
    ns.decorators = nspec.get("decorators", [])
    ns.authorizations = nspec.get("authorizations", None)
    ns.ordered = nspec.get("ordered", False)

def _get_expectant(name):
    """Returns a parser with the given name, if it exists. If it doesn't,
    attempts to get a *model* with that name. If no model exists, an error
    is raised.
    """
    return parsers.get(name, models.get(name))
{% for nspec in namespaces %}
{%- for espec in nspec.endpoints %}

@ns_{{ nspec.name }}.route(*{{ espec.routes }})
class {{ espec.name|title }}(Resource):
    {%- for sattr in espec if sattr in ["put", "get", "post", "delete"] %}
    {%- if espec[sattr].expect %}
    @api.expect(_get_expectant("{{ espec[sattr].expect.object }}"),
                validate={{"True" if espec[sattr].expect.validate else "False"}})
    {%- endif %}
    {%- if espec[sattr].marshal %}
    @api.marshal_with(models["{{ espec[sattr].marshal.object }}"],
                      {%- if espec[sattr].marshal.envelope %}
                      envelope="{{ espec[sattr].marshal.envelope }}",
                      {%- endif %}
                      skip_none={{"True" if espec[sattr].marshal.skip_none else "False"}})
    {%- endif %}
    {%- if espec[sattr].response %}
    @api.response({{ espec[sattr].response.code }}, "{{ espec[sattr].response.message }}")
    {%- endif %}
    def {{ sattr }}(ns, *args, **kwargs):
        """{{ espec[sattr].docstring }}
        """
        {%-if espec[sattr].expect %}
        if "{{ espec[sattr].expect.object }}" in parsers:
            kwargs = parsers["{{ espec[sattr].expect.object }}"].parse_args(request)
        {%- else %}
        kwargs.update({{ espec[sattr].function.get("kwargs", {}) }})
        {%- endif %}
        kwargs["_data"] = request.json

        mod, call = import_fqn("{{ espec[sattr].function.fqn }}")
        results = call(*args, **kwargs)
        {%- if espec[sattr].response %}
        return results, {{ espec[sattr].response.code }}
        {% else %}
        return results
        {%- endif %}
    {% endfor %}
{%- endfor %}
{% endfor %}

for nspec in ns_specs:
    api.add_namespace(namespaces[nspec.name])
