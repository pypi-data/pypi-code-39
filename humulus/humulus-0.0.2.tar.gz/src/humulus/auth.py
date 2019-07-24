"""This module handles routes for authentication."""

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

import functools

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField
from wtforms.validators import DataRequired


bp = Blueprint("auth", __name__)


class LoginForm(FlaskForm):
    """Form for login."""

    password = PasswordField("Password", validators=[DataRequired()])
    permanent = BooleanField("Stay logged in")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        logged_in = session.get("logged_in", False)
        if not logged_in:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.password.data == current_app.config["HUMULUS_PASSWORD"]:
            session.clear()
            session.permanent = form.permanent.data
            session["logged_in"] = True
            return redirect(url_for("index"))
        flash("Password is invalid.", category="warning")
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
