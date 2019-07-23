#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Define la constante PALABRAS_ATONAS, un listado de las palabras átonas (sin ninguna sílaba tónica) según la RAE.
"""

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"

# La constante PALABRAS_ATONAS contiene las representaciones como string de las palabras sin sílabas tónicas.

# Quito "luego" porque normalmente no es conjunción sino adverbio. Dudas: ¿Siquiera? ¿mientras? ¿incluso?
CONJUNCIONES = u'e empero mas ni o ora pero sino u y aunque como conque entonces ergo porque pues que si'.split()
# "Según" es tónico, "vía" normalmente es nombre y "cabe" la he quitado (no cabe). Además se añaden otras menos
# comunes como "pro" y "versus", además de las más "recientes" como son "durante" y "mediante".
PREPOSICIONES = u'a ante bajo con contra de desde durante en entre hacia hasta mediante para por pro ' \
                u'sin so sobre tras versus'.split()  # ¿Según? No ¿Vía?
ARTICULOS = u'el la los las al del'.split()
ADJETIVOS_POSESIVOS = u'mi mis tu tus su sus'.split()
PRONOMBRES = u'me te se lo le les nos os'.split()
# Cual y cuales no son átonos
PRONOMBRES_RELATIVOS = u'que quien quienes cuyo cuyos cuya cuyas'.split()
# como, cuando y donde pueden ser preposiciones: te lo digo como amigo, cuando la guerra, donde tu hermano
ADVERBIOS = u'aun donde cuando cuanto muy no tan'.split()  # Juana y más gente opina que "muy" es tónico.
OTROS = u'doña fray san sor'.split()  # No sé bien por qué metí "cada", pero lo saco
PALABRAS_ATONAS = set(CONJUNCIONES + PREPOSICIONES + ARTICULOS + ADJETIVOS_POSESIVOS +
                      PRONOMBRES + PRONOMBRES_RELATIVOS + ADVERBIOS + OTROS)
