import numpy
import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import lal
import lalsimulation
from lal.lal import PC_SI as LAL_PC_SI
import h5py
import warnings
warnings.filterwarnings('ignore')
#import seaborn as sns
#sns.set(style="whitegrid")
import matplotlib.pylab as pylab
plot_params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 9),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(plot_params)
from mpl_toolkits.mplot3d import axes3d
import random
import scipy.interpolate

# Calculating the projection of complex vector v on complex vector u
def proj(u, v):
    # notice: this algrithm assume denominator isn't zero
    return u * numpy.vdot(v,u) / numpy.vdot(u,u) 

# Calculating the normalized residual (= a new basis) of a vector vec from known bases
def gram_schmidt(bases, vec):
    for i in numpy.arange(0,len(bases)):
        vec = vec - proj(bases[i], vec)
    return vec/numpy.sqrt(numpy.vdot(vec,vec)) # normalized new basis

# Calculating overlap of two waveforms
def overlap_of_two_waveforms(wf1, wf2):
    wf1norm = wf1/numpy.sqrt(numpy.vdot(wf1,wf1)) # normalize the first waveform
    wf2norm = wf2/numpy.sqrt(numpy.vdot(wf2,wf2)) # normalize the second waveform
    diff = wf1norm - wf2norm
    #overlap = 1 - 0.5*(numpy.vdot(diff,diff))
    overlap = numpy.real(numpy.vdot(wf1norm, wf2norm))
    return overlap

def spherical_to_cartesian(sph):
    x = sph[0]*numpy.sin(sph[1])*numpy.cos(sph[2])
    y = sph[0]*numpy.sin(sph[1])*numpy.sin(sph[2])
    z = sph[0]*numpy.cos(sph[1])
    car = [x,y,z]
    return car

def get_m1m2_from_mcq(mc,q):
    m2 = mc * q ** (-0.6) * (1+q)**0.2
    m1 = m2 * q
    return numpy.array([m1,m2])

def generate_a_waveform(m1,m2,spin1,spin2,iota,phiRef,deltaF,f_min,f_max,ecc):
    test_mass1 = m1 * lal.lal.MSUN_SI
    test_mass2 = m2 * lal.lal.MSUN_SI
    [plus_test, cross_test]=lalsimulation.SimInspiralChooseFDWaveform(test_mass1, test_mass2, 0, 0, spin1[2], 0, 0, spin2[2], distance, iota, phiRef, 0, ecc, 0, deltaF, f_min, f_max, 0, waveFlags, approximant)
    hp = plus_test.data.data
    print "hp", len(hp)
    hp_test = hp#[numpy.int(f_min/deltaF):numpy.int(f_max/deltaF)]
    length = numpy.int((f_max-f_min)/1)
    print length,f_max
    return hp_test

def generate_a_waveform_from_mcq(mc,q,spin1,spin2,iota, phiRef):
    m1,m2 = get_m1m2_from_mcq(mc,q)
    test_mass1 = m1 * lal.lal.MSUN_SI
    test_mass2 = m2 * lal.lal.MSUN_SI
    [plus_test, cross_test]=lalsimulation.SimInspiralChooseFDWaveform(test_mass1, test_mass2, spin1[0], spin1[1], spin1[2], spin2[0], spin2[1], spin2[2], distance, iota, phiRef, 0, 0, 0, deltaF, f_min, f_max, 0, waveFlags, approximant)
    hp = plus_test.data.data
    hp_test = hp[numpy.int(f_min/deltaF):numpy.int(f_max/deltaF)]
    return hp_test

def generate_params_points(npts,nparams):
    global mc_low, mc_high, q_low, q_high, s1sphere_low, s1sphere_high, s2sphere_low, s2sphere_high, iota_low, iota_high, phiref_low, phiref_high
    params_min = [mc_low, q_low, s1sphere_low[0], s1sphere_low[1], s1sphere_low[2], s2sphere_low[0], s2sphere_low[1], s2sphere_low[2], iota_low, phiref_low] 
    params_max = [mc_high, q_high, s1sphere_high[0], s1sphere_high[1], s1sphere_high[2], s2sphere_high[0], s2sphere_high[1], s2sphere_high[2], iota_high, phiref_high]
    paramspoints = numpy.random.uniform(params_min, params_max, size=(npts,nparams))
    paramspoints = paramspoints.round(decimals=6)
    return paramspoints

