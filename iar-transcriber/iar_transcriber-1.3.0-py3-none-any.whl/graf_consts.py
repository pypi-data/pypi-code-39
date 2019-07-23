#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Crea los diccionario constantes DIGRAFOS y MONOGRAFOS, utilizados en otras clases, y la auxiliar TILDES_OPUESTAS.

Ambos diccionarios tienen como claves el string con el/los carácter(es) del grafema (monógrafo o dígrafo),
y como contenido tienen una tupla que contiene uno o más posibles objetos Grafema, cada uno representando
a uno o más fonemas.

Los grafemas se incluyen en el diccionario tanto en mayúsculas como en minúsculas (o en cualquier combinación
en los dígrafos) para no tener que preocuparse por el tipo de carácter usado y encontrarlo siempre en el
diccionario.

Teniendo en cuenta lo anterior, MONOGRAFOS incluye 152 caracteres distintos, y DIGRAFOS 28. El resto serán
grafemas desconocidos.
"""

from copy import deepcopy

from iar_transcriber.grafema import DigrafoConsonante, MonografoConsonante, MonografoSemiconsonante, MonografoVocal,\
    MonografoSemivocal, MonografoMudo, MonografoPausa, MonografoSimbolo, MonografoNumero, MonografoOrdinal

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"

# Estructura auxiliar para intercambiar entre grafema con y sin tilde
TILDES_OPUESTAS = {u'i': u'í', u'I': u'Í', u'í': u'i', u'Í': u'I',
                   u'e': u'é', u'E': u'É', u'é': u'e', u'É': u'E',
                   u'a': u'á', u'A': u'Á', u'á': u'a', u'Á': u'A',
                   u'o': u'ó', u'O': u'Ó', u'ó': u'o', u'Ó': u'O',
                   u'u': u'ú', u'U': u'Ú', u'ú': u'u', u'Ú': u'U'}

NTIL, TILD = False, True
MASC, FEME = False, True

# Dicionario DIGRAFOS
DIGRAFOS = dict()
# TODO: creo que podría añadir cosas como ps, pn, cn y cosas rarunas, para que psico ->/siko/.
DIGRAFOS[u'ch'] = (DigrafoConsonante(u'c', u'h', [u'ʧ'], u'che'),)
# OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (el 2º evita el lazo inferior)
DIGRAFOS[u'gu'] = (DigrafoConsonante(u'g', u'u', [u'ɡ'], u'ge ú'),)
DIGRAFOS[u'll'] = (DigrafoConsonante(u'l', u'l', [u'ʎ'], u'elle'),
                   DigrafoConsonante(u'l', u'l', [u'l'], u'elle'))
DIGRAFOS[u'qu'] = (DigrafoConsonante(u'q', u'u', [u'k'], u'cu ú'),)
DIGRAFOS[u'rr'] = (DigrafoConsonante(u'r', u'r', [u'r'], u'erre doble'),)
DIGRAFOS[u'tx'] = (DigrafoConsonante(u't', u'x', [u'ʧ'], u'té equis'),)  # Préstamos vascos
DIGRAFOS[u'tz'] = (DigrafoConsonante(u't', u'z', [u'ʧ'], u'té ceta'),)  # Préstamos vascos

# Para cada dígrafo, creamos las otras tres combinaciones de mayúscula/minúscula
for letras in list(DIGRAFOS.keys()):
    for variante_de_grafema in DIGRAFOS[letras]:
        # Los dígrafos son siempre consonantes, así que todos los objetos son de tipo DigrafoConsonante
        # Creamos las tres variaciones: M-m, m-M y M-M. Se mantienen los fonemas y el deletreo.
        for primario, secundario in [(letras[0].upper(), letras[1]),
                                     (letras[0], letras.upper()[1]),
                                     (letras[0].upper(), letras[1].upper())]:
            digrafo_mayusculo = deepcopy(variante_de_grafema)
            digrafo_mayusculo.set_grafema_primario(primario)
            digrafo_mayusculo.set_grafema_secundario(secundario)
            DIGRAFOS[primario + secundario] = tuple(list(DIGRAFOS.setdefault(primario + secundario, [])) +
                                                    [digrafo_mayusculo])


# Diccionario MONOGRAFOS
MONOGRAFOS = dict()
# Primero añadimos los caracteres alfabéticos, que tienen versiones en minúscula y mayúscula
# Vocales, semivocales y semiconsonantes
MONOGRAFOS[u'í'] = (MonografoVocal(u'í', [u'i'], u'í', TILD),)
MONOGRAFOS[u'i'] = (MonografoVocal(u'i', [u'i'], u'í', NTIL),
                    MonografoSemivocal(u'i', [u'i̯'], u'í'),
                    MonografoSemiconsonante(u'i', [u'j'], u'í'),
                    MonografoConsonante(u'i', [u'ʝ̞'], u'í'))  # Consonante aproximante.
MONOGRAFOS[u'y'] = (MonografoVocal(u'y', [u'i'], u'í griega', NTIL),
                    MonografoSemivocal(u'y', [u'i̯'], u'í griega'),
                    MonografoConsonante(u'y', [u'ʝ̞'], u'í griega'))  # Consonante aproximante.
MONOGRAFOS[u'&'] = (MonografoVocal(u'&', [u'i'], u'í', NTIL),  # Se considera <&> como equivalente a <y>
                    MonografoSemivocal(u'&', [u'i̯'], u'í griega'),
                    MonografoConsonante(u'&', [u'ʝ̞'], u'í griega'))  # Consonante aproximante.
MONOGRAFOS[u'é'] = (MonografoVocal(u'é', [u'e'], u'é', TILD),)
MONOGRAFOS[u'e'] = (MonografoVocal(u'e', [u'e'], u'é', NTIL),)
MONOGRAFOS[u'á'] = (MonografoVocal(u'á', [u'a'], u'á', TILD),)
MONOGRAFOS[u'a'] = (MonografoVocal(u'a', [u'a'], u'á', NTIL),)
MONOGRAFOS[u'ó'] = (MonografoVocal(u'ó', [u'o'], u'ó', TILD),)
MONOGRAFOS[u'o'] = (MonografoVocal(u'o', [u'o'], u'ó', NTIL),)
MONOGRAFOS[u'ú'] = (MonografoVocal(u'ú', [u'u'], u'ú', TILD),)
MONOGRAFOS[u'u'] = (MonografoVocal(u'u', [u'u'], u'ú', NTIL),
                    MonografoSemivocal(u'u', [u'u̯'], u'ú'),
                    MonografoSemiconsonante(u'u', [u'w'], u'ú'),
                    # OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (el 2º evita el lazo inferior)
                    MonografoConsonante(u'u', [u'ɡ', u'w'], u'ú'))  # EXCEPCIÓN: doble fonema
MONOGRAFOS[u'ü'] = (MonografoVocal(u'ü', [u'u'], u'ú', NTIL),  # Añadido artificial para procesar bien führer
                    MonografoSemiconsonante(u'ü', [u'w'], u'ú'),
                    MonografoSemivocal(u'ü', [u'u̯'], u'ú'),  # Añadido artificial para procesar bien cosas como Tahür
                    # OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (el 2º evita el lazo inferior)
                    MonografoConsonante(u'ü', [u'ɡ', u'w'], u'ú'))  # EXCEPCIÓN: doble fonema. Añadido artificial: hüa
# Consonantes
# Nasales
MONOGRAFOS[u'm'] = (MonografoConsonante(u'm', [u'm'], u'eme'),)
MONOGRAFOS[u'n'] = (MonografoConsonante(u'n', [u'n'], u'ene'),)
MONOGRAFOS[u'ñ'] = (MonografoConsonante(u'ñ', [u'ɲ'], u'eñe'),)
# Oclusivas
MONOGRAFOS[u'b'] = (MonografoConsonante(u'b', [u'b'], u'be'),)
MONOGRAFOS[u'v'] = (MonografoConsonante(u'v', [u'b'], u'uve'),)
# OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (el 2º evita el lazo inferior)
MONOGRAFOS[u'w'] = (MonografoConsonante(u'w', [u'ɡ', u'w'], u'uve doble'),
                    MonografoConsonante(u'w', [u'b'], u'uve doble'))
MONOGRAFOS[u'p'] = (MonografoConsonante(u'p', [u'p'], u'pe'),)
MONOGRAFOS[u'd'] = (MonografoConsonante(u'd', [u'd'], u'dé'),)
MONOGRAFOS[u't'] = (MonografoConsonante(u't', [u't'], u'té'),)
# OJO: el carácter del grafema g es distinto del del fonema ɡ (el 2º evita el lazo inferior)
MONOGRAFOS[u'g'] = (MonografoConsonante(u'g', [u'ɡ'], u'ge'),
                    MonografoConsonante(u'g', [u'x'], u'ge'))
MONOGRAFOS[u'k'] = (MonografoConsonante(u'k', [u'k'], u'ca'),)
MONOGRAFOS[u'c'] = (MonografoConsonante(u'c', [u'k'], u'ce'),
                    MonografoConsonante(u'c', [u'θ'], u'ce'))
MONOGRAFOS[u'ç'] = (MonografoConsonante(u'ç', [u's'], u'ce con cedilla'),)  # Préstamos catalanes
MONOGRAFOS[u'q'] = (MonografoConsonante(u'q', [u'k'], u'cu'),)
# Fricativas
MONOGRAFOS[u'f'] = (MonografoConsonante(u'f', [u'f'], u'efe'),)
MONOGRAFOS[u'z'] = (MonografoConsonante(u'z', [u'θ'], u'ceta'),)
MONOGRAFOS[u's'] = (MonografoConsonante(u's', [u's'], u'ese'),)
MONOGRAFOS[u'x'] = (MonografoConsonante(u'x', [u's'], u'equis'),
                    MonografoConsonante(u'x', [u'k'], u'equis'),
                    MonografoConsonante(u'x', [u'k', u's'], u'equis'))  # EXCEPCIÓN: doble fonema
MONOGRAFOS[u'j'] = (MonografoConsonante(u'j', [u'x'], u'jota'),)
# Laterales
MONOGRAFOS[u'l'] = (MonografoConsonante(u'l', [u'l'], u'ele'),
                    MonografoConsonante(u'l', [u'ʎ'], u'ele'))  # Por cosas como polllo, para que dé /poʎ:o/
# Vibrantes
MONOGRAFOS[u'r'] = (MonografoConsonante(u'r', [u'r'], u'erre'),
                    MonografoConsonante(u'r', [u'ɾ'], u'erre'))
# Muda
MONOGRAFOS[u'h'] = (MonografoMudo(u'h', [], u'hache'),)

# Hacemos las versiones en mayúsculas de los monógrafos alfabéticos (los que llevamos incluidos hasta ahora).
for letra in list(MONOGRAFOS.keys()):
    if letra == u'&':
        # El grafema <&> no es alfabético y no tiene mayúscula.
        continue
    for variante_de_grafema in MONOGRAFOS[letra]:
        # Creamos la variante, que es una copia (deep) de la variante original, a la que cambiamos el grafema
        # primario para ponerlo en mayúsculas.
        monografo_mayusculo = deepcopy(variante_de_grafema)
        monografo_mayusculo.set_grafema_primario(letra.upper())
        MONOGRAFOS[letra.upper()] = tuple(list(MONOGRAFOS.setdefault(letra.upper(), [])) + [monografo_mayusculo])

# Añadimos los monógrafos mudos no alfabéticos. Hay muchos posibles caracteres (distintos) de guion,
# que se decide que no tengan deletreo porque usualmente solo separan dos términos o están a inicio de párrafo.
MONOGRAFOS[u'-'] = (MonografoMudo(u'-', [], u''),)  # Son guiones distintos
MONOGRAFOS[u'­'] = (MonografoMudo(u'­', [], u''),)  # Son guiones distintos
MONOGRAFOS[u'–'] = (MonografoMudo(u'–', [], u''),)  # Son guiones distintos
MONOGRAFOS[u'‒'] = (MonografoMudo(u'‒', [], u''),)  # Son guiones distintos
MONOGRAFOS[u'−'] = (MonografoMudo(u'−', [], u''),)  # Son guiones distintos
MONOGRAFOS[u'—'] = (MonografoMudo(u'—', [], u''),)  # Son guiones distintos
MONOGRAFOS[u'―'] = (MonografoMudo(u'―', [], u''),)  # Son guiones distintos
MONOGRAFOS[u'_'] = (MonografoMudo(u'_', [], u'guion bajo'),)
MONOGRAFOS[u'•'] = (MonografoMudo(u'•', [], u'punto'),)
MONOGRAFOS[u'·'] = (MonografoMudo(u'·', [], u'punto'),)

# Se añaden otros mudos relacionados con las comillas
MONOGRAFOS[u'"'] = (MonografoMudo(u'"', [], u'comillas'),)
MONOGRAFOS[u'“'] = (MonografoMudo(u'“', [], u'abre comillas'),)
MONOGRAFOS[u'„'] = (MonografoMudo(u'„', [], u'abre comillas'),)
MONOGRAFOS[u'”'] = (MonografoMudo(u'”', [], u'cierra comillas'),)
MONOGRAFOS[u'«'] = (MonografoMudo(u'«', [], u'abre comillas'),)
MONOGRAFOS[u'»'] = (MonografoMudo(u'»', [], u'cierra comillas'),)
MONOGRAFOS[u"'"] = (MonografoMudo(u"'", [], u'comilla'),)
MONOGRAFOS[u'‘'] = (MonografoMudo(u'‘', [], u'abre comilla'),)
MONOGRAFOS[u'’'] = (MonografoMudo(u'’', [], u'cierra comilla'),)
MONOGRAFOS[u'`'] = (MonografoMudo(u'`', [], u'tilde grave'),)
MONOGRAFOS[u'´'] = (MonografoMudo(u'´', [], u'tilde aguda'),)
MONOGRAFOS[u'́'] = (MonografoMudo(u'́', [], u'tilde aguda'),)
MONOGRAFOS[u'¨'] = (MonografoMudo(u'¨', [], u'diéresis'),)
MONOGRAFOS[u'^'] = (MonografoMudo(u'^', [], u'tilde circunfleja'),)
MONOGRAFOS[u'~'] = (MonografoMudo(u'~', [], u'vírgula'),)
MONOGRAFOS[u'‹'] = (MonografoMudo(u'‹', [], u'abre comilla'),)
MONOGRAFOS[u'›'] = (MonografoMudo(u'›', [], u'cierra comilla'),)
MONOGRAFOS[u'<'] = (MonografoMudo(u'<', [], u'menor que'),)
MONOGRAFOS[u'>'] = (MonografoMudo(u'>', [], u'mayor que'),)

# Se añaden los símbolos, que siempre se deletrearán
MONOGRAFOS[u'%'] = (MonografoSimbolo(u'%', [], u'por ciento'),)
MONOGRAFOS[u'©'] = (MonografoSimbolo(u'©', [], u'copirait'),)
MONOGRAFOS[u'®'] = (MonografoSimbolo(u'®', [], u'marca registrada'),)
MONOGRAFOS[u'*'] = (MonografoSimbolo(u'*', [], u'asterisco'),)
MONOGRAFOS[u'='] = (MonografoSimbolo(u'=', [], u'igual'),)
MONOGRAFOS[u'×'] = (MonografoSimbolo(u'×', [], u'por'),)
MONOGRAFOS[u'+'] = (MonografoSimbolo(u'+', [], u'más'),)
MONOGRAFOS[u'±'] = (MonografoSimbolo(u'±', [], u'más menos'),)
MONOGRAFOS[u'^'] = (MonografoSimbolo(u'^', [], u'elevado a'),)
MONOGRAFOS[u'@'] = (MonografoSimbolo(u'@', [], u'arroba'),)
MONOGRAFOS[u'#'] = (MonografoSimbolo(u'#', [], u'almohadilla'),)
MONOGRAFOS[u'$'] = (MonografoSimbolo(u'$', [], u'dólares'),)
MONOGRAFOS[u'€'] = (MonografoSimbolo(u'€', [], u'euros'),)
MONOGRAFOS[u'£'] = (MonografoSimbolo(u'£', [], u'libras'),)
MONOGRAFOS[u'¥'] = (MonografoSimbolo(u'¥', [], u'yenes'),)
MONOGRAFOS[u'§'] = (MonografoSimbolo(u'§', [], u'sección'),)
MONOGRAFOS[u'½'] = (MonografoSimbolo(u'½', [], u'un medio'),)
MONOGRAFOS[u'¾'] = (MonografoSimbolo(u'¾', [], u'tres cuartos'),)
MONOGRAFOS[u'Ð'] = (MonografoSimbolo(u'Ð', [], u'de'),)

# Pausas, tanto caracteres blancos como signos ortográficos que implican pausa
MONOGRAFOS[u'\t'] = (MonografoPausa(u'\t', [u'‖'], u''),)
MONOGRAFOS[u'\n'] = (MonografoPausa(u'\n', [u'‖'], u''),)
MONOGRAFOS[u'\r'] = (MonografoPausa(u'\r', [u'‖'], u''),)
MONOGRAFOS[u'\f'] = (MonografoPausa(u'\f', [u'‖'], u''),)
MONOGRAFOS[u'\v'] = (MonografoPausa(u'\v', [u'‖'], u''),)

MONOGRAFOS[u'.'] = (MonografoPausa(u'.', [u'‖'], u'punto'),)
MONOGRAFOS[u':'] = (MonografoPausa(u':', [u'‖'], u'dos puntos'),)
MONOGRAFOS[u'…'] = (MonografoPausa(u'…', [u'‖'], u'puntos suspensivos'),)
MONOGRAFOS[u';'] = (MonografoPausa(u';', [u'‖'], u'punto y coma'),)
MONOGRAFOS[u'¿'] = (MonografoPausa(u'¿', [u'‖'], u'abre interrogación'),)
MONOGRAFOS[u'?'] = (MonografoPausa(u'?', [u'‖'], u'cierra interrogación'),)
MONOGRAFOS[u'¡'] = (MonografoPausa(u'¡', [u'‖'], u'abre exclamación'),)
MONOGRAFOS[u'!'] = (MonografoPausa(u'!', [u'‖'], u'cierra exclamación'),)
MONOGRAFOS[u','] = (MonografoPausa(u',', [u'|'], u'coma'),)
MONOGRAFOS[u'('] = (MonografoPausa(u'(', [u'|'], u'abre paréntesis'),)
MONOGRAFOS[u')'] = (MonografoPausa(u')', [u'|'], u'cierra paréntesis'),)
MONOGRAFOS[u'['] = (MonografoPausa(u'[', [u'|'], u'abre corchete'),)
MONOGRAFOS[u']'] = (MonografoPausa(u']', [u'|'], u'cierra corchete'),)
MONOGRAFOS[u'{'] = (MonografoPausa(u'{', [u'|'], u'abre llave'),)
MONOGRAFOS[u'}'] = (MonografoPausa(u'}', [u'|'], u'cierra llave'),)
MONOGRAFOS[u'/'] = (MonografoPausa(u'/', [u'|'], u'barra inclinada'),)
MONOGRAFOS[u'\\'] = (MonografoPausa(u'\\', [u'|'], u'barra invertida'),)
MONOGRAFOS[u'|'] = (MonografoPausa(u'|', [u'|'], u'barra vertical'),)

# Números
MONOGRAFOS[u'1'] = (MonografoNumero(u'1', [u''], u'uno'),)
MONOGRAFOS[u'2'] = (MonografoNumero(u'2', [u''], u'dos'),)
MONOGRAFOS[u'3'] = (MonografoNumero(u'3', [u''], u'tres'),)
MONOGRAFOS[u'4'] = (MonografoNumero(u'4', [u''], u'cuatro'),)
MONOGRAFOS[u'6'] = (MonografoNumero(u'6', [u''], u'cinco'),)
MONOGRAFOS[u'5'] = (MonografoNumero(u'5', [u''], u'seis'),)
MONOGRAFOS[u'7'] = (MonografoNumero(u'7', [u''], u'siete'),)
MONOGRAFOS[u'8'] = (MonografoNumero(u'8', [u''], u'ocho'),)
MONOGRAFOS[u'9'] = (MonografoNumero(u'9', [u''], u'nueve'),)
MONOGRAFOS[u'0'] = (MonografoNumero(u'0', [u''], u'cero'),)

# Marca de ordinal
MONOGRAFOS[u'°'] = (MonografoOrdinal(u'°', [u''], u'grados', MASC),)
MONOGRAFOS[u'º'] = (MonografoOrdinal(u'º', [u''], u'grados', MASC),)
MONOGRAFOS[u'ª'] = (MonografoOrdinal(u'ª', [u''], u'aría', FEME),)
