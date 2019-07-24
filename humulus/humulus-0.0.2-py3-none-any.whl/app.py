"""Functions for instantiating Flask app object."""

# Copyright 2019 Mike Shoup
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is not None:
        # Load the test config if provided
        app.config.from_mapping(test_config)
    else:
        # Load config from configuration provided via ENV
        app.config.from_envvar("HUMULUS_SETTINGS")

    # Load current version of humulus
    from . import _version

    app.config["version"] = _version.__version__

    from . import couch

    couch.init_app(app)

    # Register blueprint for index page
    from . import home

    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    # Register blueprint for recipes
    from . import recipes

    app.register_blueprint(recipes.bp)

    # Register auth blueprint
    from . import auth

    app.register_blueprint(auth.bp)

    # Register styles blueprint and cli commands
    from . import styles

    styles.init_app(app)
    app.register_blueprint(styles.bp)

    # Register custom filters
    from . import filters

    filters.create_filters(app)

    # Register custom error handlers
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)

    return app


def bad_request(e):
    return (
        render_template("_error.html", code=400, message="400 Bad Request"),
        400,
    )


def page_not_found(e):
    return (
        render_template("_error.html", code=404, message="404 Not Found"),
        404,
    )