# needs to be written but will not be used for roq construction
# for surrogate modeling
def generate_fixed_uniform_params_points(npts, nparams):
    global mc_low, mc_high, q_low, q_high, s1sphere_low, s1sphere_high, s2sphere_low, s2sphere_high, iota_low, iota_high, phiref_low, phiref_high
    x = np.linspace(mc_low, mc_high, npts)
    y = np.linspace(q_low, q_high, npts)
    z = np.linspace(s1_low[2], s1_high[2], npts)
    p = np.linspace(s2_low[2], s2_high[2], npts)
    ##x = np.linspace(8.9, 9.1, npts)
    ##y = np.linspace(1.9, 2.1, npts)
    ##z = np.linspace(0.0, 0.0, npts)
    ##p = np.linspace(0.0, 0.0, npts)
    xv, yv, zv, pv = np.meshgrid(x, y, z, p)
    paramspoints = np.vstack((xv.flatten(), yv.flatten(), zv.flatten(), pv.flatten())).T    
    paramspoints = paramspoints.round(decimals=6)
    return paramspoints

# now generating N=npts waveforms at points that are 
# randomly uniformly distributed in parameter space
# and calculate their inner products with the 1st waveform
# so as to find the best waveform as the new basis
def least_match_waveform_unnormalized(paramspoints, known_bases, npts):
    overlaps = numpy.zeros(npts)
    modula = numpy.zeros(npts)
    for i in numpy.arange(0,len(paramspoints)):
        global deltaF, distance, waveFlags, approximant
        paramspoint = paramspoints[i]
        m1, m2 = get_m1m2_from_mcq(paramspoint[0],paramspoint[1])
        s1x, s1y, s1z = spherical_to_cartesian(paramspoint[2:5]) 
        s2x, s2y, s2z = spherical_to_cartesian(paramspoint[5:8]) 
        iota=paramspoint[8]  
        phiRef=paramspoint[9]
        f_ref = 0 
        RA=0    
        DEC=0   
        psi=0   
        phi=0   
        m1 *= lal.lal.MSUN_SI
        m2 *= lal.lal.MSUN_SI
        [plus,cross]=lalsimulation.SimInspiralChooseFDWaveform(m1, m2, s1x, s1y, s1z, s2x, s2y, s2z, distance, iota, phiRef, 0, 0, 0, deltaF, f_min, f_max, f_ref, waveFlags, approximant)
        hp_tmp = plus.data.data[numpy.int(f_min/deltaF):numpy.int(f_max/deltaF)] # data_tmp is hplus and is a complex vector 
        residual = hp_tmp
        for k in numpy.arange(0,len(known_bases)):
            residual -= proj(known_bases[k],hp_tmp)
        modula[i] = numpy.sqrt(numpy.vdot(residual, residual))
    arg_newbasis = numpy.argmax(modula)    
    mass1, mass2 = get_m1m2_from_mcq(paramspoints[arg_newbasis][0],paramspoints[arg_newbasis][1])
    mass1 *= lal.lal.MSUN_SI
    mass2 *= lal.lal.MSUN_SI
    sp1x, sp1y, sp1z = spherical_to_cartesian(paramspoints[arg_newbasis,2:5]) 
    sp2x, sp2y, sp2z = spherical_to_cartesian(paramspoints[arg_newbasis,5:8]) 
    inclination = paramspoints[arg_newbasis][8]
    phi_ref = paramspoints[arg_newbasis][9]
    [plus_new, cross_new]=lalsimulation.SimInspiralChooseFDWaveform(mass1, mass2, sp1x, sp1y, sp1z, sp2x, sp2y, sp2z, distance, inclination, phi_ref, 0, 0, 0, deltaF, f_min, f_max, 0, waveFlags, approximant)
    hp_new = plus_new.data.data
    hp_new = hp_new[numpy.int(f_min/deltaF):numpy.int(f_max/deltaF)]
    basis_new = gram_schmidt(known_bases, hp_new)
    ##return numpy.array([basis_new, hp_new, paramspoints[arg_newbasis], modula[arg_newbasis]]) # elements, basis waveforms, masses, residual modula
    return numpy.array([basis_new, paramspoints[arg_newbasis], modula[arg_newbasis]]) # elements, masses&spins, residual mod


