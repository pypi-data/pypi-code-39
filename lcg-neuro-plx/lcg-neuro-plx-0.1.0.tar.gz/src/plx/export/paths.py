# -*-coding: utf-8 -*-
#
# projectv2 - Visual investigations of electrical recordings on the primate secondary visual cortex
# Copyright (C) 2019 Laboratório de Computação Gráfica
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# If you have any questions or suggestions regarding this software, visit
# <http://gitlab.com/lcg/v2/projectv2>.

"""This submodule defines the canonical paths for parts of *PLX* files exported by the :func:`plx.export.export_file`
function. All functions in this module accept a ``base_dir`` argument that indicates the base directory where other
files/directories will be created. Functions :func:`slow_channels` and :func:`spike_channels` take an additional ``channel``
parameter indicating the channel number for which a slow waveform or spike data file path is generated.
"""

import pathlib


def counts(base_dir, extension="bin"):
    """Path for the counts section (:class:`plx.parsing.Counts`)."""
    return pathlib.Path(base_dir) / f"counts.{extension}"


def event_data(base_dir, extension="bin"):
    """Path for the condensed event channel data (:class:`plx.export.ExportedEvent`)."""
    return pathlib.Path(base_dir) / f"event_data.{extension}"


def event_headers(base_dir, extension="bin"):
    """Path for the concatenated event channel headers (:class:`plx.parsing.EventHeader`)."""
    return pathlib.Path(base_dir) / f"event_headers.{extension}"


def header(base_dir, extension="bin"):
    """Path for the main header section (:class:`plx.parsing.Header`)."""
    return pathlib.Path(base_dir) / f"header.{extension}"


def slow_headers(base_dir, extension="bin"):
    """Path for the concatenated slow waveform channel headers (:class:`plx.parsing.SlowHeader`)."""
    return pathlib.Path(base_dir) / f"slow_headers.{extension}"


def spike_headers(base_dir, extension="bin"):
    """Path for the concatenated spike channel headers (:class:`plx.parsing.SpikeHeader`)."""
    return pathlib.Path(base_dir) / f"spike_headers.{extension}"


def slow_channel(base_dir, channel=None):
    """Path for the condensed slow waveform data of a single channel (:attr:`plx.export.exported_slow_dtype`)."""
    return slow_channels_dir(base_dir) / f"{channel}.bin"


def spike_channel(base_dir, channel=None):
    """Path for the condensed spike data of a single channel (:func:`plx.export.ExportedSpike`)."""
    return spike_channels_dir(base_dir) / f"{channel}.bin"


def slow_channels_dir(base_dir, extension="bin"):
    """Path for the condensed slow waveform data directory."""
    return pathlib.Path(base_dir) / "slow_channels"


def spike_channels_dir(base_dir, extension="bin"):
    """Path for the condensed spike data directory."""
    return pathlib.Path(base_dir) / "spike_channels"
