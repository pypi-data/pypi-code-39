"""A collection of methods that aim to make calculations around passive electronic networks like resonant circuits, filters, or resistor networks, easier."""

__license__ = """
Python RLC Tools

Written in 2019 by Adrian Schlarb <admin-pypi@sotai.tk>

To the extent possible under law, the author(s) have dedicated all copyright and
related and neighboring rights to this software to the public domain worldwide.
This software is distributed without any warranty.

You should have received a copy of the CC0 Public Domain Dedication along with
this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 
"""

__version__ = "0.1.1"

from math import pi,sqrt
	
	
def f0(L, C):
	"""Returns the resonant frequency of an RLC circuit with inductance L and capacitance C."""
	return(1/(2*pi*sqrt(L*C)))

def LC(freq):
	"""Returns the product of inductance and capacitance in an RLC circuit necessary for resonance at a frequency freq."""
	return(1/(2*pi*freq)**2)
	
	

def tc_RC(R, C):
	"""Returns the time constant of a resistor-capacitor circuit."""
	return(R*C)

def tc_RL(R, L):
	"""Returns the time constant of a resistor-inductor circuit."""
	return(R/L)
	
	

def period(freq):
	"""Returns the period of a wave with a frequency of freq."""
	return(1/freq)

def frequency(per):
	"""Returns the frequency of a wave with a period of per."""
	return(1/per)
	
	

def X_C(C, freq):
	"""Returns the reactance of a capacitor C at a frequency f."""
	return(1/(2*pi*freq*C))

def X_L(L, freq):
	"""Returns the reactance of an inductor L at a frequency f."""
	return(2*pi*freq*L)

def Z_C(C, freq):
	"""Returns the impedance of a capacitor C at a frequency f."""
	return(-1j*X_C(C, freq))

def Z_L(L, freq):
	"""Returns the impedance of an inductor L at a frequency f."""
	return(1j*X_L(L, freq))
	
	

def harmonic_sum(value0, value1, *more_values):
	"""Returns the 'harmonic sum', or the reciprocal of the sum of reciprocals, of 2 or more values."""
	recip_sum = 0
	
	recip_sum += 1/value0
	recip_sum += 1/value1
	
	for value in more_values:
		recip_sum += 1/value
	
	return(1/recip_sum)
