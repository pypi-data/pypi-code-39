#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entry points, um Skripte zu generieren, die einen schnellen Überblick über den Inhalt einer Cassy-Datei erlauben.
"""

import argparse
from praktikum import cassy
from pylab import *

def cassy_info():

    argparser = argparse.ArgumentParser(description='Drucke eine Zusammenfassung der in einer Cassy-Datei enthaltenen Messungen.')
    argparser.add_argument('datei', default='', help='Name der Cassy-Datei (Dateityp lab, labx oder txt).')
    argparser.add_argument('-w', '--werte', default=False, action='store_true', help='Auch die Messwerte für alle Datenreihen ausgeben.')
    args = argparser.parse_args()

    data = cassy.CassyDaten(args.datei)
    for m in range(1, data.anzahl_messungen()+1):
        print('')
        messung = data.messung(m)
        messung.info()
        for dr in messung.datenreihen:
            dr.info()
            if args.werte:
                print('Messwerte:')
                print(dr.werte)

def cassy_plot():

    argparser = argparse.ArgumentParser(description='Schnellauftragung zweier Datenreihen zu einer in einer Cassy-Datei gespeicherten Messung.')
    argparser.add_argument('datei', default='', help='Name der Cassy-Datei (Dateityp lab, labx oder txt).')
    argparser.add_argument('x', default='', help='Name der Datenreihe zur Auftragung auf der x-Achse.')
    argparser.add_argument('y', default='', help='Name der Datenreihe zur Auftragung auf der y-Achse.')
    argparser.add_argument('-m', '--messung', default=1, type=int, help='Nummer der gewünschten Messung.')
    args = argparser.parse_args()

    data = cassy.CassyDaten(args.datei)
    messung = data.messung(args.messung)
    x = messung.datenreihe(args.x)
    y = messung.datenreihe(args.y)

    figure()
    errorbar(x.werte, y.werte, fmt='.')
    xstr = x.symbol
    if x.einheit:
        xstr += ' / %s' % x.einheit
    ystr = y.symbol
    if y.einheit:
        ystr += ' / %s' % y.einheit
    xlabel(xstr)
    ylabel(ystr)
    show()
