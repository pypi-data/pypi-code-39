# coding=utf-8
from sys import argv
from os.path import exists
import gzip
import os


def leer_archivo(ruta):
    try:
        f = open(ruta, "rb")
    except IOError, e:
        print e.errno, e.message
        print "Error al leer el archivo."
    else:
        data = f.read()
        f.close()
        return data


def escribir_archivo(ruta, data):
    try:
        f = open(ruta, "wb")
    except IOError, e:
        print e.errno, e.message
        print "Error al escribir el archivo."
    else:
        f.write(data)
        f.close()


def comprimir(ruta):
    data = leer_archivo(ruta)

    if data is not None:
        f = gzip.open(ruta + ".gz", "wb")
        f.write(data)
        f.close()


def descomprimir(ruta):
    f = gzip.open(ruta)
    escribir_archivo(ruta[:ruta.rfind(".gz")], f.read())
    f.close()

def main(dir):
    dirc = len(os.listdir(dir))
    if dirc >= 1:
        for filename in os.listdir(dir):
            if filename.lower().endswith(".gz"):
                descomprimir(dir + filename)
                print "Se ha descomprimido %s." % filename
            else:
                comprimir(dir + filename)
                print "Se ha comprimido %s." % filename
    else:
        print u"No se ha encontrado ningún archivo."

dir  = "../data/"
if __name__ == "__main__":
    main(dir)