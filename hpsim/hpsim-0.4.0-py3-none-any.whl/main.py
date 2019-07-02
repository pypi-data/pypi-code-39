#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:39:28 2019

@author: hogbobson
"""

import numpy as np
from . import force
from . import miscfuncs
from . import solver
from . import ntgrtr
from . import ensgen
from . import timestep
from . import timegen
from . import visual
from . import energy



def main(          ensemble_generator = ensgen.solar_system  ,
                   integration_func = ntgrtr.n_squared              , 
                   solver_func = solver.sym2                        , 
                   wanted_forces = [force.gravity]                  , 
                   plot_func = visual.simple_2d_anim                   ,
                   plot_save = False                                ,
                   energy_func = energy.no_energy                   ,   
                   time_start = 0                                   , 
                   time_step = timestep.constant_dt(100000)         , 
                   time_end = timegen.time_years(1)
                   ):

    everything = {
            'ensemble': ensemble_generator()    ,
            'integrator': integration_func      ,
            'solver': solver_func               ,
            'forces': wanted_forces             ,
            'plotter': plot_func                ,
            'time start': time_start            ,
            'current time': time_start          ,
            'dt': time_step                     ,
            'time end': time_end                ,
            'time steps': 0                     ,
            'plot output': None
            }
    
    #I put everything here that isn't changed for readability.
    integrator = everything['integrator']
    solver     = everything['solver']
    forces     = everything['forces']
    
    while everything['current time'] < everything['time end']:
        integrator(everything['ensemble'])
        solver(everything['ensemble'], everything['dt'], forces)
        everything['current time'] += everything['dt']
        everything['time steps'] += 1
        everything['ensemble']['r data'] = np.append( \
                  everything['ensemble']['r data'], 
                  np.reshape(everything['ensemble']['r'], \
                        (everything['ensemble']['number of objects'], \
                         3,1)), axis = 2)
    
    everything['plot output'] = plot_func(everything)

    return everything