#!/usr/bin/env python3
# v2018.05.11

import sys
import ruamel.yaml
import os

def modifyparse(filename,var,val,node=None):

	# Buscamos en fichero principal
	err=modify(filename,var,val,node)
	if err==0: return 0

	# Buscamos en includes
	data=read(filename)
	if data.get("yaml-include"):
		for f in data["yaml-include"]:
			if os.path.isfile(f):
				err=modify(f,var,val,node)
				if err==0: return 0
			else:
				path=os.path.dirname(filename)
				f=path+os.path.sep+f
				if os.path.isfile(f):
					err=modify(f,var,val,node)
					if err==0: return 0
	# No encontrado
	return 1

# Modificamos fichero yaml sin alterar comentarios y estructura
def modify(filename,var,val,node=None):
	yaml=ruamel.yaml.YAML()
	yaml.width=4096
	f=open(filename,"r")
	raw=f.read()
	f.close()
	tabs=0
	for l in raw:
		if '\t' in l:
			tabs=1
			break
	if tabs: raw=raw.replace("\t", "  ")
	data=yaml.load(raw)
	datamod=data
	if node:
		for n in node:
			datamod=datamod.get(n)
			if datamod==None:
				return 1
	datamod[var]=val
	f=open(filename, "w")
	yaml.dump(data, f)
	# TODO se puede hacer dump en una variable?
	if tabs:
		f=open(filename,"r")
		raw=f.read()
		f.close()
		raw=raw.replace("  ", "\t")
		f2=open(filename,"w")
		f2.write(raw)
		f2.close()
	return 0

def read(filename):
	# Cargar yaml en ordereddict
	import collections
	ruamel.yaml.representer.RoundTripRepresenter.add_representer(
	collections.OrderedDict, ruamel.yaml.representer.RoundTripRepresenter.represent_ordereddict)
	f=open(filename,"rt")
	yaml=f.read()
	yaml=yaml.replace("\t", "  ")
	data=ruamel.yaml.load(yaml, Loader=ruamel.yaml.Loader)
	return data

# Interpreta include: [ file1, file2 .. ]
def readparse(filename):
	data=read(filename)
	if data.get("yaml-include"):
		for f in data["yaml-include"]:
			if os.path.isfile(f):
				subdata=read(f)
				data.update(subdata)
			else:
				path=os.path.dirname(filename)
				f=path+os.path.sep+f
				if os.path.isfile(f):
					subdata=read(f)
					data.update(subdata)
		#data["include"]=None
		data.pop("yaml-include")
	return data
