"""This module has functions for interacting with CouchDB"""

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

import json
import uuid
from datetime import datetime
from pathlib import Path

import click
from cloudant import CouchDB
from cloudant.view import View
from flask import abort, current_app, g
from flask.cli import with_appcontext
from slugify import slugify


def get_couch():
    """Connect to the configured CouchDB."""
    if "couch" not in g:
        g.couch = CouchDB(
            current_app.config["COUCH_USERNAME"],
            current_app.config["COUCH_PASSWORD"],
            url=current_app.config["COUCH_URL"],
            connect=True,
            auto_renew=True,
        )
    return g.couch


def get_db():
    """Returns a database to interact with."""
    return get_couch()[current_app.config["COUCH_DATABASE"]]


def close_couch(e=None):
    """Disconnect from CouchDB."""
    couch = g.pop("couch", None)
    if couch is not None:
        couch.disconnect()


def build_couch():
    """Create any necessary databases and design documents."""
    couch = get_couch()
    dbname = current_app.config["COUCH_DATABASE"]
    couch.create_database(dbname, throw_on_exists=False)
    put_designs()


@click.command("build-couch")
@with_appcontext
def build_couch_command():
    """Builds the couch for easy relaxing."""
    build_couch()
    click.echo("Built a couch. Please have a seat.")


def init_app(app):
    """Register the teardown and CLI command with the app."""
    app.teardown_appcontext(close_couch)
    app.cli.add_command(build_couch_command)


def put_doc(doc):
    """Put a doc on the couch.

    If doc has a name field, the name will be slufigied and used as an id.
    Otherwise, the id will be a random UUID.
    """
    db = get_db()

    if "name" in doc and "_id" not in doc:
        # Slugify the name, use that for id
        slug = slugify(doc["name"])
        doc["_id"] = slug
        i = 1
        # Check if id exists and append/increment a number until it doesn't.
        while doc["_id"] in db:
            doc["_id"] = slug + "-{}".format(i)
            i += 1
    elif "_id" not in doc:
        # Use a UUID for name
        doc["_id"] = str(uuid.uuid4())

    # Add a created timestamp
    # Timestamps are written to couchdb in ISO-8601 format
    doc["created"] = datetime.utcnow().isoformat(timespec="seconds")

    return db.create_document(doc, throw_on_exists=True)


def update_doc(doc):
    """Update a doc.

    Adds an 'updated' field representing the current time the doc was updated.
    """
    doc["updated"] = datetime.utcnow().isoformat(timespec="seconds")
    doc.save()


def get_doc(id):
    """Gets a doc from CouchDB and returns it."""
    return get_db()[id]


def get_doc_or_404(id):
    """Tries to get a doc, otherwise abort with 404."""
    try:
        doc = get_doc(id)
    except KeyError:
        abort(404)
    return doc


def put_designs():
    """Loads all design docs from the designs/ folder and puts them.

    If any documents are missing an '_id' field, a KeyError exception will have
    been raised. Not all documents will have been loaded.
    """
    here = Path(__file__).parent

    for filename in here.glob("designs/*.json"):
        with open(filename, "r") as fp:
            data = json.load(fp)

        # See if document already exists
        if data["_id"] in get_db():
            doc = get_doc(data["_id"])
            # Popping off the revision and storing it. Then compare
            rev = doc.pop("_rev")
            doc.pop("created", None)
            if data == doc:
                get_db().clear()
                return
            # Copy the values of data to doc.
            for k in data:
                doc[k] = data[k]
            doc["_rev"] = rev  # Add the revision back
            doc.save()
        else:
            put_doc(data)


def get_view(doc_name, view_name):
    """Return a cloudant.View object matching the specified name."""
    return View(get_doc(doc_name), view_name)
