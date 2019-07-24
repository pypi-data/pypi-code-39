"""This module handles routes for the home page"""

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

from flask import (
    current_app,
    Blueprint,
    redirect,
    url_for,
    request,
    jsonify,
    render_template,
)

from humulus.couch import get_db

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    """Renders the homepage template"""
    return redirect(url_for("recipes.index"))


@bp.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


@bp.route("/status")
def status():
    status = {"version": current_app.config["version"]}
    if request.args.get("couch", default=False):
        if get_db().exists():
            status["couch"] = "ok"
            return jsonify(status), 200
        else:
            status["couch"] = "not_exist"
            return jsonify(status), 500
    return jsonify(status), 200