def least_match_quadratic_waveform_unnormalized(paramspoints, known_quad_bases, npts):
    overlaps = numpy.zeros(npts)
    modula = numpy.zeros(npts)
    for i in numpy.arange(0,len(paramspoints)):
        global deltaF, distance, waveFlags, approximant
        paramspoint = paramspoints[i]
        m1, m2 = get_m1m2_from_mcq(paramspoint[0],paramspoint[1])
        s1x, s1y, s1z = spherical_to_cartesian(paramspoint[2:5]) 
        s2x, s2y, s2z = spherical_to_cartesian(paramspoint[5:8]) 
        iota=paramspoint[8]  
        phiRef=paramspoint[9]
        f_ref = 0 
        RA=0    
        DEC=0   
        psi=0   
        phi=0   
        m1 *= lal.lal.MSUN_SI
        m2 *= lal.lal.MSUN_SI
        [plus,cross]=lalsimulation.SimInspiralChooseFDWaveform(m1, m2, s1x, s1y, s1z, s2x, s2y, s2z, distance, iota, phiRef, 0, 0, 0, deltaF, f_min, f_max, f_ref, waveFlags, approximant)
        hp_tmp = plus.data.data[numpy.int(f_min/deltaF):numpy.int(f_max/deltaF)] # data_tmp is hplus and is a complex vector 
        hp_quad_tmp = (numpy.absolute(hp_tmp))**2
        residual = hp_quad_tmp
        for k in numpy.arange(0,len(known_quad_bases)):
            residual -= proj(known_quad_bases[k],hp_quad_tmp)
        modula[i] = numpy.sqrt(numpy.vdot(residual, residual))
    arg_newbasis = numpy.argmax(modula)    
    mass1, mass2 = get_m1m2_from_mcq(paramspoints[arg_newbasis][0],paramspoints[arg_newbasis][1])
    mass1 *= lal.lal.MSUN_SI
    mass2 *= lal.lal.MSUN_SI
    sp1x, sp1y, sp1z = spherical_to_cartesian(paramspoints[arg_newbasis,2:5]) 
    sp2x, sp2y, sp2z = spherical_to_cartesian(paramspoints[arg_newbasis,5:8]) 
    inclination = paramspoints[arg_newbasis][8]
    phi_ref = paramspoints[arg_newbasis][9]
    [plus_new, cross_new]=lalsimulation.SimInspiralChooseFDWaveform(mass1, mass2, sp1x, sp1y, sp1z, sp2x, sp2y, sp2z, distance, inclination, phi_ref, 0, 0, 0, deltaF, f_min, f_max, 0, waveFlags, approximant)
    hp_new = plus_new.data.data
    hp_new = hp_new[numpy.int(f_min/deltaF):numpy.int(f_max/deltaF)]
    hp_quad_new = (numpy.absolute(hp_new))**2
    basis_quad_new = gram_schmidt(known_quad_bases, hp_quad_new)    
    ##return numpy.array([basis_new, hp_new, paramspoints[arg_newbasis], modula[arg_newbasis]]) # elements, basis waveforms, masses, residual modula
    return numpy.array([basis_quad_new, paramspoints[arg_newbasis], modula[arg_newbasis]]) # elements, masses&spins, residual mod

def bases_searching_results_unnormalized(npts, nparams, nbases, known_bases, basis_waveforms, params, residual_modula):
    for k in numpy.arange(0,nbases-1):
        print "Linear Iter: ", k
        params_points = generate_params_points(npts, nparams)
        ##basis_new, hp_new, params_new, rm_new = least_match_waveform_unnormalized(params_points, known_bases, npts)
        basis_new, params_new, rm_new= least_match_waveform_unnormalized(params_points, known_bases, npts)
        known_bases= numpy.append(known_bases, numpy.array([basis_new]), axis=0)
        ##basis_waveforms = numpy.append(basis_waveforms, numpy.array([hp_new]), axis=0)
        params = numpy.append(params, numpy.array([params_new]), axis = 0)
        residual_modula = numpy.append(residual_modula, rm_new)
    ##return known_bases, basis_waveforms, params, residual_modula
    return known_bases, params, residual_modula

def bases_searching_quadratic_results_unnormalized(npts, nparams, nbases_quad, known_quad_bases, basis_waveforms, params_quad, residual_modula):
    for k in numpy.arange(0,nbases_quad-1):
        print "Quadratic Iter: ", k
        params_points = generate_params_points(npts, nparams)
        basis_new, params_new, rm_new= least_match_quadratic_waveform_unnormalized(params_points, known_quad_bases, npts)
        known_quad_bases= numpy.append(known_quad_bases, numpy.array([basis_new]), axis=0)
        params_quad = numpy.append(params_quad, numpy.array([params_new]), axis = 0)
        residual_modula = numpy.append(residual_modula, rm_new)
    ##return known_bases, basis_waveforms, params, residual_modula
    return known_quad_bases, params_quad, residual_modula

