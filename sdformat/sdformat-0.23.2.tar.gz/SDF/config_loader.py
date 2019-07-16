"""
    Read SDF config file.
    ---------------------

    Copyright (C) 2017-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import json
import os

_HOME = os.path.expanduser("~")

_CONFIG_DIR = _HOME + "/.sdf"
_CONFIG_FILE = _CONFIG_DIR + "/config.json"


def _create_default_config(cfg_file: str):
    cfg = {"use_system_jpkfile": False,
           "use_system_igor": False,
           "use_system_oiffile": False,
           "use_system_tifffile": False,
           "use_system_mfpfile": False}
    with open(cfg_file, 'wt') as fh:
        json.dump(cfg, fh)


def _load_config(cfg_file) -> "ConfigContainer":
    with open(cfg_file, 'rt') as fh:
        cfg_dict = json.load(fh)
    return type('ConfigContainer', (), cfg_dict)


if not os.path.isdir(_CONFIG_DIR):
    os.mkdir(_CONFIG_DIR)
    _create_default_config(_CONFIG_FILE)
if not os.path.isfile(_CONFIG_FILE):
    _create_default_config(_CONFIG_FILE)
CONFIG = _load_config(_CONFIG_FILE)