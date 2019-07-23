#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Se crea una serie de diccionarios que incluyen los alófonos del español

En concreto se crea el diccionario ALOFONOS_ATAQUE, ALOFONOS_CODA, ALOFONOS_NUCLEO_ORALES, ALOFONOS_NUCLEO_NASALES
y ALOFONOS_PAUSA, que contienen los alófonos del tipo que se indica.

Se han dispuesto los fonemas así puesto que facilita y acorta las búsquedas, ya que el alófono con el que se
pronuncia un fonema depende del entorno y de la posición en la sílaba que ocupe. Así, las consonantes en ataque
tienen un repertorio más limitado de alófonos, mientras que en coda suele haber un mayor abanico de posibilidades,
incluyendo la eliminación del alófono (se expresa como alófono nulo). Igualmente, el hecho de estar "envuelto" o no
en un entorno nasal hace variar sustancialmente los alófonos vocálicos, de forma que los alófonos en entornos orales
nunca aparecen en entornos nasales y a la inversa.

Todos los diccionarios tienen la misma estructura: las claves son el símbolo IPA de un fonema, y el contenido de
cada elemento es una lista de alófonos, que incluye todos los alófonos con los que se pueda expresar dicho fonema.

# También se incluyen algunas otras constantes auxiliares para la definición de las condiciones, así como el
ALOFONO_VACIO global, que evita (en lo posible, salvo que hagamos deepcopy) multiplicidad de objetos a cambio
de una multiplicidad de referencias al objeto.
"""

from copy import deepcopy

from iar_transcriber.alofono import Alofono, AlofonoConsonante, AlofonoVocal, AlofonoSemiconsonante, AlofonoSemivocal, AlofonoPausa

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


# TODO: podríamos usar sets en lugar de listas, porque lo único que hacemos es la operación if XXX in condiciones_fonema
# Se crea una serie de variables auxiliares que se utiliza para definir las restricciones de los alófonos
NASALES = [u'm', u'n', u'ɲ']
OCLUSIVAS_SORDAS = [u'p', u't', u'k']
# OJO: el carácter del grafema g es distinto del del alófono ɡ (aunque parezca el mismo aquí)
OCLUSIVAS_SONORAS = [u'b', u'd', u'ɡ']
OCLUSIVAS = OCLUSIVAS_SONORAS + OCLUSIVAS_SORDAS
AFRICADAS_SORDAS = [u'ʧ']
AFRICADAS_SONORAS = [u'ʤ']
AFRICADAS = AFRICADAS_SORDAS + AFRICADAS_SONORAS
FRICATIVAS_SORDAS = [u'f', u'θ', u's', u'ʃ', u'x']
FRICATIVAS_SONORAS = [u'ʒ']
FRICATIVAS = FRICATIVAS_SORDAS + FRICATIVAS_SONORAS
APROXIMANTES = [u'ʝ̞']
LATERALES = [u'l', u'ʎ']
VIBRANTES = [u'r', u'ɾ']

ALVEOLARES = [u's', u'l', u'r', u'n']
POSTALVEOLARES = [u'ʒ', u'ʃ', u'ʤ', u'ʧ']
PALATALES = [u'ɲ', u'ʎ', u'ʝ̞']
# OJO: el carácter del grafema g es distinto del del alófono ɡ (aunque parezca el mismo aquí)
VELARES = [u'ɡ', u'k', u'x']

SONORAS = NASALES + OCLUSIVAS_SONORAS + AFRICADAS_SONORAS + FRICATIVAS_SONORAS + APROXIMANTES + LATERALES + VIBRANTES
SORDAS = OCLUSIVAS_SORDAS + AFRICADAS_SORDAS + FRICATIVAS_SORDAS
CONSONANTES = SONORAS + SORDAS

LIQUIDAS = [u'l', u'ɾ']
SOLIDAS = NASALES + OCLUSIVAS + AFRICADAS + FRICATIVAS + APROXIMANTES + [u'r', u'ʎ']

SEMIVOCALES = [u'i̯', u'u̯']
VOCALES = [u'i', u'e', u'a', u'o', u'u']
SEMICONSONANTES = [u'j', u'w']
VOCOIDES = SEMIVOCALES + SEMICONSONANTES + VOCALES
VOCOIDES_ANTERIORES = [u'i', u'i̯', u'j', u'e']
VOCOIDES_POSTERIORES = [u'u', u'u̯', u'w', u'o']

PAUSAS = [u'|', u'‖']

# Aunque el alófono vacío es trivial, se define y se utiliza como constante para que todos los alófonos vacíos
# (que de hecho son los más frecuentes) sean copias de un único objeto en memoria, en lugar de crear una estructura
# de datos para cada posición vacía de cada sílaba.
ALOFONO_VACIO = Alofono()

# ALOFONOS_ATAQUE es un diccionario (que quizá debería llamarse ALOFONOS_DE_ATAQUE_PARA_FONEMA, pero es muy largo).
# Las claves son los símbolos IPA de cada fonema aceptado por el sistema, y para cada uno se tiene una estructura de
# datos consistente en una lista de alófonos con los que se puede expresar dicho fonema.
# Por otra parte, al crear los alófonos les aportamos la información de qué alófono IPA son, de qué fonema provienen
# (es el mismo que el fonema de la clave del diccionario), y qué condiciones de fonemas en su entorno necesitan.
# Se incluyen en el diccionario los datos de los fonemas geminados, tanto consonánticos como vocálicos.

# Es poco intuitivo que, por ejemplo, se tengan alófonos como /n:/ que puede serlo tanto del fonema /n:/ como del /n/.
# Esto ocurre también en las consonantes en coda, pero no en las vocales. Parece que no tiene sentido y que tendríamos
# que tener siempre el fonema geminado cuando sale un alófono geminado, pero esto no es así. ¿Por qué?
# La clave para entenderlo es que cuando se tienen dos fonemas iguales consecutivos, como en <innovar> se
# identifica como un fonema largo, y el alófono por lo tanto, también lo es (y nos queda /i.nːo.ˈbaɾ/, [i.nːo.ˈβ̞aɾ]).
# Sin embargo, existen combinaciones de consonantes en coda y ataque que, siendo fonemas distintos, dan lugar a un
# fonema doble (las oclusivas sordas que se sonorizan en coda, y las vibrantes). En estos casos, la transcripción
# fonológica mantiene los fonemas, mientras que en la transcripción fonética aparece el alófono largo.
# Compara las diferencias de <pop bar, popbar, Bob bar, bobbar>: /ˈpopˈbaɾ|popˈbaɾ|ˈboˈbːaɾ|boˈbːaɾ/,
# [ˈpɔˈβ̞ːaɾ|pɔˈβ̞ːaɾ|ˈboˈβ̞ːaɾ|boˈβ̞ːaɾ] (fíjate en la separación de fonemas, y en la apertura de la vocal).
# Para hacer esto posible, en estos casos el fonema que está en coda se mantiene pero se considera que se expresa
# con un alófono cero, y el fonema de ataque también se mantiene pero se expresa con un alófono de duración larga.

ALOFONOS_ATAQUE = dict()
# Nasales
ALOFONOS_ATAQUE[u'm'] = (AlofonoConsonante(u'm', u'm'), )
ALOFONOS_ATAQUE[u'mː'] = (AlofonoConsonante(u'mː', u'mː'), )
ALOFONOS_ATAQUE[u'n'] = (AlofonoConsonante(u'nː', u'n', fonemas_previos_ipa=[u'n']),
                         AlofonoConsonante(u'n', u'n'))
ALOFONOS_ATAQUE[u'nː'] = (AlofonoConsonante(u'nː', u'nː'), )
ALOFONOS_ATAQUE[u'ɲ'] = (AlofonoConsonante(u'ɲː', u'ɲ', fonemas_previos_ipa=[u'ɲ']),
                         AlofonoConsonante(u'ɲ', u'ɲ'))
ALOFONOS_ATAQUE[u'ɲː'] = (AlofonoConsonante(u'ɲː', u'ɲː'), )
# Oclusivas
ALOFONOS_ATAQUE[u'b'] = (AlofonoConsonante(u'β̞ː', u'b', fonemas_previos_ipa=[u'b', u'p']),
                         AlofonoConsonante(u'b', u'b', fonemas_previos_ipa=NASALES + PAUSAS),
                         AlofonoConsonante(u'β̞', u'b'))
ALOFONOS_ATAQUE[u'bː'] = (AlofonoConsonante(u'bː', u'bː', fonemas_previos_ipa=NASALES + PAUSAS),
                          AlofonoConsonante(u'β̞ː', u'bː'), )
ALOFONOS_ATAQUE[u'p'] = (AlofonoConsonante(u'pː', u'p', fonemas_previos_ipa=[u'p']),
                         AlofonoConsonante(u'p', u'p'))
ALOFONOS_ATAQUE[u'pː'] = (AlofonoConsonante(u'pː', u'pː'), )
ALOFONOS_ATAQUE[u'd'] = (AlofonoConsonante(u'ð̞ː', u'd', fonemas_previos_ipa=[u'd', u't']),
                         AlofonoConsonante(u'd̪', u'd', fonemas_previos_ipa=NASALES + PAUSAS + [u'l']),
                         AlofonoConsonante(u'ð̞', u'd'))
ALOFONOS_ATAQUE[u'dː'] = (AlofonoConsonante(u'dː', u'dː', fonemas_previos_ipa=NASALES + PAUSAS + [u'l']),
                          AlofonoConsonante(u'ð̞ː', u'dː'), )
ALOFONOS_ATAQUE[u't'] = (AlofonoConsonante(u'tː', u't', fonemas_previos_ipa=[u't']),
                         AlofonoConsonante(u't̟', u't', fonemas_previos_ipa=[u'θ']),
                         AlofonoConsonante(u't̪', u't'))
ALOFONOS_ATAQUE[u'tː'] = (AlofonoConsonante(u'tː', u'tː'), )
# OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (aunque parezca el mismo aquí)
ALOFONOS_ATAQUE[u'ɡ'] = (AlofonoConsonante(u'ɣ̞ː', u'ɡ', fonemas_previos_ipa=[u'ɡ', u'k']),
                         AlofonoConsonante(u'ɡ', u'ɡ', fonemas_previos_ipa=NASALES + PAUSAS),
                         AlofonoConsonante(u'ɣ̞', u'ɡ'))
# OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (aunque parezca el mismo aquí)
ALOFONOS_ATAQUE[u'ɡː'] = (AlofonoConsonante(u'ɡː', u'ɡː', fonemas_previos_ipa=NASALES + PAUSAS),
                          AlofonoConsonante(u'ɣ̞ː', u'ɡː'), )
ALOFONOS_ATAQUE[u'k'] = (AlofonoConsonante(u'kː', u'k', fonemas_previos_ipa=[u'k']),
                         AlofonoConsonante(u'k̠', u'k', fonemas_siguientes_ipa=VOCOIDES_POSTERIORES),
                         AlofonoConsonante(u'k̟', u'k', fonemas_siguientes_ipa=VOCOIDES_ANTERIORES),
                         AlofonoConsonante(u'k', u'k'))
ALOFONOS_ATAQUE[u'kː'] = (AlofonoConsonante(u'kː', u'kː'), )
# Africadas
ALOFONOS_ATAQUE[u'ʤ'] = (AlofonoConsonante(u'ʤː', u'ʤ', fonemas_previos_ipa=[u'ʤ']),
                         AlofonoConsonante(u'ʤ', u'ʤ'), )
ALOFONOS_ATAQUE[u'ʤː'] = (AlofonoConsonante(u'ʤː', u'ʤː'), )
ALOFONOS_ATAQUE[u'ʧ'] = (AlofonoConsonante(u'ʧː', u'ʧ', fonemas_previos_ipa=[u'ʧ']),
                         AlofonoConsonante(u'ʧ', u'ʧ'), )
ALOFONOS_ATAQUE[u'ʧː'] = (AlofonoConsonante(u'ʧː', u'ʧː'), )
# Fricativas
ALOFONOS_ATAQUE[u'f'] = (AlofonoConsonante(u'fː', u'f', fonemas_previos_ipa=[u'f']),
                         AlofonoConsonante(u'f', u'f'))
ALOFONOS_ATAQUE[u'fː'] = (AlofonoConsonante(u'fː', u'fː'), )
ALOFONOS_ATAQUE[u'θ'] = (AlofonoConsonante(u'θː', u'θ', fonemas_previos_ipa=[u'θ']),
                         AlofonoConsonante(u'θ', u'θ'))
ALOFONOS_ATAQUE[u'θː'] = (AlofonoConsonante(u'θː', u'θː'), )
ALOFONOS_ATAQUE[u's'] = (AlofonoConsonante(u'sː', u's', fonemas_previos_ipa=[u's']),
                         AlofonoConsonante(u's', u's'))
ALOFONOS_ATAQUE[u'sː'] = (AlofonoConsonante(u'sː', u'sː'), )
ALOFONOS_ATAQUE[u'ʒ'] = (AlofonoConsonante(u'ʒː', u'ʒ', fonemas_previos_ipa=[u'ʒ']),
                         AlofonoConsonante(u'ʒ', u'ʒ'))
ALOFONOS_ATAQUE[u'ʒː'] = (AlofonoConsonante(u'ʒː', u'ʒː'), )
ALOFONOS_ATAQUE[u'ʃ'] = (AlofonoConsonante(u'ʃː', u'ʃ', fonemas_previos_ipa=[u'ʃ']),
                         AlofonoConsonante(u'ʃ', u'ʃ'))
ALOFONOS_ATAQUE[u'ʃː'] = (AlofonoConsonante(u'ʃː', u'ʃː'), )
ALOFONOS_ATAQUE[u'x'] = (AlofonoConsonante(u'χː', u'x', fonemas_previos_ipa=[u'x'],
                                           fonemas_siguientes_ipa=VOCOIDES_POSTERIORES),
                         AlofonoConsonante(u'χ', u'x', fonemas_siguientes_ipa=VOCOIDES_POSTERIORES),
                         AlofonoConsonante(u'xː', u'x', fonemas_previos_ipa=[u'x']),
                         AlofonoConsonante(u'x', u'x'))
ALOFONOS_ATAQUE[u'xː'] = (AlofonoConsonante(u'χː', u'xː', fonemas_siguientes_ipa=VOCOIDES_POSTERIORES),
                          AlofonoConsonante(u'xː', u'xː'))
# Aproximantes
ALOFONOS_ATAQUE[u'ʝ̞'] = (AlofonoConsonante(u'ʝ̞ː', u'ʝ̞', fonemas_previos_ipa=[u'ʝ̞']),
                          AlofonoConsonante(u'ɟ͡ʝ̞', u'ʝ̞', fonemas_previos_ipa=NASALES + LATERALES + PAUSAS),
                          AlofonoConsonante(u'ʝ̞', u'ʝ̞'))
ALOFONOS_ATAQUE[u'ʝ̞ː'] = (AlofonoConsonante(u'ʝ̞ː', u'ʝ̞ː'), )
# Laterales
ALOFONOS_ATAQUE[u'l'] = (AlofonoConsonante(u'lː', u'l', fonemas_previos_ipa=[u'l']),
                         AlofonoConsonante(u'l', u'l'))
ALOFONOS_ATAQUE[u'lː'] = (AlofonoConsonante(u'lː', u'lː'), )
ALOFONOS_ATAQUE[u'ʎ'] = (AlofonoConsonante(u'ʎː', u'ʎ', fonemas_previos_ipa=[u'ʎ']),
                         AlofonoConsonante(u'ʎ', u'ʎ'))
ALOFONOS_ATAQUE[u'ʎː'] = (AlofonoConsonante(u'ʎː', u'ʎː'), )
# Vibrantes
ALOFONOS_ATAQUE[u'r'] = (AlofonoConsonante(u'rː', u'r', fonemas_previos_ipa=[u'ɾ']),
                         AlofonoConsonante(u'r', u'r'))
ALOFONOS_ATAQUE[u'rː'] = (AlofonoConsonante(u'rː', u'rː'), )
ALOFONOS_ATAQUE[u'ɾ'] = (AlofonoConsonante(u'ɾ', u'ɾ'), )
ALOFONOS_ATAQUE[u'ɾː'] = (AlofonoConsonante(u'ɾː', u'ɾː'), )


# ALOFONOS_CODA contiene, para cada fonema que puede aparecer en coda, los alófonos con los que se expresa
ALOFONOS_CODA = dict()
# Nasales
ALOFONOS_CODA[u'm'] = (AlofonoConsonante(u'n', u'm', fonemas_siguientes_ipa=PAUSAS),  # Tiene que ir el primero
                       AlofonoConsonante(u'm', u'm', fonemas_siguientes_ipa=[u'b', u'p']),
                       AlofonoConsonante(u'ɱ', u'm', fonemas_siguientes_ipa=[u'f']),
                       AlofonoConsonante(u'n̟', u'm', fonemas_siguientes_ipa=[u'θ']),
                       AlofonoConsonante(u'n̪', u'm', fonemas_siguientes_ipa=[u'd', u't']),
                       AlofonoConsonante(u'ⁿ', u'm', fonemas_siguientes_ipa=[u's'],
                                         fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                       AlofonoConsonante(u'n', u'm', fonemas_siguientes_ipa=[u's', u'l', u'r']),
                       AlofonoConsonante(u'm̥', u'm', fonemas_siguientes_ipa=[u'n']),  # OJO: m̥ = m en superíndice
                       AlofonoConsonante(u'ⁿ', u'm', fonemas_siguientes_ipa=[u'm']),
                       AlofonoConsonante(u'ⁿ̠', u'm', fonemas_siguientes_ipa=[u'ɲ']),
                       AlofonoConsonante(u'n̠', u'm', fonemas_siguientes_ipa=[u'ʎ', u'ʝ̞'] + POSTALVEOLARES),
                       AlofonoConsonante(u'ɴ', u'm', fonemas_siguientes_ipa=[u'x'],
                                         fonemas_postsiguientes_ipa=VOCOIDES_POSTERIORES),
                       AlofonoConsonante(u'ŋ', u'm', fonemas_siguientes_ipa=VELARES))
ALOFONOS_CODA[u'mː'] = (AlofonoConsonante(u'mː', u'mː', fonemas_siguientes_ipa=PAUSAS),  # Tiene que ir el primero
                        AlofonoConsonante(u'ɱː', u'mː', fonemas_siguientes_ipa=[u'f']),
                        AlofonoConsonante(u'', u'mː', fonemas_siguientes_ipa=[u'n']),
                        AlofonoConsonante(u'mː', u'mː'))
ALOFONOS_CODA[u'n'] = (AlofonoConsonante(u'n', u'n', fonemas_siguientes_ipa=PAUSAS),  # Tiene que ir el primero
                       AlofonoConsonante(u'm', u'n', fonemas_siguientes_ipa=[u'b', u'p']),
                       AlofonoConsonante(u'ɱ', u'n', fonemas_siguientes_ipa=[u'f']),
                       AlofonoConsonante(u'n̟', u'n', fonemas_siguientes_ipa=[u'θ']),
                       AlofonoConsonante(u'n̪', u'n', fonemas_siguientes_ipa=[u'd', u't']),
                       AlofonoConsonante(u'ⁿ', u'n', fonemas_siguientes_ipa=[u's'],
                                         fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                       AlofonoConsonante(u'n', u'n', fonemas_siguientes_ipa=[u's', u'l', u'r']),
                       AlofonoConsonante(u'', u'n', fonemas_siguientes_ipa=[u'n']),
                       AlofonoConsonante(u'ⁿ', u'n', fonemas_siguientes_ipa=[u'm']),
                       AlofonoConsonante(u'ⁿ̠', u'n', fonemas_siguientes_ipa=[u'ɲ']),
                       AlofonoConsonante(u'n̠', u'n', fonemas_siguientes_ipa=[u'ʎ', u'ʝ̞'] + POSTALVEOLARES),
                       AlofonoConsonante(u'ɴ', u'n', fonemas_siguientes_ipa=[u'x'],
                                         fonemas_postsiguientes_ipa=VOCOIDES_POSTERIORES),
                       AlofonoConsonante(u'ŋ', u'n', fonemas_siguientes_ipa=VELARES))
ALOFONOS_CODA[u'nː'] = (AlofonoConsonante(u'nː', u'nː', fonemas_siguientes_ipa=PAUSAS),  # Tiene que ir el primero
                        AlofonoConsonante(u'n̟ː', u'nː', fonemas_siguientes_ipa=[u'θ']),
                        AlofonoConsonante(u'n̪ː', u'nː', fonemas_siguientes_ipa=[u'd', u't']),
                        AlofonoConsonante(u'nː', u'nː', fonemas_siguientes_ipa=[u's', u'l', u'r']),
                        AlofonoConsonante(u'', u'nː', fonemas_siguientes_ipa=[u'n']),
                        AlofonoConsonante(u'nː', u'nː', fonemas_siguientes_ipa=[u'm']),
                        AlofonoConsonante(u'n̠ː', u'nː', fonemas_siguientes_ipa=PALATALES + POSTALVEOLARES),  # CAMBIO
                        AlofonoConsonante(u'ɴː', u'nː', fonemas_siguientes_ipa=[u'x'],
                                          fonemas_postsiguientes_ipa=VOCOIDES_POSTERIORES),
                        AlofonoConsonante(u'ŋː', u'nː', fonemas_siguientes_ipa=VELARES),
                        AlofonoConsonante(u'nː', u'nː'))
ALOFONOS_CODA[u'ɲ'] = (AlofonoConsonante(u'', u'ɲ', fonemas_siguientes_ipa=[u'ɲ']),
                       AlofonoConsonante(u'ɲ', u'ɲ'))
ALOFONOS_CODA[u'ɲː'] = (AlofonoConsonante(u'', u'ɲː', fonemas_siguientes_ipa=[u'ɲ']),
                        AlofonoConsonante(u'ɲː', u'ɲː'))
# Oclusivas
ALOFONOS_CODA[u'b'] = (AlofonoConsonante(u'', u'b', fonemas_siguientes_ipa=[u'b']),
                       AlofonoConsonante(u'β̥', u'b', fonemas_siguientes_ipa=PAUSAS),  # OJO: β̥ = β̞ en superíndice.
                       AlofonoConsonante(u'', u'b', fonemas_siguientes_ipa=[u's'],
                                         fonemas_postsiguientes_ipa=OCLUSIVAS),
                       AlofonoConsonante(u'β̞', u'b'))
ALOFONOS_CODA[u'bː'] = (AlofonoConsonante(u'', u'bː', fonemas_siguientes_ipa=[u'b']),
                        AlofonoConsonante(u'bː', u'bː'))
ALOFONOS_CODA[u'p'] = (AlofonoConsonante(u'', u'p', fonemas_siguientes_ipa=[u'p', u'b']),
                       AlofonoConsonante(u'β̞', u'p'))
ALOFONOS_CODA[u'pː'] = (AlofonoConsonante(u'', u'pː', fonemas_siguientes_ipa=[u'p']),
                        AlofonoConsonante(u'pː', u'pː'))
ALOFONOS_CODA[u'd'] = (AlofonoConsonante(u'', u'd', fonemas_siguientes_ipa=[u'd']),
                       AlofonoConsonante(u'ð̥', u'd', fonemas_siguientes_ipa=OCLUSIVAS + VOCOIDES + LATERALES + PAUSAS),
                       AlofonoConsonante(u'ð̥', u'd', fonemas_siguientes_ipa=FRICATIVAS,  # OJO: ð̥ = ð̞  en superínd.
                                         fonemas_postsiguientes_ipa=VOCOIDES),
                       AlofonoConsonante(u'', u'd', fonemas_siguientes_ipa=FRICATIVAS,
                                         fonemas_postsiguientes_ipa=OCLUSIVAS),
                       AlofonoConsonante(u'ð̞', u'd'))
ALOFONOS_CODA[u'dː'] = (AlofonoConsonante(u'', u'dː', fonemas_siguientes_ipa=[u'd']),
                        AlofonoConsonante(u'dː', u'dː'))
ALOFONOS_CODA[u't'] = (AlofonoConsonante(u'', u't', fonemas_siguientes_ipa=[u't', u'd']),
                       AlofonoConsonante(u'ð̞', u't'))
ALOFONOS_CODA[u'tː'] = (AlofonoConsonante(u'', u'tː', fonemas_siguientes_ipa=[u't']),
                        AlofonoConsonante(u'tː', u'tː'))
# OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (aunque parezca el mismo aquí)
ALOFONOS_CODA[u'ɡ'] = (AlofonoConsonante(u'', u'ɡ', fonemas_siguientes_ipa=[u'ɡ']),
                       AlofonoConsonante(u'ɣ̥', u'ɡ', fonemas_siguientes_ipa=PAUSAS),  # OJO: ɣ̥ = ɣ̞ en superíndice.
                       AlofonoConsonante(u'ɣ̥', u'ɡ', fonemas_siguientes_ipa=FRICATIVAS,
                                         fonemas_postsiguientes_ipa=VOCOIDES),
                       AlofonoConsonante(u'ɣ̞', u'ɡ'))
# OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (aunque parezca el mismo aquí)
ALOFONOS_CODA[u'ɡː'] = (AlofonoConsonante(u'', u'ɡː', fonemas_siguientes_ipa=[u'ɡ']),
                        AlofonoConsonante(u'ɡː', u'ɡː'))
ALOFONOS_CODA[u'k'] = (AlofonoConsonante(u'', u'k', fonemas_siguientes_ipa=[u'k', u'ɡ']),
                       AlofonoConsonante(u'ɣ̞', u'k'))
ALOFONOS_CODA[u'kː'] = (AlofonoConsonante(u'', u'kː', fonemas_siguientes_ipa=[u'k']),
                        AlofonoConsonante(u'kː', u'kː'))
# Africadas
ALOFONOS_CODA[u'ʤ'] = (AlofonoConsonante(u'', u'ʤ', fonemas_siguientes_ipa=[u'ʤ']),
                       AlofonoConsonante(u'ʤ', u'ʤ'))
ALOFONOS_CODA[u'ʤː'] = (AlofonoConsonante(u'', u'ʤː', fonemas_siguientes_ipa=[u'ʤ']),
                        AlofonoConsonante(u'ʤː', u'ʤː'))
ALOFONOS_CODA[u'ʧ'] = (AlofonoConsonante(u'', u'ʧ', fonemas_siguientes_ipa=[u'ʧ']),
                       AlofonoConsonante(u'ʧ', u'ʧ'))
ALOFONOS_CODA[u'ʧː'] = (AlofonoConsonante(u'', u'ʧː', fonemas_siguientes_ipa=[u'ʧ']),
                        AlofonoConsonante(u'ʧː', u'ʧː'))
# Fricativas
ALOFONOS_CODA[u'f'] = (AlofonoConsonante(u'', u'f', fonemas_siguientes_ipa=[u'f']),
                       AlofonoConsonante(u'f̬', u'f', fonemas_siguientes_ipa=SONORAS),
                       AlofonoConsonante(u'f', u'f'))
ALOFONOS_CODA[u'fː'] = (AlofonoConsonante(u'', u'fː', fonemas_siguientes_ipa=[u'f']),
                        AlofonoConsonante(u'f̬ː', u'fː', fonemas_siguientes_ipa=SONORAS),
                        AlofonoConsonante(u'fː', u'fː'))
ALOFONOS_CODA[u'θ'] = (AlofonoConsonante(u'', u'θ', fonemas_siguientes_ipa=[u'θ']),
                       AlofonoConsonante(u'θ̬', u'θ', fonemas_siguientes_ipa=SONORAS),
                       AlofonoConsonante(u'θ', u'θ'))
ALOFONOS_CODA[u'θː'] = (AlofonoConsonante(u'', u'θː', fonemas_siguientes_ipa=[u'θ']),
                        AlofonoConsonante(u'θ̬ː', u'θː', fonemas_siguientes_ipa=SONORAS),
                        AlofonoConsonante(u'θː', u'θː'))
ALOFONOS_CODA[u's'] = (AlofonoConsonante(u'', u's', fonemas_siguientes_ipa=[u's'] + VIBRANTES),
                       AlofonoConsonante(u'z̪', u's', fonemas_siguientes_ipa=[u'd']),  # OJO: z̪ = s̪̬
                       AlofonoConsonante(u's̪', u's', fonemas_siguientes_ipa=[u't']),
                       AlofonoConsonante(u's̬', u's', fonemas_siguientes_ipa=SONORAS),
                       AlofonoConsonante(u's', u's'))
ALOFONOS_CODA[u'sː'] = (AlofonoConsonante(u'', u'sː', fonemas_siguientes_ipa=[u's'] + VIBRANTES),
                        AlofonoConsonante(u'z̪ː', u'sː', fonemas_siguientes_ipa=[u'd']),   # OJO: z̪ː = s̪̬ː
                        # OJO: Era la s dentalizada y sonorizada: s̪̬
                        AlofonoConsonante(u's̪ː', u'sː', fonemas_siguientes_ipa=[u't']),
                        AlofonoConsonante(u's̬ː', u'sː', fonemas_siguientes_ipa=SONORAS),
                        AlofonoConsonante(u'sː', u'sː'))
ALOFONOS_CODA[u'ʒ'] = (AlofonoConsonante(u'', u'ʒ', fonemas_siguientes_ipa=[u'ʒ']),
                       AlofonoConsonante(u'ʒ̪', u'ʒ', fonemas_siguientes_ipa=[u'd', u't']),
                       AlofonoConsonante(u'ʒ', u'ʒ'))
ALOFONOS_CODA[u'ʒː'] = (AlofonoConsonante(u'', u'ʒː', fonemas_siguientes_ipa=[u'ʒ']),
                        AlofonoConsonante(u'ʒ̪ː', u'ʒː', fonemas_siguientes_ipa=[u'd', u't']),
                        AlofonoConsonante(u'ʒː', u'ʒː'))
ALOFONOS_CODA[u'ʃ'] = (AlofonoConsonante(u'', u'ʃ', fonemas_siguientes_ipa=[u'ʃ']),
                       AlofonoConsonante(u'ʒ̪', u'ʃ', fonemas_siguientes_ipa=[u'd']),
                       AlofonoConsonante(u'ʃ̪', u'ʃ', fonemas_siguientes_ipa=[u't']),
                       AlofonoConsonante(u'ʃ̬', u'ʃ', fonemas_siguientes_ipa=SONORAS),
                       AlofonoConsonante(u'ʃ', u'ʃ'))
ALOFONOS_CODA[u'ʃː'] = (AlofonoConsonante(u'', u'ʃː', fonemas_siguientes_ipa=[u'ʃ']),
                        AlofonoConsonante(u'ʒ̪ː', u'ʃː', fonemas_siguientes_ipa=[u'd']),
                        AlofonoConsonante(u'ʃ̪ː', u'ʃː', fonemas_siguientes_ipa=[u't']),
                        AlofonoConsonante(u'ʃ̬ː', u'ʃː', fonemas_siguientes_ipa=SONORAS),
                        AlofonoConsonante(u'ʃː', u'ʃː'))
ALOFONOS_CODA[u'x'] = (AlofonoConsonante(u'', u'x', fonemas_siguientes_ipa=[u'x']),
                       # OJO: x̥ = x en superíndice.
                       AlofonoConsonante(u'x̥', u'x', fonemas_siguientes_ipa=FRICATIVAS + NASALES + PAUSAS),
                       AlofonoConsonante(u'', u'x'))
ALOFONOS_CODA[u'xː'] = (AlofonoConsonante(u'', u'xː', fonemas_siguientes_ipa=[u'x']),
                        AlofonoConsonante(u'xː', u'xː'))
# Aproximantes
# En realidad, [ʝ̞] [ʝ̞ː] no aparecerán nunca en coda. Se pone por completitud
ALOFONOS_CODA[u'ʝ̞'] = (AlofonoConsonante(u'', u'ʝ̞', fonemas_siguientes_ipa=[u'ʝ̞']),
                        AlofonoConsonante(u'ʝ̞', u'ʝ̞'))
ALOFONOS_CODA[u'ʝ̞ː'] = (AlofonoConsonante(u'', u'ʝ̞ː', fonemas_siguientes_ipa=[u'ʝ̞']),
                         AlofonoConsonante(u'ʝ̞ː', u'ʝ̞ː'),)
# Laterales
ALOFONOS_CODA[u'l'] = (AlofonoConsonante(u'', u'l', fonemas_siguientes_ipa=[u'l']),
                       AlofonoConsonante(u'l̪', u'l', fonemas_siguientes_ipa=[u'd', u't']),
                       AlofonoConsonante(u'l̟', u'l', fonemas_siguientes_ipa=[u'θ']),
                       AlofonoConsonante(u'l̠', u'l', fonemas_siguientes_ipa=PALATALES + POSTALVEOLARES),
                       AlofonoConsonante(u'l', u'l'))
ALOFONOS_CODA[u'lː'] = (AlofonoConsonante(u'', u'lː', fonemas_siguientes_ipa=[u'l']),
                        AlofonoConsonante(u'l̪ː', u'lː', fonemas_siguientes_ipa=[u'd', u't']),
                        AlofonoConsonante(u'l̟ː', u'lː', fonemas_siguientes_ipa=[u'θ']),
                        AlofonoConsonante(u'l̠ː', u'lː', fonemas_siguientes_ipa=PALATALES + POSTALVEOLARES),
                        AlofonoConsonante(u'lː', u'lː'))
# En realidad, [ʎ] [ʎː] no aparecerán nunca en coda. Se pone por completitud
# Hay complicaciones en el código para convertir las /ʎ/ finales en /l/. Pero es que el cambio no es sólo alofónico
# (en cuyo caso bastaría con añadir un alófono y quitarse complicaciones), sino que se cambia el fonema.
ALOFONOS_CODA[u'ʎ'] = (AlofonoConsonante(u'', u'ʎ', fonemas_siguientes_ipa=[u'ʎ']),
                       AlofonoConsonante(u'ʎ', u'ʎ'))
ALOFONOS_CODA[u'ʎː'] = (AlofonoConsonante(u'', u'ʎː', fonemas_siguientes_ipa=[u'ʎ']),
                        AlofonoConsonante(u'ʎː', u'ʎː'))
# Vibrantes
ALOFONOS_CODA[u'r'] = (AlofonoConsonante(u'', u'r', fonemas_siguientes_ipa=[u'r']),
                       AlofonoConsonante(u'r', u'r'))
ALOFONOS_CODA[u'rː'] = (AlofonoConsonante(u'', u'rː', fonemas_siguientes_ipa=[u'r']),
                        AlofonoConsonante(u'rː', u'rː'))
ALOFONOS_CODA[u'ɾ'] = (AlofonoConsonante(u'', u'ɾ', fonemas_siguientes_ipa=[u'r']),
                       AlofonoConsonante(u'ɾ', u'ɾ'))
# En realidad, [ɾː] no aparecerán nunca en coda (equivale a [r]). Se pone por completitud
ALOFONOS_CODA[u'ɾː'] = (AlofonoConsonante(u'', u'ɾː', fonemas_siguientes_ipa=[u'r']),
                        AlofonoConsonante(u'ɾː', u'ɾː'))


ALOFONOS_PAUSA = dict()
ALOFONOS_PAUSA[u'|'] = (AlofonoPausa(u'|', u'|'), )
ALOFONOS_PAUSA[u'‖'] = (AlofonoPausa(u'‖', u'‖'), )


# Dividimos los alófonos de núcleo en dos (nasales y no nasales) por motivos de eficiencia y velocidad de procesado.
ALOFONOS_NUCLEO_ORALES = dict()
# TODO: tras los fallos vistos en el manual que me habían inducido a error, parece que hay vocales que siempre se
# abren cuando tienen coda (independientemente de la consonante que sea), así que, aunque da miedo, se podrían
# simplificar las condiciones. Para la i, o, u, solo quedarían por incluir las africadas, [ʎ] (que no sale en coda)
# y la [r].
# OJO: En partes del código como en silaba, vocaliza_semiconsonante y semivocal, se considera que el primer alófono
# es abierto y el último cerrado. Es importante mantener este orden.
# Vocales
ALOFONOS_NUCLEO_ORALES[u'i'] = (AlofonoVocal(u'i̞', u'i', fonemas_siguientes_ipa=NASALES,
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'i̞', u'i', fonemas_siguientes_ipa=SEMIVOCALES,
                                             fonemas_postsiguientes_ipa=NASALES,
                                             fonemas_postpostsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'i̞', u'i', fonemas_siguientes_ipa=[u'θ', u's', u'ʒ', u'ʃ', u'ɾ', u'l'],
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'i̞', u'i', fonemas_siguientes_ipa=OCLUSIVAS + [u'f'],
                                             fonemas_postsiguientes_ipa=SOLIDAS + PAUSAS),
                                AlofonoVocal(u'i̞', u'i', fonemas_siguientes_ipa=[u'r', u'x']),
                                AlofonoVocal(u'i̞', u'i', fonemas_previos_ipa=[u'r']),
                                AlofonoVocal(u'i', u'i'))
ALOFONOS_NUCLEO_ORALES[u'e'] = (AlofonoVocal(u'ɛ', u'e', fonemas_siguientes_ipa=LIQUIDAS,
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                # OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ
                                AlofonoVocal(u'ɛ', u'e', fonemas_siguientes_ipa=[u'ɡ', u'k'],
                                             fonemas_postsiguientes_ipa=SOLIDAS + PAUSAS),
                                AlofonoVocal(u'ɛ', u'e', fonemas_siguientes_ipa=[u'i̯', u'r', u'x']),
                                AlofonoVocal(u'ɛ', u'e', fonemas_previos_ipa=[u'r']),
                                AlofonoVocal(u'e', u'e'))
ALOFONOS_NUCLEO_ORALES[u'a'] = (AlofonoVocal(u'ɑ', u'a', fonemas_siguientes_ipa=VOCOIDES_POSTERIORES + [u'x']),
                                AlofonoVocal(u'ɑ', u'a', fonemas_siguientes_ipa=[u'l'],
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'a', u'a'))
ALOFONOS_NUCLEO_ORALES[u'o'] = (AlofonoVocal(u'ɔ', u'o', fonemas_siguientes_ipa=NASALES,
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'ɔ', u'o', fonemas_siguientes_ipa=SEMIVOCALES,
                                             fonemas_postsiguientes_ipa=NASALES,
                                             fonemas_postpostsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'ɔ', u'o', fonemas_siguientes_ipa=[u'θ', u's', u'ʒ', u'ʃ', u'ɾ', u'l'],
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'ɔ', u'o', fonemas_siguientes_ipa=OCLUSIVAS + [u'f'],
                                             fonemas_postsiguientes_ipa=SOLIDAS + PAUSAS),
                                AlofonoVocal(u'ɔ', u'o', fonemas_siguientes_ipa=[u'i̯', u'r', u'x']),
                                AlofonoVocal(u'ɔ', u'o', fonemas_previos_ipa=[u'r']),
                                AlofonoVocal(u'ɔ', u'o', fonemas_previos_ipa=[u'a'],
                                             fonemas_siguientes_ipa=[u'ɾ'],
                                             fonemas_postsiguientes_ipa=VOCOIDES),
                                AlofonoVocal(u'o', u'o'))
ALOFONOS_NUCLEO_ORALES[u'u'] = (AlofonoVocal(u'u̞', u'u', fonemas_siguientes_ipa=NASALES,
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'u̞', u'u', fonemas_siguientes_ipa=SEMIVOCALES,
                                             fonemas_postsiguientes_ipa=NASALES,
                                             fonemas_postpostsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'u̞', u'u', fonemas_siguientes_ipa=[u'θ', u's', u'ʒ', u'ʃ', u'ɾ', u'l'],
                                             fonemas_postsiguientes_ipa=CONSONANTES + PAUSAS),
                                AlofonoVocal(u'u̞', u'u', fonemas_siguientes_ipa=OCLUSIVAS + [u'f'],
                                             fonemas_postsiguientes_ipa=SOLIDAS + PAUSAS),
                                AlofonoVocal(u'u̞', u'u', fonemas_siguientes_ipa=[u'r', u'x']),
                                AlofonoVocal(u'u̞', u'u', fonemas_previos_ipa=[u'r']),
                                AlofonoVocal(u'u', u'u'))
# Creamos las versiones de duración larga para las vocales orales.
for fonema_nucleo_ipa in list(ALOFONOS_NUCLEO_ORALES.keys()):
    alofonos_nucleo = ALOFONOS_NUCLEO_ORALES[fonema_nucleo_ipa]
    if isinstance(alofonos_nucleo[0], AlofonoVocal):
        for alofono_nucleo in alofonos_nucleo:
            fonema_ipa_largo = alofono_nucleo.get_fonema_padre_ipa() + u'ː'
            alofono_vocal_larga = deepcopy(alofono_nucleo)
            alofono_vocal_larga.set_alofono_ipa(alofono_nucleo.get_alofono_ipa() + u'ː')
            alofono_vocal_larga.set_fonema_padre_ipa(fonema_ipa_largo)
            ALOFONOS_NUCLEO_ORALES.setdefault(fonema_ipa_largo, []).append(alofono_vocal_larga)
# Deslizantes
ALOFONOS_NUCLEO_ORALES[u'i̯'] = (AlofonoSemivocal(u'i̯', u'i̯'), )
ALOFONOS_NUCLEO_ORALES[u'u̯'] = (AlofonoSemivocal(u'u̯', u'u̯'), )
ALOFONOS_NUCLEO_ORALES[u'j'] = (AlofonoSemiconsonante(u'j', u'j'), )
ALOFONOS_NUCLEO_ORALES[u'w'] = (AlofonoSemiconsonante(u'w', u'w'), )


# En código como en silaba, vocaliza_semiconsonante y semivocal se considera que la abierta es la última.
ALOFONOS_NUCLEO_NASALES = dict()
# Vocales
ALOFONOS_NUCLEO_NASALES[u'i'] = (AlofonoVocal(u'ĩ', u'i', fonemas_siguientes_ipa=NASALES,
                                              fonemas_postsiguientes_ipa=VOCOIDES),
                                 AlofonoVocal(u'ĩ̞', u'i'))
ALOFONOS_NUCLEO_NASALES[u'e'] = (AlofonoVocal(u'ẽ', u'e'), )
ALOFONOS_NUCLEO_NASALES[u'a'] = (AlofonoVocal(u'ã', u'a'), )
ALOFONOS_NUCLEO_NASALES[u'o'] = (AlofonoVocal(u'õ', u'o', fonemas_siguientes_ipa=NASALES,
                                              fonemas_postsiguientes_ipa=VOCOIDES),
                                 AlofonoVocal(u'õ', u'o', fonemas_siguientes_ipa=SEMIVOCALES,
                                              fonemas_postsiguientes_ipa=NASALES,
                                              fonemas_postpostsiguientes_ipa=VOCOIDES),
                                 AlofonoVocal(u'ɔ̃', u'o'))
ALOFONOS_NUCLEO_NASALES[u'u'] = (AlofonoVocal(u'ũ', u'u', fonemas_siguientes_ipa=NASALES,
                                              fonemas_postsiguientes_ipa=VOCOIDES),
                                 AlofonoVocal(u'ũ̞', u'u'))
# Creamos las versiones de duración larga para las vocales nasales.
for fonema_nucleo_ipa in list(ALOFONOS_NUCLEO_NASALES.keys()):
    alofonos_nucleo = ALOFONOS_NUCLEO_NASALES[fonema_nucleo_ipa]
    if isinstance(alofonos_nucleo[0], AlofonoVocal):
        for alofono_nucleo in alofonos_nucleo:
            fonema_ipa_largo = alofono_nucleo.get_fonema_padre_ipa() + u'ː'
            alofono_vocal_larga = deepcopy(alofono_nucleo)
            alofono_vocal_larga.set_alofono_ipa(alofono_nucleo.get_alofono_ipa() + u'ː')
            alofono_vocal_larga.set_fonema_padre_ipa(fonema_ipa_largo)
            ALOFONOS_NUCLEO_NASALES.setdefault(fonema_ipa_largo, []).append(alofono_vocal_larga)
# Deslizantes
ALOFONOS_NUCLEO_NASALES[u'i̯'] = (AlofonoSemivocal(u'ĩ̯', u'i̯'), )
ALOFONOS_NUCLEO_NASALES[u'u̯'] = (AlofonoSemivocal(u'ũ̯', u'u̯'), )
ALOFONOS_NUCLEO_NASALES[u'j'] = (AlofonoSemiconsonante(u'j̃', u'j'), )
ALOFONOS_NUCLEO_NASALES[u'w'] = (AlofonoSemiconsonante(u'w̃', u'w'), )
