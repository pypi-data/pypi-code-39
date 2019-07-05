# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 17:37:33 2018

@author: Carmen
"""
from PIL import Image
import subprocess
import os
import matplotlib.pyplot as plt

def plotFunction(n, xlabel, ylabel):
    """
    With this function make functions plot is possible.
    
    Parameters
    ----------
    n: int
        number of files to plot.
    
    xlabel: str
        It will be used to label the x axis.
        
    ylabel: str
        It will be used to label the y axis
        
    t0: float
        Time at which the plot starts
    
    t1: float
        Time at which the plot finishes
    
    steps: int
        Number of points that will be taken from the x axis to make the 
        function interpolation.
        
    Returns
    -------
    frame
        It opens a frame. It will contain the function plot.
            
    Raises
    ------
    InputError
        If t0, t1 and steps inputs are bad arguments
            
    Warnings
    --------
    To execute this method GnuPlot should be installed and added to the 
    PATH variables.
        
    Notes
    -----
    If Gnuplot is not installed, the graph will be made with matplotlib.     
    
        
    """
    
    #estas condiciones sirven para definir la variable a. a es una tupla con
    #dos contenidos, primero la variable del eje x y segundo sus unidades.
    if "t" in xlabel[0]:
        a=(xlabel, "s")
    elif "c" in xlabel[0]:
        a=(xlabel, "A")
    elif "n" in xlabel[0] or "v" in xlabel[0]:
        a=(xlabel, "V")

    
    #estos comandos estan dirigidos a gnuplot  
    f='"data/data%s.dat" title "%s" w l'%(str(0), ylabel[0])
    for i in range(1,n):
        f=f+', "data/data%s.dat" title "%s" w l'%(str(i), ylabel[i])    
    gpcmds=[]

    #gpcmds es una lista con los comandos que se ejecutaran en la 
    #terminal de gnuplot
    gpcmds.extend(['set terminal pngcairo size 600, 350 enhanced '# Single line, no comma!
        'font "Verdana, 10" '  # Single line, no comma!
        'set xlabel "%s [%s]"'%a, #curiosamente este comando se ejecuta
        'set xlabel "%s [%s]"'%a, #comando para definir xlabel
        'set key right bottom', #para definir la posicion en la que aparecera la funcion
        'set grid', #activa el grid
        'set output "graphics/%s Vs %s.png"'%(a[0], ylabel[0]), #donde y como se guardara el grafico
        'plot %s'%f, # f puede hacer referencia a una funcion o a un archivo que se debe leer.
        'exit'])
    
    
    #con esta sentencia los argumentos de la lista se unen con '\n' y de ese
    #modo se crea convierte en un str.
    gpcmds = '\n'.join(gpcmds)
    
    #estos dos comandos llaman a la terminal y desde ahi se crean los 
    #directorios graphics y mkdir
    p = subprocess.Popen('mkdir graphics & mkdir data', shell=True)
    
    
    #se llama a gnuplot. Si al intentar ejecutar gnuplot surge algun problema, 
    #ya sea porque no instalado o no esta aÃ±adido al PATH, entonces entrara
    #en la excepcion y realizara el grafico mediante el modulo de matplotlib.
    try:
        p = subprocess.run(['gnuplot'], input=gpcmds.encode('utf-8'))
        
    except:
        f=[]
        with open("data/data0.dat", "r") as file1:
            dim = len(file1.read().split("\n"))
            
        with open("data/data.dat", "w") as file:
            file.write(a[0]+" ")
            t = (0,)
            for i in range(n):
                t += (i+1,)
                file.write(ylabel[i]+" ")
            file.write("\n")
            for i in range(dim-1):
                for j in range(n):
                    with open("data/data%s.dat" % str(j), "r") as file1:
                        # f sera el fitxategi que se vaya a leer
                        f=file1.read().split("\n")
                        if j == 0 and n == 1:
                            file.write(f[i]+"\n")
                        elif j == 0:
                            file.write(f[i]+" ")
                            
                        elif j < n-1:
                            file.write(f[i].split()[1]+" ")
                        else:
                            file.write(f[i].split()[1]+"\n")

        plt.plotfile("data/data.dat", t, delimiter = " ", subplots=False)
            
        plt.grid(True)
        plt.xlabel('%s [%s]'%(a[0], a[1]))
        plt.ylabel(' ')
        plt.savefig('graphics/%s Vs %s.png' % (a[0], ylabel[0]))
    
              
    #permite abrir el archivo guardado.
    img = Image.open('graphics/%s Vs %s.png' % (a[0], ylabel[0]))
    img.show() 

