"""
"""

import sys
from datetime import datetime

from flask import jsonify
from marshmallow import Schema as MSchema
from marshmallow import fields

from .__base__ import apispecs
from .component import Component
from .value import NestedValue

PATHS = {}
COMPONENTS = {}


def generate_type_format_from_schema(ty):
    if ty == int:
        return 'integer', None
    elif ty == str:
        return 'string', None
    elif ty == bool:
        return 'boolean', None
    elif ty == datetime:
        return 'string', 'date-time'


def _append_parameter(apispec, data, part):
    if part in apispec:
        for k, v in apispec[part].items():
            for ty in v.types:
                if ty in (int, str, bool, datetime):
                    gtype, gformat = generate_type_format_from_schema(ty)
                    d = {
                        'in': part,
                        'name': k,
                        'required': not v.optional,
                        'schema': {
                            'type': gtype,
                        },
                    }
                    if gformat:
                        d['format'] = gformat
                    data['parameters'].append(d)
                    break


def parse_paths_spec(apispec):
    global PATHS
    data = {
        'parameters': [],
        'tags': apispec.get('tags', []),
        'summary': apispec.get('summary', ''),
        'description': apispec.get('description', ''),
    }

    _append_parameter(apispec, data, 'query')
    _append_parameter(apispec, data, 'param')

    if 'body' in apispec:
        d, s = parse_spec(apispec['body'])
        data['requestBody'] = {
            'description': '',
            'required': True,
            'content': {
                'application/json': {
                    'schema': s
                },
            },
        }
    if 'response' in apispec:
        d, s = parse_spec(apispec['response'])
        data['responses'] = {}
        for k, v in d.items():
            if k == 200:
                data['responses'][k] = {
                    'description': '',
                    'content': {
                        'application/json': {
                            'schema': d[200]
                        }
                    }
                }
            else:
                data['responses'][k] = v
    PATHS[apispec['url']] = {
        apispec['methods'][0].lower(): data,
    }


def stype_string(): return dict(schema=dict(type='string'))


def stype_integer(): return dict(schema=dict(type='integer'))


def stype_boolean(): return dict(schema=dict(type='boolean'))


def stype_datetime(): return dict(schema=dict(type='string', format='date-time'))


def stype_list(): return dict(schema=dict(type='array', items=dict(type='string')))


def parse_spec(request):
    global COMPONENTS
    nr = {}
    if isinstance(request, fields.Field):
        if isinstance(request, fields.String):
            return stype_string(), None
        elif isinstance(request, fields.Int):
            return stype_integer(), None
        elif isinstance(request, fields.Boolean):
            return stype_boolean(), None
        elif isinstance(request, fields.DateTime):
            return stype_datetime(), None
        elif isinstance(request, fields.List):
            t, r = parse_spec(request.container)
            if r:
                nr = r
            else:
                nr = t
            nr = nr.get('schema', nr)  # strip schema key for components
            return dict(schema=dict(type='array', items=nr)), None
        elif isinstance(request, fields.Nested):
            ty = {'$ref': '#/components/schemas/%s' % request.schema.__class__.__name__}
            if request.many:
                ty = dict(type='array', items=ty)
            return parse_spec(request.schema), ty
    elif isinstance(request, Component):
        if request.__class__ and request.__class__.__dict__:
            for k, v in request.__class__.__dict__.get('_declared_fields').items():
                if k.startswith('__') or callable(v):
                    continue
                t, r = parse_spec(v)
                if r:
                    nr[k] = r
                else:
                    nr[k] = t

            nnr = {}
            for j, n in nr.items():
                nnr[j] = n.get('schema', n)  # strip schema key for components

            COMPONENTS[request.__class__.__name__] = {
                'type': 'object',
                'properties': nnr,
            }
            return nnr, {'$ref': '#/components/schemas/%s' % request.__class__.__name__}
    elif isinstance(request, NestedValue):
        return parse_spec(request.nested_class(many=request.many)), {'$ref': '#/components/schemas/%s' % request.nested_class.__name__}
    elif isinstance(request, dict):
        for k, v in request.items():
            t, r = parse_spec(v)
            if r:
                nr[k] = r
            else:
                nr[k] = t
        return nr, None
    else:
        return request, None


information_default = {
    "openapi": "3.0.1",
    "info": {
        "title": "__TITLE__",
        "description": "__DESCRIPTION__",
        # "termsOfService": "http://swagger.io/terms/",
        "contact": {
            "email": "__EMAIL__"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "version": "__VERSION"
    },
    "tags": [
        {
            "name": "default",
            "description": "default apis",
            "externalDocs": {
                "description": "Find out more",
                "url": "http://swagger.io"
            }
        },
    ]
}


def _generate():
    for spec in apispecs:
        try:
            parse_paths_spec(spec)
        except Exception as e:
            import traceback
            print('++++++++++++++++++++++++++++++++++++++++++', e)
            traceback.print_tb(sys.exc_info()[2])

    s = information_default
    s['paths'] = PATHS
    s['components'] = {
        'schemas': COMPONENTS
    }
    return s


def generate():
    return jsonify(_generate())
