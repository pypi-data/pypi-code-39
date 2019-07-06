#!/usr/bin/env python

import os
import json
import flask
import inspect
from . import protocookie as pc

cdir = os.path.dirname(inspect.getfile(inspect.currentframe()))

with open(os.path.join(cdir, "config.json")) as fd:
    config = json.load(fd)

pc.encryptionKey = config["encryptionKey"]

app = flask.Flask(__name__)

cookieSetterTemplate = """
    <!doctype html>
    <title>Protobuf Cookie</title>
    <form action="/">
        <button type="submit">Reload page</button>
    </form>
    {% if authdata %}
      <p>Current authentication data from cookie:</p>
      <pre>{{ authdata}}</pre>
      <p>Raw cookie value (base64 encoded encrypted data):</p>
      <pre>{{ rawauthdata}}</pre>
    {% endif %}
    <p>Setting new authentication cookie from json:</p>
    <pre>{{ jsondata}}</pre>
    <p>
    {% if authdata %}
    <form action="/del">
        <button type="submit">Remove cookie</button>
    </form>
    {% endif %}
"""

@app.route('/')
def index():
    authdata = ""
    rawauthdata = flask.request.cookies.get(config["cookieName"])
    if rawauthdata:
        authdata=pc.decrypt(rawauthdata.encode())
    resp = flask.make_response(
            flask.render_template_string(
                cookieSetterTemplate,
                authdata=authdata,
                rawauthdata=rawauthdata,
                jsondata=json.dumps(
                    config["userDefinition"],
                    sort_keys = True,
                    indent = 4,
                    separators = (',', ': '))
                )
            )
    resp.set_cookie(
            config["cookieName"],
            pc.encrypt(config["userDefinition"]))
    return resp

@app.route('/del')
def delete_cookie():
        resp = flask.make_response(flask.redirect("/"))
        resp.set_cookie(config["cookieName"], '', expires=0)
        return resp

if __name__ == "__main__":
    app.run()
