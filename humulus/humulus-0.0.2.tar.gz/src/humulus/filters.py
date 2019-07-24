"""This module contains filters used in rendering of Jinja templates."""

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


def recipe_og(recipe):
    """Returns a recipe's Original Gravity"""
    if "fermentables" not in recipe:
        return "0.000"
    points = 0
    grain_points = 0
    # Loop through fermentables, adding up points
    for fermentable in recipe["fermentables"]:
        if fermentable["type"] == "Grain":
            grain_points += float(fermentable["amount"]) * float(
                fermentable["ppg"]
            )
        else:
            points += float(fermentable["amount"]) * float(fermentable["ppg"])
    points += grain_points * float(recipe["efficiency"]) / 100
    return "{:.3f}".format(
        round(1 + points / (1000 * float(recipe["volume"])), 3)
    )


def recipe_fg(recipe):
    """Returns a recipe's final gravity"""
    if "yeast" not in recipe or "fermentables" not in recipe:
        return "0.000"
    og = float(recipe_og(recipe))
    og_delta = 0.0
    # Adjust original gravity by removing nonfermentables (i.e., Lactose)
    for fermentable in recipe["fermentables"]:
        if fermentable["type"] == "Non-fermentable":
            og_delta += (
                float(fermentable["amount"])
                * float(fermentable["ppg"])
                / (1000 * float(recipe["volume"]))
            )
    attenuation = (
        float(recipe["yeast"]["low_attenuation"])
        + float(recipe["yeast"]["high_attenuation"])
    ) / 200
    return "{:.3f}".format(
        round(1 + (og - 1 - og_delta) * (1 - attenuation) + og_delta, 3)
    )


def recipe_ibu(recipe):
    """Return a recipe's IBU"""
    if "hops" not in recipe:
        return "0"
    bigness = 1.65 * 0.000125 ** (float(recipe_og(recipe)) - 1)
    ibu = 0.0
    for h in recipe["hops"]:
        if h["use"] != "Boil" and h["use"] != "FWH":
            continue
        mgl = (
            float(h["alpha"])
            * float(h["amount"])
            * 7490.0
            / (float(recipe["volume"]) * 100.0)
        )
        btf = (1 - math.exp(-0.04 * float(h["duration"]))) / 4.15
        ibu += bigness * btf * mgl
    return "{:.0f}".format(ibu)


def recipe_ibu_ratio(recipe):
    """Return a recipe's IBU ratio"""
    if "fermentables" not in recipe or "hops" not in recipe:
        return "0"
    if len(recipe["fermentables"]) == 0:
        return "0"  # Otherwise a divide by zero error will occur
    og = float(recipe_og(recipe))
    ibu = float(recipe_ibu(recipe))
    return "{:.2f}".format(round(0.001 * ibu / (og - 1), 2))


def recipe_abv(recipe):
    """Return a recipe's finished ABV"""
    if "fermentables" not in recipe or "yeast" not in recipe:
        return "0"
    og = float(recipe_og(recipe))
    fg = float(recipe_fg(recipe))
    return "{:.1f}".format(round((og - fg) * 131.25, 1))


def recipe_srm(recipe):
    """Return a recipe's SRM"""
    if "fermentables" not in recipe:
        return "0"
    mcu = 0
    for f in recipe["fermentables"]:
        mcu += float(f["amount"]) * float(f["color"]) / float(recipe["volume"])
    return "{:.0f}".format(1.4922 * (mcu ** 0.6859))


def sort_hops(hops, form=False):
    """Sorts a list of hops by use in recipe."""
    by_use = {"FWH": [], "Boil": [], "Whirlpool": [], "Dry-Hop": []}

    # Split hops into each use type.
    for hop in hops:
        if form:
            by_use[hop.use.data].append(hop)
        else:
            by_use[hop["use"]].append(hop)

    if form:

        def key(hop):
            return float(hop.duration.data)

    else:

        def key(hop):
            return float(hop["duration"])

    hops_sorted = sorted(by_use["FWH"], key=key, reverse=True)
    hops_sorted.extend(sorted(by_use["Boil"], key=key, reverse=True))
    hops_sorted.extend(sorted(by_use["Whirlpool"], key=key, reverse=True))
    hops_sorted.extend(sorted(by_use["Dry-Hop"], key=key, reverse=True))
    return hops_sorted


def ferm_pct(fermentables):
    """Adds a 'pct' to each fermentable in fermentables.

    'pct' represents the total percentage a fermentable makes up of the grist.
    """
    total = 0
    # Calculate total
    for ferm in fermentables:
        total += float(ferm["amount"])
    # Add a pct to each ferm
    for ferm in fermentables:
        ferm["pct"] = 100 * float(ferm["amount"]) / total
    return fermentables


def create_filters(app):
    app.add_template_filter(recipe_og)
    app.add_template_filter(recipe_fg)
    app.add_template_filter(recipe_ibu)
    app.add_template_filter(recipe_ibu_ratio)
    app.add_template_filter(recipe_abv)
    app.add_template_filter(recipe_srm)
    app.add_template_filter(sort_hops)
    app.add_template_filter(ferm_pct)
