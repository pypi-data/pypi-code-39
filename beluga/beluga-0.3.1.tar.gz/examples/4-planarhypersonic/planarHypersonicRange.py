"""Unconstrained planar hypersonic trajectory problem.
Entry flight-path angle is constrained so the vehicle enters
the atmosphere fairly steep. It performs a skip maneuver to
reach it's target."""
from math import *

import beluga
import logging

ocp = beluga.OCP('planarHypersonicRange')

# Define independent variables
ocp.independent('t', 's')


# Define equations of motion
ocp.state('h', 'v*sin(gam)', 'm')   \
   .state('theta', 'v*cos(gam)/r', 'rad')  \
   .state('v', '-D/mass - mu*sin(gam)/r**2', 'm/s') \
   .state('gam', 'L/(mass*v) + (v/r - mu/(v*r^2))*cos(gam)', 'rad')


# Define quantities used in the problem
ocp.quantity('rho', 'rho0*exp(-h/H)')
ocp.quantity('Cl', '(1.5658*alfa + -0.0000)')
ocp.quantity('Cd', '(1.6537*alfa^2 + 0.0612)')
ocp.quantity('D', '0.5*rho*v^2*Cd*Aref')
ocp.quantity('L', '0.5*rho*v^2*Cl*Aref')
ocp.quantity('r', 're+h')

# Define controls
ocp.control('alfa', 'rad')

# Define constants
ocp.constant('mu', 3.986e5*1e9, 'm^3/s^2')  # Gravitational parameter, m^3/s^2
ocp.constant('rho0', 0.001*1.2, 'kg/m^3')  # Sea-level atmospheric density, kg/m^3
ocp.constant('H', 7500, 'm')  # Scale height for atmosphere of Earth, m
ocp.constant('mass', 750/2.2046226, 'kg')  # Mass of vehicle, kg
ocp.constant('re', 6378000, 'm')  # Radius of planet, m
ocp.constant('Aref', pi*(24*.0254/2)**2, 'm^2')  # Reference area of vehicle, m^2
ocp.constant('h_0', 80000, 'm')
ocp.constant('v_0', 4000, 'm/s')
ocp.constant('gam_0', (-90+0.01)*pi/180, 'rad')
ocp.constant('h_f', 40000, 'm')
# ocp.constant('theta_f', 0, 'rad')

# Define costs
ocp.terminal_cost('-theta**2', 'rad**2')

# Define constraints
ocp.constraints() \
    .initial('h-h_0', 'm') \
    .initial('theta', 'rad') \
    .initial('v-v_0', 'm/s') \
    .initial('gam-gam_0', 'rad') \
    .terminal('h-h_f', 'm')  \
    # .terminal('theta-theta_f', 'rad')

ocp.scale(m='h', s='h/v', kg='mass', rad=1)

bvp_solver = beluga.bvp_algorithm('Shooting', num_arcs=16)

guess_maker = beluga.guess_generator(
    'auto',
    start=[40000, 0, 4000, (-90)*pi/180],
    direction='forward',
    costate_guess=-0.1
)

continuation_steps = beluga.init_continuation()

# Start by flying straight towards the ground
continuation_steps.add_step('bisection') \
                .num_cases(10) \
                .const('h_f', 35000)

# Slowly turn up the density
continuation_steps.add_step('bisection') \
                .num_cases(11) \
                .const('rho0', 0.1*1.2)

# Start by flying straight towards the ground
continuation_steps.add_step('bisection') \
                .num_cases(10) \
                .const('h_f', 30000)

# # Move downrange out a tad
# continuation_steps.add_step('bisection') \
#                 .num_cases(11) \
#                 .const('theta_f', 0.01*pi/180)
#
# # Bring flight-path angle up slightly to activate the control
# continuation_steps.add_step('bisection') \
#                 .num_cases(11) \
#                 .const('gam_0', -70*pi/180) \
#                 .const('theta_f', 0.5*pi/180)

# # Move downrange down a bit
# continuation_steps.add_step('bisection') \
#                 .num_cases(20) \
#                 .const('theta_f', 0.8*pi/180)

beluga.add_logger(logging_level=logging.DEBUG)

sol_set = beluga.solve(
    ocp=ocp,
    method='indirect',
    bvp_algorithm=bvp_solver,
    steps=continuation_steps,
    guess_generator=guess_maker
)

sol = sol_set[-1][-1]

import matplotlib.pyplot as plt
plt.plot(sol.y[:,1], sol.y[:,0])
plt.show()

plt.plot(sol.y[:,2], sol.y[:,0])
plt.show()

plt.plot(sol.t, sol.dual[:,2])
plt.show()
