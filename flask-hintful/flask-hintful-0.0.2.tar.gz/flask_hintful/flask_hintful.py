import re
from dataclasses import is_dataclass

from flask import Blueprint, Flask, jsonify
from openapi_specgen import OpenApi, OpenApiParam, OpenApiPath, OpenApiResponse

from .utils import get_func_metadata
from .wrappers import BlueprintWrapper, view_func_wrapper


class FlaskHintful():

    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app
        self.openapi_paths = []
        self.flask_app.add_url_rule('/openapi.json', view_func=self.openapi_json)
        self.flask_app.add_url_rule('/swagger', view_func=self.swagger_ui)

    def swagger_ui(self):
        return '''
            <! doctype html>
            <html>
            <head>
            <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css">
            <title>
            </title>
            </head>
            <body>
            <div id="swagger-ui">
            </div>
            <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
            <!-- `SwaggerUIBundle` is now available on the page -->
            <script>

            const ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                deepLinking: true
            })
            </script>
            </body>
            </html>
    '''

    def openapi_json(self):
        return jsonify(OpenApi(self.flask_app.name, self.openapi_paths).as_dict())

    def _add_openapi_path(self, rule, methods, view_func):

        func_metadata = get_func_metadata(view_func)
        openapi_params = []
        body = None

        for param_name, param in func_metadata['params'].items():
            if hasattr(param.annotation, '__marshmallow__'):
                body = param.annotation.__marshmallow__.__class__
            elif is_dataclass(param.annotation):
                body = param.annotation
            elif f'<{param_name}>' in re.findall('<.*?>', rule):
                openapi_params.append(
                    OpenApiParam(
                        param_name,
                        'path',
                        data_type=param.annotation if param.annotation is not param.empty else None,
                        default=param.default if param.default is not param.empty else None,
                        required=param.default is param.empty
                    )
                )
            else:
                openapi_params.append(
                    OpenApiParam(
                        param_name,
                        'query',
                        data_type=param.annotation if param.annotation is not param.empty else None,
                        default=param.default if param.default is not param.empty else None,
                        required=param.default is param.empty
                    )
                )

        response_type = func_metadata['return'] if func_metadata['return'] is not func_metadata['empty'] else str

        if hasattr(response_type, '__marshmallow__'):
            response_type = response_type.__marshmallow__.__class__

        openapi_response = OpenApiResponse('', data_type=response_type)

        for method in methods:
            self.openapi_paths.append(
                OpenApiPath(
                    rule.replace('<', '{').replace('>', '}'),
                    method.lower(),
                    [openapi_response],
                    openapi_params,
                    descr=func_metadata['doc'],
                    request_body=body
                )
            )

    def route(self, rule: str, **options):
        def decorator(view_func):
            wrapped_view_func = view_func_wrapper(view_func)
            self.flask_app.route(rule, **options)(wrapped_view_func)
            self._add_openapi_path(rule, options.get('methods', ['GET']), view_func)
            return view_func
        return decorator

    def register_blueprint(self, blueprint: Blueprint):
        bp_wrapper = BlueprintWrapper(self)
        for i, func in enumerate(blueprint.deferred_functions):
            blueprint.deferred_functions[i] = func(bp_wrapper)
        self.flask_app.register_blueprint(blueprint)
