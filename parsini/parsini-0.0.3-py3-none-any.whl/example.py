# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from colorin import Colorin
from parsini import Parsini

# instancia clase
config= Parsini('conf')
# lee fichero de configuración
config.read()

# get valor del param dentro del sector
user= config.get_param('database','passwdb')

# get valores de configuracion en lista raw del file
print(config.get_rawlist())

# prepara archivo de configuración sector, param, value
config.set_param('database','user', 'alvaro')
config.set_param('database','host_ip2','172.17.0.12')

# crea parámetros nuevos para fichero de configuracion
config.create_param('profile','param', 'value')
config.create_param('new_conf','name', 'name')

# salva fichero de configuración con los nuevos valores
config.write()

# get valores de configuracion en lista raw del file
print(config.get_confidict())
