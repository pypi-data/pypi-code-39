import os

import numpy as np

from hwaves.hwf_density import cartesian_density, pack_cartesian_data, write_cartesian
from hwaves.hwf import radial_wf_integral

tests_path = os.path.join(os.getcwd(),'tests')

nx = 30
ny = 30
nz = 30
dx = 0.1
dy = 0.1
dz = 0.1

def test_cartesian_density():

    x, y, z, PV = cartesian_density(1,0,0,nx,ny,nz,dx,dy,dz)
    ijk_xyz_PV = pack_cartesian_data(x,y,z,PV)
    fpath = os.path.join(tests_path,'cartesian_density_1s.dat')
    write_cartesian(ijk_xyz_PV,fpath)
    #assert(os.path.exists(fpath))

def test_wf_integrals():
    r_A = np.linspace(0.,50.,1000)
    for n in range(1,4):
        for l in range(0,n):
            integ = radial_wf_integral(n,l,r_A)
            print('density integral for n={},l={}: {}'.format(n,l,integ))

