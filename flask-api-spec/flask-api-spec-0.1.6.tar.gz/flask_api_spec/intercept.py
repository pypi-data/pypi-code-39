import os
import re
import sys
from functools import wraps

import jinja2
import marshmallow
import schema as pyschema
from flask import abort, jsonify, render_template, request, send_from_directory
from marshmallow import Schema as MSchema
from marshmallow import fields
from schema import Optional, Schema, SchemaError

from .__base__ import apispecs
from .exceptions import ValidationError
from .generate import generate
from .component import Component

RE_URL_WITH_PARAM = re.compile(r"<.*?:(.*?)>")
app = None


def _validate(component, obj):
    try:
        Schema(component).validate(obj)
    except pyschema.SchemaError as e:
        raise ValidationError(e.args[0], payload=obj)


def validate_querystring(component, data):
    n = {}
    for k, v in component.items():
        if v.optional:
            n[Optional(k)] = v
        else:
            n[k] = v
    query = {}
    for k, v in data.items():
        query[k] = v[0]
    _validate(n, query)


def validate_parameter(component, data):
    """
    parameters are not optional.
    """
    _validate(component, data)


def validate_body(maybe_component, data):
    """
    check if component is validatable recursively, validate the data

    maybe_component is maybe Request
    """
    if isinstance(maybe_component, Component):
        _validate(maybe_component.schema, data)
    # if isinstance(maybe_component, Request):
    #     _validate(maybe_component.schema, data)
    elif isinstance(maybe_component, dict):
        for k, component in maybe_component.items():
            try:
                validate_body(component, data[k])
            except KeyError as e:  # no such key in data
                raise ValidationError('Missing key: %s', payload=e)


def populate_response(maybe_component, data):
    """
    make response object
    """
    # if component.serializable(maybe_component):
    #     try:
    #         maybe_component.serialize(data)
    # maybe_component is serializable
    if isinstance(maybe_component, Component):
        try:
            maybe_component.load(data)
            return maybe_component.dump(data)
        except marshmallow.exceptions.ValidationError as v_e:
            raise ValidationError(v_e.messages, payload=data)
    # maybe_component is dict
    new_response = dict()
    for k, component in maybe_component.items():
        # try as dict
        try:
            response = data[k]  # dict
        except KeyError:
            # next, try as object
            try:
                response = getattr(data, k)  # object
            except AttributeError as a_e:
                raise ValidationError(str(a_e), payload=data)

        if isinstance(component, dict) or isinstance(component, MSchema):  # dict or MSchema
            new_response[k] = populate_response(component, response)
        else:
            new_response[k] = response
    return new_response


def apispec(spec):
    def deco(f):
        apispecs.append(spec)
        spec_keys = spec

        # create request validators
        validators = []
        if 'query' in spec_keys:
            validators.append(
                lambda req, kwargs: validate_querystring(spec['query'], dict(req.args)))
        if 'param' in spec_keys:
            validators.append(
                lambda req, kwargs: validate_parameter(spec['param'], kwargs))
        if 'body' in spec_keys:
            validators.append(
                lambda req, kwargs: validate_body(spec['body'], req.json))

        @wraps(f)
        def inner(*args, **kwargs):
            response_as_html = 'text/html' in request.headers.get('accept')
            try:
                for validator in validators:
                    validator(request, kwargs)
            except (ValidationError, SchemaError) as v_e:
                if response_as_html:
                    raise ValidationError(v_e)
                else:
                    # validation failed. raise 406 error.
                    resp = app.make_response(jsonify(dict(
                        error='validation error', message=str(v_e))))
                    resp.status_code = 406
                    abort(resp)
            response = f(*args, **kwargs)
            try:
                if 'response' in spec_keys:
                    response = populate_response(
                        spec['response']['200'], response)
                return jsonify(response)
            except ValidationError as v_e:
                if response_as_html:
                    raise v_e
                else:
                    resp = app.make_response(jsonify(dict(
                        error='validation error', message=str(v_e))))
                    resp.status_code = 406
                    abort(resp)
        return inner
    return deco


def route(rule, **kwargs):
    spec = kwargs.get('apispec')
    if spec:
        spec['description'] = ''
        spec['summary'] = spec.get('summary', '')
        if 'methods' in kwargs:
            spec['methods'] = kwargs['methods']
        else:
            spec['methods'] = ['GET']

        del kwargs['apispec']

    def decorator(f):
        endpoint = kwargs.pop('endpoint', None)
        if spec:
            spec['url'] = re.sub(RE_URL_WITH_PARAM, '{\\1}', rule)
            spec['description'] = normalize_doc(f.__doc__) or ''
            f = apispec(spec)(f)
        app.add_url_rule(rule, endpoint, f, **kwargs)
        return f
    return decorator


# https://www.python.org/dev/peps/pep-0257/
def normalize_doc(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def init_app(_app):
    global app
    app = _app
    app.route = route

    # custom template directory
    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'templates')
    app.jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(tmpl_dir),
    ])

    # additional routes

    @app.route('/spec')
    def flask_api_spec_docs():
        return generate()

    @app.route('/flask-api-spec/static/<path:filename>')
    def flask_api_spec_static(filename):
        return send_from_directory('%s/../static' % (tmpl_dir,), filename)

    @app.route('/docs')
    def flask_api_docs():
        return render_template('swagger.html')
