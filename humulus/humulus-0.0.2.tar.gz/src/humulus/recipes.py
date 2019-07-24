"""This module handles routes for the recipes"""

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
from decimal import Decimal

import requests
from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    jsonify,
    request,
    url_for,
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (
    Form,
    StringField,
    DecimalField,
    TextAreaField,
    FieldList,
    FormField,
    SelectField,
)
from wtforms.validators import DataRequired, Optional

from humulus.auth import login_required
from humulus.couch import (
    get_doc,
    get_doc_or_404,
    put_doc,
    update_doc,
    get_view,
)
from humulus.styles import get_styles_list

bp = Blueprint("recipes", __name__, url_prefix="/recipes")


class FermentableForm(Form):
    """Form for fermentables.

    CSRF is disabled for this form (using `Form as parent class)
    because it is never used by itself.
    """

    name = StringField("Name", validators=[DataRequired()])
    type = SelectField(
        "Type",
        validators=[DataRequired()],
        choices=[
            (c, c)
            for c in [
                "Grain",
                "LME",
                "DME",
                "Sugar",
                "Non-fermentable",
                "Other",
            ]
        ],
    )
    amount = DecimalField("Amount (lb)", validators=[DataRequired()])
    ppg = DecimalField("PPG", validators=[DataRequired()])
    color = DecimalField("Color (°L)", validators=[DataRequired()])

    @property
    def doc(self):
        """Returns a dictionary that can be deserialized into JSON.

        Used for putting into CouchDB.
        """
        return {
            "name": self.name.data,
            "type": self.type.data,
            "amount": str(self.amount.data),
            "ppg": str(self.ppg.data),
            "color": str(self.color.data),
        }


class HopForm(Form):
    """Form for hops.

    CSRF is disabled for this form (using `Form as parent class)
    because it is never used by itself.
    """

    name = StringField("Name", validators=[DataRequired()])
    use = SelectField(
        "Usage",
        validators=[DataRequired()],
        choices=[(c, c) for c in ["Boil", "FWH", "Whirlpool", "Dry-Hop"]],
    )
    alpha = DecimalField("Alpha Acid %", validators=[DataRequired()])
    duration = DecimalField("Duration (min/day)", validators=[DataRequired()])
    amount = DecimalField("Amount (oz)", validators=[DataRequired()])

    @property
    def doc(self):
        """Returns a dictionary that can be deserialized into JSON.

        Used for putting into CouchDB.
        """
        return {
            "name": self.name.data,
            "use": self.use.data,
            "alpha": str(self.alpha.data),
            "duration": str(self.duration.data),
            "amount": str(self.amount.data),
        }


class YeastForm(Form):
    """Form for yeast.

    CSRF is disabled for this form (using `Form as parent class)
    because it is never used by itself.
    """

    name = StringField("Name", validators=[Optional()])
    type = SelectField(
        "Type",
        default="",
        choices=[(c, c) for c in ["", "Liquid", "Dry"]],
        validators=[Optional()],
    )
    lab = StringField("Lab")
    code = StringField("Lab Code")
    flocculation = SelectField(
        "Flocculation",
        default="",
        choices=[(c, c) for c in ["", "Low", "Medium", "High"]],
        validators=[Optional()],
    )
    low_attenuation = DecimalField("Low Attenuation", validators=[Optional()])
    high_attenuation = DecimalField(
        "High Attenuation", validators=[Optional()]
    )
    min_temperature = DecimalField("Min Temp (°F)", validators=[Optional()])
    max_temperature = DecimalField("Max Temp (°F)", validators=[Optional()])
    abv_tolerance = DecimalField("ABV % tolerance", validators=[Optional()])

    @property
    def doc(self):
        """Returns a dictionary that can be deserialized into JSON.

        Used for putting into CouchDB.
        """
        yeast = {
            "name": self.name.data,
            "low_attenuation": str(self.low_attenuation.data),
            "high_attenuation": str(self.high_attenuation.data),
        }
        if self.type.data:
            yeast["type"] = self.type.data
        if self.lab.data:
            yeast["lab"] = self.lab.data
        if self.code.data:
            yeast["code"] = self.code.data
        if self.flocculation.data:
            yeast["flocculation"] = self.flocculation.data
        if self.min_temperature.data:
            yeast["min_temperature"] = str(self.min_temperature.data)
        if self.max_temperature.data:
            yeast["max_temperature"] = str(self.max_temperature.data)
        if self.abv_tolerance.data:
            yeast["abv_tolerance"] = str(self.abv_tolerance.data)
        return yeast


