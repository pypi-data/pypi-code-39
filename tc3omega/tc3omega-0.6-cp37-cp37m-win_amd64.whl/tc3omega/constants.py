#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yaml import safe_load, dump
from os import path, mkdir
import numpy as np

"""
This module is for loading the sample parameters/constants, it provides
options for:
    - loading sample data from a '.yml' file
    - entering sample data manually
"""


class Constants(object):
    def __init__(self, name, length, width, heater_dRdT, R_shunt, ds, Cvs,
                 layer_names, save_prompt,
                 cfg_dir="samples"):
        self.name = name_check(name)
        self.length = length
        self.b = width / 2
        self.heater_dRdT = heater_dRdT
        self.R_shunt = R_shunt
        self.ds = ds
        self.Cvs = Cvs
        self.layer_names = layer_names
        self.cfg_dir = cfg_dir

        if save_prompt:
            if path.exists(self.yaml_file_path()):
                print("* file '{}' already exists"
                      .format(self.yaml_file_path()))
                while True:
                    ans = input("* overwrite? [y/n]: ")
                    if ans in ['y', 'Y', 'yes', 'Yes']:
                        self.save_yaml_file()
                        print("saved current config")
                        break
                    elif ans in ['n', 'N', 'no', 'No']:
                        print("did NOT save current config")
                        break
                    else:
                        pass
            else:
                self.save_yaml_file()

    @classmethod
    def manualStart(cls):
        """MANUAL ENTRY"""
        print("* manual sample configuration")
        accept_parameters = False
        while not accept_parameters:
            print()
            name = input("    enter a name for dataset: ")
            length = float(input("    heater line length [m]: "))
            width = float(input("    heater line width [m]: "))
            heater_dRdT = float(input("    heater resistance change "
                                      "per unit temperature [Ohm/Kelvin]: "))
            R_shunt = float(input("    shunt resistance [Ohm]: "))
            num_layers = int(input("    number of layers to simulate "
                                   "(excluding heater): "))
            print()
            ds, Cvs, layer_names = [], [], []
            for i in range(num_layers):
                layer_name = input("    name for LAYER #{}: ".format(i + 1))
                d = float(input("    tickness [m] of LAYER #{}: "
                                .format(i + 1)))
                C = float(input("    heat capacity [J/m^3/K] of LAYER #{}: "
                                .format(i + 1)))

                ds.append(d)
                Cvs.append(C)
                layer_names.append(layer_name)
                print()

            # Asking user to confirm inputs
            print()
            print("    INPUTED PARAMETERS")
            print("    ------------------")
            print("    heater width: {} m".format(width))
            print("    heater length: {} m".format(length))
            print("    heater dRdT: {} Ohm/K".format(heater_dRdT))
            print("    shunt resistance: {} Ohms".format(R_shunt))
            print("    number of layers (excluding heater): {}"
                  .format(num_layers))
            print("    layer thicknesses (top to bottom; [m]): {}".format(ds))
            print("    layer heat capacities (top to bottom; [J/m^3/K]): {}"
                  .format(Cvs))
            print()

            while True:
                accept_string = input("* PROCEED? [y/n]: ")
                if accept_string in ['y', 'Y', 'yes', 'Yes']:
                    accept_parameters = True
                    break
                elif accept_string in ['n', 'N', 'no', 'No']:
                    break
                else:
                    pass
        return cls(name, length, width, heater_dRdT, R_shunt, ds, Cvs,
                   layer_names, save_prompt=True)

    @classmethod
    def fromFile(cls, file_path):
        """PROVIDE PARAMETERS IN A '.yml' FILE"""
        with open(file_path, 'r') as file:
            cfg = safe_load(file)

        name = cfg['general']['name']
        length = cfg['heater']['line_length']
        width = cfg['heater']['line_width']
        dRdT = cfg['heater']['dRdT']

        R_shunt = cfg['shunt_resistor']['R']

        ds = [cfg['layers'][x]['thickness'] for x in
              cfg['layers']]

        Cvs = [cfg['layers'][x]['heat_capacity'] for x in
               cfg['layers']]

        layer_names = [x for x in cfg['layers']]

        return cls(name, length, width, dRdT, R_shunt, ds, Cvs,
                   layer_names, save_prompt=False)

    def yaml_file_path(self):
        return "/".join([self.cfg_dir, self.name + ".yml"])

    def save_yaml_file(self):
        """WRITES  '.yml' FILE CONTAINING CURRENT SAMPLE CONFIG"""
        layers_dict = {}
        for i, layer_name in enumerate(self.layer_names):
            layers_dict[layer_name] = {'thickness': self.ds[i],
                                       'heat_capacity': self.Cvs[i]}

        data = {'general': {'name': self.name},
                'heater': {'line_length': self.length,
                           'line_width': 2 * self.b,
                           'dRdT': self.heater_dRdT},
                'shunt_resistor': {'R': self.R_shunt},
                'layers': layers_dict}

        try:
            mkdir(self.cfg_dir)
        except FileExistsError:
            pass

        with open(self.yaml_file_path(), 'w') as ymlfile:
            dump(data, ymlfile)
        return

    def getvals(self):
        return {'name': self.name,
                'length': self.length,
                'half_width': self.b,
                'heater_dRdT': self.heater_dRdT,
                'R_shunt': self.R_shunt,
                'd_values': np.array(self.ds, dtype=np.double),
                'Cv_values': np.array(self.Cvs, dtype=np.double),
                'layer_names': self.layer_names}


# ----------------------------------------------------------------------------
# GENERAL UTILITIES
# ----------------------------------------------------------------------------
def name_check(name):
    if name is None:
        return 'Untitled'
    elif type(name) is str:
        return name
    else:
        raise ValueError("'name' must be a string")
