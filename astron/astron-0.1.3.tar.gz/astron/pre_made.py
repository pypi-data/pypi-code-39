import pygame
import os, sys
import math
import numpy as np
sys.path.append('./')
from game import *

# lines = 0
# files = ['assests', 'game', 'scene', 'utilities']
# for file in files:
#         f = open(r'./astron/' + file + '.py', 'r').read()
#         lines += f.count('\n')
# print(lines)

screen_x, screen_y = 1920, 1080
modpath = os.path.abspath(os.path.split(sys.argv[0])[0])

############# LEVEL 1 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 2000)
orbit = Orbit(a=500, b=500, center_x=screen_x, center_y=screen_y/2, CW=True, angular_step = 2*np.pi/(200.0), progress = np.pi/4)
planet = Planet('Test', mass = 2e16, orbit = orbit)
level1 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([0,0], [screen_x, 0]), win_velocity = 90.0,
           background = (0.0, 0.0, 0.0)
)

############# LEVEL 2 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 500)
orbit = Orbit(a=1000, b=800, center_x=screen_x/2, center_y=0.0, CW=False, angular_step = 2*np.pi/(200.0), progress = np.pi*0.9)
planet = Planet('Test', mass = 4e16, orbit = orbit, color = (100,0,0))
level2 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([screen_x,0], [screen_x, screen_y/10]), win_velocity = 90.0,
           background = modpath + '\images\stars_1.jpg'
)

############# LEVEL 3 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 800)
orbit = Orbit(a=800, b=300, center_x=screen_x*0.75, center_y=screen_x*0.25, CW=True, angular_step = 2*np.pi/(200.0), progress = np.pi/3)
planet = Planet('Test', mass = 4e16, orbit = orbit, color = (245, 66, 239))
level3 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet], win_region = ([0,0], [0, screen_y/5]), win_velocity = 190.0,
           background = modpath + '\images\stars_2.jpg'
)

############# LEVEL 4 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 3000, gas_level = 225)

orbit = Orbit(a=800, b=800, center_x=0.0, center_y=3*screen_y/4, CW=False, angular_step = np.pi/(200.0), progress = 0.0)
planet = Planet('Test', mass = 5e16, orbit = orbit, color = (48, 227, 240))

orbit2 = Orbit(a=800, b=800, center_x=screen_x, center_y=screen_y/2, CW=True, angular_step = 3*np.pi/(200.0), progress = np.pi/2)
planet2 = Planet('Test', mass = 5e16, orbit = orbit2, color=(240, 217, 43))

level4 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet, planet2], win_region = ([screen_x,0], [screen_x, screen_y/7]), win_velocity = 180,
           background = modpath + '\images\stars_3.jpg'
)

############# LEVEL 5 #############

sc = Spacecraft('Test', mass = 100, thrust_force = 5000, gas_level = 250)

orbit = Orbit(a=800, b=800, center_x=0.0, center_y=3*screen_y/4, CW=False, angular_step = np.pi/(200.0), progress = 0.0)
planet = Planet('Test', mass = 5e16, orbit = orbit)

orbit2 = Orbit(a=800, b=800, center_x=screen_x+100, center_y=screen_y/2, CW=True, angular_step = 3*np.pi/(200.0), progress = np.pi/2)
planet2 = Planet('Test', mass = 10e16, orbit = orbit2)

level5 = GameScene(resolution = (screen_x, screen_y), sc=sc, planets=[planet, planet2], 
                   win_region = ([screen_x*0.75,0], [screen_x*0.9, 0.0]),
                   win_velocity = 100,
           background = modpath + '\images\stars_4.jpg'
)
##################################

game = Game(scenes = [
        level1, 
        level2, 
        level3, 
        level4,
        level5
        ], fullscreen=True, fps=60)

# game.startGame(splash=True)