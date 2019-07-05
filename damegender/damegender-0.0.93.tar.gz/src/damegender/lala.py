#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damegender; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,
import pprint
import os
import json
import numpy as np
import requests
from app.dame_gender import Gender
from app.dame_utils import DameUtils
from app.dame_genderapi import DameGenderApi

du = DameUtils()
fichero = open("files/apikeys/genderapipass.txt", "r+")
path="files/names/partial.csv"
backup = open("files/names/genderapi"+du.path2file(path)+".txt", "w+")
contenido = fichero.readline()
string = ""
dga = DameGenderApi()
names = dga.csv2names(path)
names_list = du.split(names, 20)
myjson = {'names': []}
print(names_list)

for l in names_list:
    count = 1
    string = ""
    for n in l:
        if (len(l) > count):
            string = string + n + ";"
        else:
            string = string + n
            count = count + 1
    print(string)
    url1 = 'https://genderapi.io/api/?name='+ string +'&multi=true&key=' + contenido
    r = requests.get(url1)
    j = json.loads(r.text)

print(j)
myjson['names'].append(j['name'])
backup.write(r.text+"\n")
backup.close()

    #             r = requests.get('https://genderapi.io/api/?name=david;luis miguel;sara&multi=true&key=5d1c7127e4b20450744e2292')
#             j = json.loads(r.text)
#             print(r.text)
#             myjson['names'].append(j['names'])
# print(myjson)

# ds = DameSexmachine()
# cm = ds.confusion_matrix()
# print(cm)
# am = np.array([[2, 1, 0],[1, 15, 0],[0, 2, 0]])
# print(am)
# print(np.array_equal(cm, am))

# s = DameSexmachine()
# m = s.multinomialNB_load()
# array = [[ 0,  0,  1,  0, 21,  0,  0,  0,  0, 34,  2,  0,  0,  0,  0,  0, 0,
#                    0,  0,  0,  5,  0,  0,  0,  0,  0,  2,  0,  0,  0, 34,  1,  0],
#                  [ 0,  0,  0,  0, 21,  0,  0,  0,  0, 34,  0,  0,  0,  0,  0,  1, 0,
#                    0,  0,  0,  5,  0,  0,  1,  0,  0,  1,  0,  0,  1, 34,  0,  0]]
# predicted= m.predict(array)
# print(predicted)
# n = np.array([0, 0])
# print(n)
# du = DameUtils()
# path="files/names/partial.csv"
# fo = open("files/names/genderapi"+du.path2file(path)+".txt", "r+")

# if (os.path.isfile("files/names/genderapi"+du.path2file(path)+".txt")):
#     with open("files/names/genderapi"+du.path2file(path)+".txt", encoding='utf8') as f:
#         text = f.read().strip()
#         print(text)
#         json_object = json.loads(text)
#         print(json_object)
#     # fo = open("files/names/genderapi"+du.path2file(path)+".txt", "r+")
#     # print("File name: " + fo.name)
#     # jsondata = open("files/names/genderapi"+du.path2file(path)+".txt").read()
#     # print(jsondata)
#     # d = json.loads(jsondata)
#     # print(d)
#fo.close()
# dga = DameGenderApi()
# if (dga.config['DEFAULT']['genderapi'] == 'yes'):
#     print(dga.guess_list(path="files/names/partial.csv", binary=False))
