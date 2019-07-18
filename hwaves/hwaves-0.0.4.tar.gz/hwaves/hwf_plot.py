import os

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from mayavi import mlab
from skimage import measure

from .hwf import spherical_harmonic, radial_probability
from .hwf_density import real_wf_cartesian_density, cartesian_density

bohr_rad_A = 0.529177       #Angstrom
elec_mass_amu = 5.485799090 #amu

def plot_spherical_harmonic(l,m,th,ph,showplot=False):
    #
    # th and ph can be meshgrids
    #
    Ylm = spherical_harmonic(l,m,th,ph)
    sph_amp = np.abs(Ylm * np.conj(Ylm))
    #sph_amp = np.real(Ylm)
    x_amp = sph_amp * np.sin(ph) * np.cos(th)
    y_amp = sph_amp * np.sin(ph) * np.sin(th)
    z_amp = sph_amp * np.cos(ph)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.plot_surface(x_amp, y_amp, z_amp,
    rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
    linewidth=0, antialiased=False, alpha=0.5)
    if showplot:
        plt.show()
    return fig

def plot_radial_wf(n,l,r_A,Z=1,N_neut=0,showplot=False):
    #
    # r_A is an array
    #
    Rnl,Rnlsqr,Pnl = radial_probability(n,l,r_A,Z,N_neut)

    fig = plt.figure()
    #plt = fig.gca()
    plt.plot(Z*r_A,Rnl)
    plt.xlabel('Z*r (Angstrom)')
    #ax.set_ylabel('Rnl')

    #fig = plt.figure()
    #ax = fig.gca()
    plt.plot(Z*r_A,Rnlsqr)
    #ax.set_xlabel('Z*r (Angstrom)')
    #ax.set_ylabel('Rnl**2')

    #fig = plt.figure()
    #ax = fig.gca()
    plt.plot(Z*r_A,Pnl)
    #ax.set_xlabel('Z*r (Angstrom)')
    #ax.set_ylabel('Pnl')
    plt.legend(['Rnl [A^(-3/2)]','Rnl**2 [A^-3]','Pnl [A^-1]'])
    if showplot:
        plt.show()
    return fig

    #nx = 80
    #ny = 80
    #nz = 80
    #dx = 0.2
    #dy = 0.2
    #dz = 0.2

def plot_isosurface(n,l,m,nx,ny,nz,dx,dy,dz,isolevel=None,Z=1,N_neut=0,showplot=False):
    x_grid,y_grid,z_grid,PV = cartesian_density(n,l,m,nx,ny,nz,dx,dy,dz,Z,N_neut)
    if not isolevel:
        isolevel = 0.3*np.max(PV)
    plot_isosurf(PV,isolevel,dx,dy,dz,showplot)

def plot_real_wf_isosurface(n,l,absm,plusminus,nx,ny,nz,dx,dy,dz,isolevel=None,Z=1,N_neut=0,showplot=False):
    x_grid,y_grid,z_grid,PV = real_wf_cartesian_density(n,l,absm,plusminus,nx,ny,nz,dx,dy,dz,Z,N_neut)
    if not isolevel:
        isolevel = 0.3*np.max(PV)
    plot_isosurf(PV,isolevel,dx,dy,dz,showplot)

def write_real_wf_isosurface(obj_file_path,n,l,absm,plusminus,nx,ny,nz,dx,dy,dz,isolevel=None,Z=1,N_neut=0):
    x_grid,y_grid,z_grid,PV = real_wf_cartesian_density(n,l,absm,plusminus,nx,ny,nz,dx,dy,dz,Z,N_neut)
    verts, faces, norms, vals = measure.marching_cubes_lewiner(PV, isolevel, spacing=(dx,dy,dz))   
    with open(obj_file_path,'w') as objf:
        objf.write('mtllib test.mtl\n')
        objf.write('# VERTICES\n')
        vmeanx = np.mean(verts[:,0]) 
        vmeany = np.mean(verts[:,1]) 
        vmeanz = np.mean(verts[:,2]) 
        for v in verts:
            objf.write('v {:.4f} {:.4f} {:.4f} 1.\n'.format(v[0]-vmeanx,v[1]-vmeany,v[2]-vmeanz))
        # We may want to define textures at some point
        #objf.write('# TEXTURE COORDINATES\n')
        #objf.write('vt 0.3 0.5\n')
        #objf.write('vt 0.6 0.5\n')
        #objf.write('vt 0.9 0.5\n')
        #vert_tx_map = [] 
        #for iv in range(len(verts)):
        #    vert_tx_map.append(np.mod(iv,3)+1)
        objf.write('# VERTEX NORMALS\n')
        for vn in norms:
            objf.write('vn {:.4f} {:.4f} {:.4f}\n'.format(vn[0],vn[1],vn[2]))
        objf.write('usemtl test\n')
        objf.write('# FACES\n')
        for f in faces:
            fpp = f+1
            objf.write('f {}//{} {}//{} {}//{}\n'.format(fpp[0],fpp[0],fpp[1],fpp[1],fpp[2],fpp[2]))
            #objf.write('f {}/1/{} {}/2/{} {}/3/{}\n'.format(f[0],f[0],f[1],f[1],f[2],f[2]))
            #objf.write('f {}/{}/{} {}/{}/{} {}/{}/{}\n'.format(
            #    fpp[0],vert_tx_map[f[0]],fpp[0],
            #    fpp[1],vert_tx_map[f[1]],fpp[1],
            #    fpp[2],vert_tx_map[f[2]],fpp[2]))

def get_isosurf_geometry(PV,isolevel,dx,dy,dz):
    #print('range of PV: {} to {}'.format(np.min(PV),np.max(PV)))
    #print('isolevel: {}'.format(isolevel))
    verts, faces, norms, vals = measure.marching_cubes_lewiner(PV, isolevel, spacing=(dx,dy,dz))   
    return verts, faces, norms, vals

def plot_isosurf(PV,isolevel,dx,dy,dz,showplot):
    verts, faces, norms, vals = get_isosurf_geometry(PV,isolevel,dx,dy,dz)
    fig = plt.figure(figsize=(14,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(verts[:, 0], verts[:,1], faces, verts[:, 2], cmap='hsv', lw=1, alpha=0.5)
    if showplot:
        plt.show()
    return fig

def plot_scatter():
    # TODO: take volumetric data, plot a 3d scatter
    pass