class MashStepForm(Form):
    """Form for mash steps.

    CSRF is disabled for this form (using `Form as parent class)
    because it is never used by itself.
    """

    name = StringField("Step Name", validators=[DataRequired()])
    type = SelectField(
        "Type",
        choices=[(c, c) for c in ["Infusion", "Temperature", "Decoction"]],
    )
    temp = DecimalField("Temperature (°F)", validators=[DataRequired()])
    time = DecimalField("Time (min)", validators=[DataRequired()])
    amount = DecimalField("Water Amount (gal)")

    @property
    def doc(self):
        """Returns a dictionary that can be deserialized into JSON.

        Used for putting into CouchDB.
        """
        step = {
            "name": self.name.data,
            "type": self.type.data,
            "temp": str(self.temp.data),
            "time": str(self.time.data),
        }
        if self.amount.data:
            step["amount"] = str(self.amount.data)
        return step


class MashForm(Form):
    """Form for mash.

    CSRF is disabled for this form (using `Form as parent class)
    because it is never used by itself.
    """

    name = StringField("Mash Name", validators=[Optional()])
    steps = FieldList(FormField(MashStepForm), min_entries=0, max_entries=20)

    @property
    def doc(self):
        """Returns a dictionary that can be deserialized into JSON.

        Used for putting into CouchDB.
        """
        return {"name": self.name.data, "steps": [s.doc for s in self.steps]}


class RecipeForm(FlaskForm):
    """Form for recipes."""

    name = StringField("Name", validators=[DataRequired()])
    type = SelectField(
        "Type",
        default="",
        choices=[(c, c) for c in ["All-Grain", "Partial Extract", "Extract"]],
        validators=[Optional()],
    )
    efficiency = DecimalField(
        "Batch Efficiency (%)", validators=[DataRequired()]
    )
    volume = DecimalField("Batch Volume (gal)", validators=[DataRequired()])
    notes = TextAreaField("Notes")
    fermentables = FieldList(
        FormField(FermentableForm), min_entries=0, max_entries=20
    )
    hops = FieldList(FormField(HopForm), min_entries=0, max_entries=20)
    yeast = FormField(YeastForm)
    mash = FormField(MashForm)
    style = SelectField("Style", choices=[], validators=[Optional()])

    @property
    def doc(self):
        """Returns a dictionary that can be deserialized into JSON.

        Used for putting into CouchDB.
        """
        recipe = {
            "name": self.name.data,
            "efficiency": str(self.efficiency.data),
            "volume": str(self.volume.data),
            "notes": self.notes.data,
            "$type": "recipe",
            "type": self.type.data,
            "style": self.style.data,
        }

        recipe["fermentables"] = [f.doc for f in self.fermentables]
        recipe["hops"] = [h.doc for h in self.hops]
        if (
            self.yeast.doc["name"]
            and self.yeast.doc["low_attenuation"] != "None"
            and self.yeast.doc["high_attenuation"] != "None"
        ):
            recipe["yeast"] = self.yeast.doc
        if self.mash.doc["name"]:
            recipe["mash"] = self.mash.doc
        return recipe

    def copyfrom(self, data):
        """Copies from a dictionary (data) into the current object"""
        self.name.data = data["name"]
        self.type.data = data["type"]
        self.efficiency.data = Decimal(data["efficiency"])
        self.volume.data = Decimal(data["volume"])
        self.notes.data = data["notes"]
        self.style.data = data["style"]

        for fermentable in data["fermentables"]:
            self.fermentables.append_entry(
                {
                    "name": fermentable["name"],
                    "type": fermentable["type"],
                    "amount": Decimal(fermentable["amount"]),
                    "ppg": Decimal(fermentable["ppg"]),
                    "color": Decimal(fermentable["color"]),
                }
            )

        for hop in data["hops"]:
            self.hops.append_entry(
                {
                    "name": hop["name"],
                    "use": hop["use"],
                    "alpha": Decimal(hop["alpha"]),
                    "duration": Decimal(hop["duration"]),
                    "amount": Decimal(hop["amount"]),
                }
            )

        if "yeast" in data:
            self.yeast.form.name.data = data["yeast"]["name"]
            self.yeast.form.low_attenuation.data = Decimal(
                data["yeast"]["low_attenuation"]
            )
            self.yeast.form.high_attenuation.data = Decimal(
                data["yeast"]["high_attenuation"]
            )
            if "type" in data["yeast"]:
                self.yeast.form.type.data = data["yeast"]["type"]
            if "lab" in data["yeast"]:
                self.yeast.form.lab.data = data["yeast"]["lab"]
            if "code" in data["yeast"]:
                self.yeast.form.code.data = data["yeast"]["code"]
            if "flocculation" in data["yeast"]:
                self.yeast.form.flocculation.data = data["yeast"][
                    "flocculation"
                ]
            if "min_temperature" in data["yeast"]:
                self.yeast.form.min_temperature.data = Decimal(
                    data["yeast"]["min_temperature"]
                )
            if "max_temperature" in data["yeast"]:
                self.yeast.form.max_temperature.data = Decimal(
                    data["yeast"]["max_temperature"]
                )
            if "abv_tolerance" in data["yeast"]:
                self.yeast.form.abv_tolerance.data = Decimal(
                    data["yeast"]["abv_tolerance"]
                )

        if "mash" in data:
            if "name" in data["mash"]:
                self.mash.form.name.data = data["mash"]["name"]
            if "steps" in data["mash"]:
                for step in data["mash"]["steps"]:
                    new_step = {
                        "name": step["name"],
                        "type": step["type"],
                        "temp": Decimal(step["temp"]),
                        "time": Decimal(step["time"]),
                    }
                    if "amount" in step:
                        new_step["amount"] = Decimal(step["amount"])
                    print(new_step)
                    self.mash.steps.append_entry(new_step)


