#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 23:02:08 2019

@author: ncs
"""
import logging
import pandas as pd
import numpy as np
from .utils import ParamFile

def read_weather_inputs(path_to_weather_file):
    """Read from weather input file to populate the dataframe"""
    logging.debug("  Reading weather")
    w = np.loadtxt(
        path_to_weather_file,
        delimiter="\t",
        comments="%",
        dtype={
            "names": (
                "day",
                "month",
                "year",
                "minTemp",
                "maxTemp",
                "Precipitation",
                "ReferenceET",
            ),
            "formats": ("i", "i2", "i4", "f8", "f8", "f8", "f8"),
        },
    )
    weather = pd.DataFrame(w)
    return weather

class Soil(ParamFile):
    """Soil class. Sub-class of ParamFile, only defined here to initialize
    self.composition inside of __init__"""

    def __init__(self, in_dir, soil_file, soil_profile_file):
        logging.debug("  Reading soil")
        super().__init__(in_dir + soil_file)
        self.composition = None
        self.source_file = soil_file
        self._read_layers(in_dir + soil_profile_file)

    def _read_layers(self, path_to_soil_profile_file):
        profile = np.loadtxt(
            path_to_soil_profile_file,
            delimiter="\t",
            comments="%",
            dtype={"names": ("soil", "dz", "type"), "formats": ("i", "f4", "i")},
        )
        layers = pd.DataFrame(profile)
        layers["dzsum"] = layers.dz.cumsum()
        self.composition = layers
        return self


class Crops:
    """For this model, there are 2 top level parameters and one or
    more Crops.

    The Crops object is the container for the crop information.
    Each crop has an associated name and several parameter files.
    """

    # TODO: this should only raise Not implemented Error
    # It should not be part of the software. It should be implemented by users

    def __init__(self, calendar_file, crops=None, ):
        self.calendar = self.read_planting_calendar(calendar_file)
        self.crop_collection = {}
        if crops is None:
            self.crop_collection['Quinoa'] = Crop(
            "./Input/Quinoa.txt",
            "./Input/IrrigationManagement.txt",
            "./Input/IrrigationSchedule.txt",
            )
        else:
            assert(type(crops) is dict)
            self.crop_collection = crops

        self.nCrops = len(self.crop_collection)
        self.rotation = (self.nCrops > 1)

    def read_planting_calendar(self, cal_file):
        """Read planting calendar into a pandas dataframe with header"""
        planting_calendar = pd.read_csv(
            cal_file,
            infer_datetime_format=True,
            comment="%",
            sep="\t",
            parse_dates=True,
        )
        return planting_calendar


class Crop(ParamFile):
    """Crop objects contain the modeling information about a Crop"""

    def __init__(self, input_file, irrigation_file, irrigation_schedule):
        super().__init__(input_file)

        # In AquaCrop, each crop struct has 89 fields of varying types
        # Should we do the same here?
