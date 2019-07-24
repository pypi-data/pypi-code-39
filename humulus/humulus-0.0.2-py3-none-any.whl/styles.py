"""This module has functions for working with BJCP styles."""

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

import math
import xml.etree.ElementTree as ET

import click
import requests
from flask import (
    Blueprint,
    abort,
    current_app,
    render_template,
    request,
    jsonify,
)
from flask.cli import with_appcontext

from humulus.auth import login_required
from humulus.couch import get_db, put_doc, get_view, get_doc_or_404

bp = Blueprint("styles", __name__, url_prefix="/styles")


def sub_to_doc(sub):
    """Coverts sub (XML) to a dictionary document.

    The returned dictionary can be placed right into CouchDB if you want.
    """
    doc = {
        "_id": "{}".format(sub.attrib["id"]),
        "$type": "style",
        "name": sub.find("name").text,
        "aroma": sub.find("aroma").text,
        "appearance": sub.find("appearance").text,
        "flavor": sub.find("flavor").text,
        "mouthfeel": sub.find("mouthfeel").text,
        "impression": sub.find("impression").text,
        "ibu": {},
        "og": {},
        "fg": {},
        "srm": {},
        "abv": {},
    }
    if sub.find("comments") is not None:
        doc["comments"] = sub.find("comments").text
    if sub.find("history") is not None:
        doc["history"] = sub.find("history").text
    if sub.find("ingredients") is not None:
        doc["ingredients"] = sub.find("ingredients").text
    if sub.find("comparison") is not None:
        doc["comparison"] = sub.find("comparison").text
    if sub.find("examples") is not None:
        doc["examples"] = sub.find("examples").text
    if sub.find("tags") is not None:
        doc["tags"] = sub.find("tags").text.split(", ")

    doc["ibu"]["low"] = (
        sub.find("./stats/ibu/low").text
        if sub.find("./stats/ibu/low") is not None
        else "0"
    )
    doc["ibu"]["high"] = (
        sub.find("./stats/ibu/high").text
        if sub.find("./stats/ibu/high") is not None
        else "100"
    )
    doc["og"]["low"] = (
        sub.find("./stats/og/low").text
        if sub.find("./stats/og/low") is not None
        else "1.0"
    )
    doc["og"]["high"] = (
        sub.find("./stats/og/high").text
        if sub.find("./stats/og/high") is not None
        else "1.2"
    )
    doc["fg"]["low"] = (
        sub.find("./stats/fg/low").text
        if sub.find("./stats/fg/low") is not None
        else "1.0"
    )
    doc["fg"]["high"] = (
        sub.find("./stats/fg/high").text
        if sub.find("./stats/fg/high") is not None
        else "1.2"
    )
    doc["srm"]["low"] = (
        sub.find("./stats/srm/low").text
        if sub.find("./stats/srm/low") is not None
        else "0"
    )
    doc["srm"]["high"] = (
        sub.find("./stats/srm/high").text
        if sub.find("./stats/srm/high") is not None
        else "100"
    )
    doc["abv"]["low"] = (
        sub.find("./stats/abv/low").text
        if sub.find("./stats/abv/low") is not None
        else "0"
    )
    doc["abv"]["high"] = (
        sub.find("./stats/abv/high").text
        if sub.find("./stats/abv/high") is not None
        else "100"
    )
    return doc


def import_styles(url):
    """Parses BJCP styles in XML format from `url`.

    `url` defaults to the official BJCP XML styleguide.

    Each subcategory is converted to JSON and then put to a couchdb. The _id of
    the subsequent document will be `<number><letter>`, i.e., 1A.
    If the style already exists in the database, it will be skipped.
    """
    db = get_db()
    root = ET.fromstring(requests.get(url).text)
    subs = root.findall('./class[@type="beer"]/category/subcategory')
    for sub in subs:
        doc = sub_to_doc(sub)
        if doc["_id"] not in db:
            put_doc(doc)


def get_styles_list():
    """Returns a list containing id and names of all styles."""
    view = get_view("_design/styles", "by-category")
    styles = [["", ""]]
    for row in view(include_docs=False)["rows"]:
        styles.append(
            [
                row["id"],
                "{}{} {}".format(row["key"][0], row["key"][1], row["value"]),
            ]
        )
    return styles


@click.command("import-styles")
@with_appcontext
def import_command():
    """CLI command to import BJCP styles."""
    url = current_app.config.get(
        "BJCP_STYLES_URL",
        (
            "https://raw.githubusercontent.com/meanphil"
            "/bjcp-guidelines-2015/master/styleguide.xml"
        ),
    )
    import_styles(url)
    click.echo("Imported BJCP styles.")


def init_app(app):
    """Register the CLI command with the app."""
    app.cli.add_command(import_command)


@bp.route("/")
@login_required
def index():
    descending = request.args.get(
        "descending", default="false", type=str
    ).lower() in ["true", "yes"]
    sort_by = request.args.get("sort_by", default="category", type=str)
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=20, type=int)

    view = get_view("_design/styles", "by-{}".format(sort_by))
    try:
        rows = view(include_docs=True, descending=descending)["rows"]
    except requests.exceptions.HTTPError:
        abort(400)

    return render_template(
        "styles/index.html",
        rows=rows[(page - 1) * limit : page * limit],  # noqa
        descending=descending,
        sort_by=sort_by,
        page=page,
        num_pages=math.ceil(len(rows) / limit),
        limit=limit,
    )


@bp.route("/info/<id>")
@login_required
def info(id):
    return render_template("styles/info.html", style=get_doc_or_404(id))


@bp.route("/info/<id>/json")
@login_required
def info_json(id):
    """Returns JSON for the style.

    If the 'specs' argument is present (regardless of value), only return
    specs.
    """
    style = get_doc_or_404(id)
    # Remove fields not needed for specs
    if request.args.get("specs", None) is not None:
        return jsonify(
            {
                "ibu": style["ibu"],
                "og": style["og"],
                "fg": style["fg"],
                "abv": style["abv"],
                "srm": style["srm"],
            }
        )
    # Remove fields not needed for export
    style.pop("_id")
    style.pop("_rev")
    style.pop("$type")
    return jsonify(style)


@bp.route("/info/<id>/recipes")
def recipes(id):
    style = get_doc_or_404(id)
    view = get_view("_design/recipes", "by-style")
    rows = view(include_docs=True, descending=True, key=id)["rows"]
    return render_template("styles/recipes.html", style=style, rows=rows)
