
# coding: utf-8

# In[1]:


import os
import sys



# general import for smrt
from smrt import make_snowpack, make_model, sensor_list
import numpy as np


def get_model(args):
	if agrs.optimize:
		model = make_model("oiba", "odort")
	else:
		model = make_model("iba", "dort")
	return model


def setup_shs_snowpack(nlyr=40):

	assert nlyr % 2 == 0

	tau = 0.16

	density_range = np.arange(30, 510, 150)

	r_shs = 0.58 * 0.5e-3
	thickness = np.full(nlyr, 0.1)

	snowpack_shs = [make_snowpack(thickness, "sticky_hard_spheres", density=[x, x/2]*(nlyr//2), temperature=[265]*nlyr, radius=r_shs, stickiness=tau) for x in density_range]
	return snowpack_shs


def setup_exp_snowpack(nlyr=40):

	assert nlyr % 2 == 0

	density_range = np.arange(30, 510, 150)

	l_exp = 0.58 * 0.5e-3

	thickness = np.full(nlyr, 0.1)

	snowpack_exp = [make_snowpack(thickness, "exponential", density=[x, x/2]*(nlyr//2), temperature=[265]*nlyr, corr_length=l_exp) for x in density_range]
	return snowpack_exp