def calculate_surrogate_waveform(test_params, mc_low, mc_high, q_low, q_high, interpts, nparams, emp_nodes, V, solver, smooth):
    test_mass1_Msun = test_params[0]
    test_mass2_Msun = test_params[1]
    test_spin1z = test_params[2]
    test_spin2z = test_params[3]
    paramspoints_interp = generate_fixed_uniform_params_points(interpts, nparams)
    mass1_interp = numpy.zeros(len(paramspoints_interp))
    mass2_interp = numpy.zeros(len(paramspoints_interp))
    for k in numpy.arange(0,interpts):
        mass1_interp[k], mass2_interp[k] = get_m1m2_from_mcq(paramspoints_interp[k,0],paramspoints_interp[k,1]) 
    s1z_interp = paramspoints_interp[:,2]
    s2z_interp = paramspoints_interp[:,3]
    print "mmmmmmm", len(mass2_interp), len(s1z_interp)

    cis = numpy.zeros((mass1_interp.size, len(emp_nodes))) + numpy.zeros((mass1_interp.size, len(emp_nodes)))*1j
    inverse_V = numpy.linalg.inv(V)
    for i in numpy.arange(0, len(paramspoints_interp)):
        m1, m2 = get_m1m2_from_mcq(paramspoints_interp[i,0], paramspoints_interp[i,1])
        m1 *= lal.lal.MSUN_SI
        m2 *= lal.lal.MSUN_SI
        sp1z = paramspoints_interp[i,2]
        sp2z = paramspoints_interp[i,3]
        [plus_start, cross_start]=lalsimulation.SimInspiralChooseFDWaveform(m1, m2, 0, 0, sp1z, 0, 0, sp2z, distance, 0, 0, 0, 0, 0, deltaF, f_min, f_max, 0, waveFlags, approximant)
        hp_interp = plus_start.data.data
        hp_interp = hp_interp[numpy.int(f_min/deltaF):numpy.int(f_max/deltaF)]
        if solver is 'solve':
            Ci = numpy.linalg.solve(V, hp_interp[emp_nodes])
        elif solver is 'inv':
            Ci = numpy.dot(inverse_V, hp_test[emp_nodes])
        cis[i] = Ci
        interpolant_rep = numpy.zeros(len(hp_interp))+numpy.zeros(len(hp_interp))*1j
        for j in numpy.arange(0, ndim):
            tmp = numpy.multiply(Ci[j], known_bases[j])
            interpolant_rep += tmp
        diff_rep = (interpolant_rep - hp_interp)/numpy.sqrt(numpy.vdot(hp_interp,hp_interp))
    zsplines = numpy.zeros(len(emp_nodes)) + numpy.zeros(len(emp_nodes))*1j
    for j in numpy.arange(0, len(emp_nodes)):
        zz = cis[:,j]
        spline = scipy.interpolate.Rbf(mass1_interp,mass2_interp,s1z_interp,s2z_interp,zz,function=smooth,smooth=5, episilon=5)
        m1_test = numpy.array([test_mass1_Msun])
        m2_test = numpy.array([test_mass2_Msun])
        sp1z_test = numpy.array([test_spin1z])
        sp2z_test = numpy.array([test_spin2z])
        B1, B2, B3, B4 = numpy.meshgrid(m1_test, m2_test, sp1z_test, sp2z_test, indexing='xy')
        zspline = numpy.zeros((m1_test.size, m1_test.size)) + numpy.zeros((m1_test.size, m1_test.size))*1j
        zspline = spline(B1,B2,B3,B4)
        zsplines[j] = zspline[0]
        interpolant = numpy.zeros(len(known_bases[0]))+numpy.zeros(len(known_bases[0]))*1j
    for j in numpy.arange(0, ndim):
        tmp = numpy.multiply(zsplines[j], known_bases[j])
        interpolant += tmp
    return interpolant

def calculate_surrogate_error(test_params, mc_low, mc_high, q_low, q_high, interpts, emp_nodes, V, solver, smooth):
    test_mass1_Msun, test_mass2_Msun = get_m1m2_from_mcq(test_params[0], test_params[1])
    spin1 = [0, 0, test_params[2]]
    spin2 = [0, 0, test_params[3]]    
    hp_test = generate_a_waveform(test_mass1_Msun,test_mass2_Msun,spin1,spin2)
    interpolant = calculate_surrogate_waveform(test_params, mc_low, mc_high, q_low, q_high, interpts, emp_nodes, V, solver, smooth)
    overlap = overlap_of_two_waveforms(hp_test, interpolant)
    rep_error = 2*(1-overlap)
    suro_error = 1-overlap
    return suro_error

nparams = 10
mc_low = 20 #7.932707
mc_high = 50.0  #14.759644
q_low = 6
q_high = 18
s1sphere_low = [0, 0, 0]
s1sphere_high = [0.9, numpy.pi, 2.0*numpy.pi]
s2sphere_low = [0, 0, 0]
s2sphere_high = [0.9, numpy.pi, 2.0*numpy.pi]
iota_low = 0
iota_high = numpy.pi
phiref_low = 0
phiref_high = 2*numpy.pi
f_min = 20
f_max = 1024
deltaF = 0.25

npts = 300
nbases = 500
distance = 10 * LAL_PC_SI * 1.0e6 #* 1e-20 # 10 Mpc is default, now move closer by 1e-20 
waveFlags=lal.CreateDict()
approximant = lalsimulation.IMRPhenomPv2

freq= numpy.arange(f_min,f_max,deltaF)



