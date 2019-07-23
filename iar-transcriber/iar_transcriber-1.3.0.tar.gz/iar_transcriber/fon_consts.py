#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Crea el diccionario constante FONEMAS (que incluye todos los fonemas reconocidos por el sistema) y otras constantes

El diccionario FONEMAS consta de 60 objetos de la clase Fonema, de los cuales 2 son pausas, 31 son fonemas "propios"
(que incluye también 2 fricativas palatales propios de dialectos americanos), y 27 fonemas de duración larga.
Este diccionario es utilizado en muchas otras clases y es un elemento básico del sistema.

El resto de constantes tienen que ver con la descripción fonética de los distintos fonemas
"""

from copy import deepcopy

from iar_transcriber.fonema import Fonema, FonemaConsonante, FonemaSemiconsonante, FonemaVocal, FonemaSemivocal, FonemaPausa

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"

# Constantes de sonoridad
SORD, SONO = False, True
# Constantes de duración
CORT, LARG = 1, 2
# Constantes de abertura (vocoides)
ABIE, MEDI, CERR = 1, 2, 3
# Constantes de localización (vocoides)
ANTE, CENT, POST = 1, 2, 3
# Constantes de punto de articulación (consonantes)
BILA, LADE, INTD, DEAL, ALVE, POAL, PALA, VELA, UVUL, GLOT = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
# Constantes de modo de articulacion (consonantes)
NASA, OCLU, AFRI, FRIC, APRO, LATE, VIBM, VIBS = 1, 2, 3, 4, 5, 6, 7, 8

FONEMA_VACIO = Fonema()

# Diccionario FONEMAS
FONEMAS = dict()
# Primero los fonemas de vocoides
FONEMAS[u'i'] = FonemaVocal(u'i', ANTE, CERR)
FONEMAS[u'e'] = FonemaVocal(u'e', ANTE, MEDI)
FONEMAS[u'a'] = FonemaVocal(u'a', CENT, ABIE)
FONEMAS[u'o'] = FonemaVocal(u'o', POST, MEDI)
FONEMAS[u'u'] = FonemaVocal(u'u', POST, CERR)
FONEMAS[u'i̯'] = FonemaSemivocal(u'i̯', ANTE)
FONEMAS[u'u̯'] = FonemaSemivocal(u'u̯', POST)
FONEMAS[u'j'] = FonemaSemiconsonante(u'j', ANTE)
FONEMAS[u'w'] = FonemaSemiconsonante(u'w', POST)
# Después los fonemas de consonantes
FONEMAS[u'm'] = FonemaConsonante(u'm', NASA, BILA, SONO)
FONEMAS[u'n'] = FonemaConsonante(u'n', NASA, ALVE, SONO)
FONEMAS[u'ɲ'] = FonemaConsonante(u'ɲ', NASA, PALA, SONO)
FONEMAS[u'b'] = FonemaConsonante(u'b', OCLU, BILA, SONO)
FONEMAS[u'p'] = FonemaConsonante(u'p', OCLU, BILA, SORD)
FONEMAS[u'd'] = FonemaConsonante(u'd', OCLU, DEAL, SONO)
FONEMAS[u't'] = FonemaConsonante(u't', OCLU, DEAL, SORD)
# OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ
FONEMAS[u'ɡ'] = FonemaConsonante(u'ɡ', OCLU, VELA, SONO)
FONEMAS[u'k'] = FonemaConsonante(u'k', OCLU, VELA, SORD)
FONEMAS[u'ʤ'] = FonemaConsonante(u'ʤ', AFRI, POAL, SONO)
FONEMAS[u'ʧ'] = FonemaConsonante(u'ʧ', AFRI, POAL, SORD)
FONEMAS[u'f'] = FonemaConsonante(u'f', FRIC, LADE, SORD)
FONEMAS[u'θ'] = FonemaConsonante(u'θ', FRIC, INTD, SORD)
FONEMAS[u's'] = FonemaConsonante(u's', FRIC, ALVE, SORD)
FONEMAS[u'ʒ'] = FonemaConsonante(u'ʒ', FRIC, POAL, SONO)
FONEMAS[u'ʃ'] = FonemaConsonante(u'ʃ', FRIC, POAL, SORD)
FONEMAS[u'x'] = FonemaConsonante(u'x', FRIC, VELA, SORD)
FONEMAS[u'ʝ̞'] = FonemaConsonante(u'ʝ̞', APRO, PALA, SONO)
FONEMAS[u'l'] = FonemaConsonante(u'l', LATE, ALVE, SONO)
FONEMAS[u'ʎ'] = FonemaConsonante(u'ʎ', LATE, PALA, SONO)
FONEMAS[u'r'] = FonemaConsonante(u'r', VIBM, ALVE, SONO)
FONEMAS[u'ɾ'] = FonemaConsonante(u'ɾ', VIBS, ALVE, SONO)

FONEMAS[u'|'] = FonemaPausa(u'|', CORT)
FONEMAS[u'‖'] = FonemaPausa(u'‖', LARG)

# Creamos las versiones largas de los fonemas vocálicos y consonánticos
for fonema_ipa in list(FONEMAS.keys()):
    fonema = FONEMAS[fonema_ipa]
    if isinstance(fonema, FonemaVocal) or isinstance(fonema, FonemaConsonante):
        fonema = deepcopy(FONEMAS[fonema_ipa])
        fonema.set_fonema_ipa(fonema_ipa + u'ː')
        FONEMAS[fonema_ipa + u'ː'] = fonema