class ImportForm(FlaskForm):
    upload = FileField(validators=[FileRequired()])


@bp.route("/")
def index():
    descending = request.args.get(
        "descending", default="false", type=str
    ).lower() in ["true", "yes"]
    sort_by = request.args.get("sort_by", default="name", type=str)

    view = get_view("_design/recipes", "by-{}".format(sort_by))
    try:
        rows = view(include_docs=True, descending=descending)["rows"]
    except requests.exceptions.HTTPError:
        abort(400)

    return render_template(
        "recipes/index.html", rows=rows, descending=descending, sort_by=sort_by
    )


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = RecipeForm()
    form.style.choices = get_styles_list()

    if form.validate_on_submit():
        response = put_doc(form.doc)
        flash("Created recipe: {}".format(form.name.data), "success")
        return redirect(url_for("recipes.info", id=response["_id"]))
    return render_template("recipes/create.html", form=form)


@bp.route("/create/json", methods=("GET", "POST"))
@login_required
def create_json():
    form = ImportForm()
    if form.validate_on_submit():
        recipe = RecipeForm()
        try:
            recipe.copyfrom(json.load(form.upload.data))
        except Exception as e:
            flash("Error converting data from JSON: {}".format(e), "warning")
            return render_template("recipes/create_json.html", form=form)
        response = put_doc(recipe.doc)
        return redirect(url_for("recipes.info", id=response["_id"]))
    return render_template("recipes/create_json.html", form=form)


@bp.route("/info/<id>")
def info(id):
    recipe = get_doc_or_404(id)

    style = None
    if recipe["style"] != "":
        try:
            style = get_doc(recipe["style"])
        except KeyError:
            flash(
                "Could not find style `{}`.".format(recipe["style"]), "warning"
            )

    return render_template("recipes/info.html", recipe=recipe, style=style)


@bp.route("/info/<id>/json")
def info_json(id):
    recipe = get_doc_or_404(id)
    # Remove fields specific not intended for export
    recipe.pop("_id")
    recipe.pop("_rev")
    recipe.pop("$type")
    return jsonify(recipe)


@bp.route("/delete/<id>", methods=("POST",))
@login_required
def delete(id):
    recipe = get_doc_or_404(id)
    recipe.delete()
    return redirect(url_for("home.index"))


@bp.route("/update/<id>", methods=("GET", "POST"))
@login_required
def update(id):
    # Get the recipe from the database and validate it is the same revision
    form = RecipeForm()
    form.style.choices = get_styles_list()
    recipe = get_doc_or_404(id)
    if form.validate_on_submit():
        if recipe["_rev"] != request.args.get("rev", None):
            flash(
                (
                    "Update conflict for recipe: {}. "
                    "Your changes have been lost.".format(recipe["name"])
                ),
                "danger",
            )
            return redirect(url_for("recipes.info", id=id))
        # Copy values from submitted form to the existing recipe and save
        for key, value in form.doc.items():
            recipe[key] = value
        update_doc(recipe)

        flash("Updated recipe: {}".format(form.name.data), "success")
        return redirect(url_for("recipes.info", id=id))
    else:
        form.copyfrom(recipe)

    return render_template(
        "recipes/update.html", form=form, id=id, rev=recipe["_rev"]
    )
