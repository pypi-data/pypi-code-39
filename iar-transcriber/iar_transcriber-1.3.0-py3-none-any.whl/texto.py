#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Texto, que representa la estructura (en objetos Frase) de una Texto.

Esta clase tiene una funcionalidad restringida, y en su mayor parte se tienen métodos que hacen llamadas a
métodos de la clase Frase. Además tiene un método que proporciona recuentos de aparición de los distintos
fonemas y alófonos, así como de sus combinaciones en sílabas.
"""

from iar_tokenizer import Tokenizer
from iar_transcriber.frase import Frase
from iar_transcriber.sil_consts import ACPR, ACSC

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Texto:
    u"""La clase Texto es una representación estructurada (en objetos Frase) de un texto.

    En esta clase se divide un texto (representado por un string) en frases, creándose un objeto Frase
    para cada una de ellas. También permite realizar recuentos de aparición de los fonemas/alófonos y tipos
    de sílaba.
    """

    def __init__(self, texto, resilabea=True, calcula_alofonos=True,
                 inserta_epentesis=False, organiza_grafemas=False):
        u"""Constructor para la clase Texto.

        En la clase Texto tenemos una lista de objetos Frase, y además guardamos el propio string de texto.

        :type texto: unicode
        :param texto: La cadena de caracteres que representa el texto
        :type resilabea: bool
        :param resilabea: Si está a True se realiza el resilabeo de las frases
        :type calcula_alofonos: bool
        :param calcula_alofonos: Si está a True se calculan los alófonos, si no sólo calculamos los fonemas
        :type inserta_epentesis: bool
        :param inserta_epentesis: Si está a True se inserta una /e/ epentética ante ataques complejos comenzados por /s/
        :type organiza_grafemas: bool
        :param organiza_grafemas: Si está a True, se crea la estructura de grafemas de la palabra, de cara a hacer una
            transcripción ortográfica
        """
        self._texto = texto
        frases_enteras_texto = Tokenizer.segmenta_por_frases(texto, elimina_separadores=False,
                                                             elimina_separadores_blancos=True,
                                                             adjunta_separadores=True)
        self._frases = []
        for frase_entera_texto in frases_enteras_texto:
            self._frases += [Frase(frase_entera_texto, resilabea, calcula_alofonos,
                                   inserta_epentesis, organiza_grafemas)]

    def resilabea(self, calcula_alofonos):
        u"""Resilabea las frases del texto

        :return: None
        """
        for frase in self._frases:
            frase.resilabea(calcula_alofonos)

    def get_frases(self):
        u"""Devuelve la lista de objetos Frase que contiene este objeto Texto

        :rtype: [Frase]
        :return: La lista de objetos Frase que representan las frases de este Texto
        """
        return self._frases

    def get_palabras(self):
        u"""Devuelve la lista de objetos Palabra que contiene este objeto Texto

        :rtype: [Palabra]
        :return: La lista de objetos Palabra que representan las palabras de este Texto
        """
        return [palabra for frase in self._frases for palabra in frase.get_palabras()]

    def get_silabas(self):
        u"""Devuelve la lista de objetos Silaba que contiene este objeto Texto

        :rtype: [Silaba]
        :return: La lista de objetos Silaba que representan las sílabas de este Texto
        """
        return [sil for frase in self._frases for pal in frase.get_palabras() for sil in pal.get_silabas()]

    def get_fonemas(self, incluye_pausas=False):
        u"""Devuelve la lista de objetos Fonema que contiene este objeto Texto

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluyen los fonemas de pausa. Si no, no.
        :rtype: [Fonema]
        :return: La lista de objetos Fonema que representan los fonemas de este Texto
        """
        return [fon for frase in self._frases for pal in frase.get_palabras()
                for sil in pal.get_silabas() for fon in sil.get_fonemas(incluye_pausas)]

    def get_alofonos(self, incluye_pausas=False):
        u"""Devuelve la lista de objetos Alofono que contiene este objeto Texto

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluyen los alófonos de pausa. Si no, no.
        :rtype: [Alofono]
        :return: La lista de objetos Alofono que representan los alófonos de este Texto
        """
        return [alo for frase in self._frases for pal in frase.get_palabras()
                for sil in pal.get_silabas() for alo in sil.get_alofonos(incluye_pausas)]

    def get_grafemas(self, incluye_pausas=False):
        u"""Devuelve la lista de objetos Grafema que contiene este objeto Texto

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluyen los grafemas de pausa. Si no, no.
        :rtype: [Grafema]
        :return: La lista de objetos Grafema que representan los grafemas de este Texto
        """
        return [graf for frase in self._frases for pal in frase.get_palabras()
                for sil in pal.get_silabas() for graf in sil.get_grafemas(incluye_pausas)]

    def transcribe_ortograficamente_texto(self, marca_tonica=False, separador=u'-', apertura=u'<', cierre=u'>'):
        u"""Se devuelve la transcripción ortográfica del texto, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type separador: unicode
        :param separador: Un string que se coloca entre sílabas
        :type apertura: unicode
        :param apertura: Un string que se coloca al inicio
        :type cierre: unicode
        :param cierre: Un string que se coloca al final
        :rtype: unicode
        :return: La transcripción ortográfica del texto, según los parámetros
        """
        transcripcion_texto = u''
        for orden_frase, frase in enumerate(self._frases):
            transcripcion_frase = frase.transcribe_ortograficamente_frase(marca_tonica=marca_tonica,
                                                                          incluye_pausas=True,
                                                                          separador=separador,
                                                                          apertura=u'',
                                                                          cierre=u'')
            if transcripcion_frase:
                transcripcion_texto += (u' ' if transcripcion_texto and
                                        transcripcion_texto[-1] not in u'\t\n\r\f\v' else u'') + transcripcion_frase
        return apertura + transcripcion_texto + cierre

    def transcribe_fonologicamente_texto(self, marca_tonica=True, transcribe_fonemas_aparentes=False,
                                         separador=u'.', apertura=u'/', cierre=u'/'):
        u"""Se devuelve la transcripción fonológica del texto, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type transcribe_fonemas_aparentes: bool
        :param transcribe_fonemas_aparentes: Si está a True se produce la "refonemización": si un alófono coincide
            con un fonema distinto al que lo originó, se devuelve el fonema con el que coincide el alófono.
            Esto afecta a las nasales, o a semivocales que se consonantizan. Así, con este parámetro a True, la
            transcripción fonológica de <convino> y <combino> es en ambos casos /kombino/.
        :type separador: unicode
        :param separador: Un string que se coloca entre sílabas
        :type apertura: unicode
        :param apertura: Un string que se coloca al inicio
        :type cierre: unicode
        :param cierre: Un string que se coloca al final
        :rtype: unicode
        :return: La transcripción fonológica (fonemas) del texto, según los parámetros
        """
        transcripcion_texto = u''
        for orden_frase, frase in enumerate(self._frases):
            transcripcion_frase = frase.transcribe_fonologicamente_frase(
                marca_tonica=marca_tonica,
                incluye_pausa_previa=False,
                incluye_pausa_posterior=orden_frase < len(self._frases) - 1,
                transcribe_fonemas_aparentes=transcribe_fonemas_aparentes,
                separador=separador,
                apertura=u'',
                cierre=u'')
            if transcripcion_frase:
                if transcripcion_texto:
                    if transcripcion_texto[-1] not in [u'|', u'‖']:
                        if not transcripcion_frase[0] in [u'|', u'‖']:
                            transcripcion_texto += separador  # Toca meter el separador
                    elif transcripcion_frase[0] in [u'|', u'‖']:
                        if transcripcion_frase[0] == u'‖':
                            transcripcion_texto = transcripcion_texto[:-1] + u'‖'
                        transcripcion_frase = transcripcion_frase[1:]
                elif transcripcion_frase[0] in [u'|', u'‖']:
                    transcripcion_frase = transcripcion_frase[1:]
                transcripcion_texto += transcripcion_frase
        # Cabe la posibilidad de tener textos raros como "Sí, ¿?", que se transcribe como /ˈsi|/, con una pausa,
        # porque el "¿?" final se convierte en una sílaba fonéticamente vacía (no conviene que la borremos, porque
        # quizá hagamos la transcripción ortográfica).
        if transcripcion_texto and transcripcion_texto[-1] in [u'|', u'‖']:
            transcripcion_texto = transcripcion_texto[:-1]
        return apertura + transcripcion_texto + cierre

    def transcribe_foneticamente_texto(self, marca_tonica=True, ancha=False,
                                       separador=u'.', apertura=u'[', cierre=u']'):
        u"""Se devuelve la transcripción fonética del texto, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type ancha: bool
        :param ancha: Si está a True se devuelve la transcripción ancha. Está a False se devuelve la transcripción
            estrecha (por defecto).
        :type separador: unicode
        :param separador: Un string que se coloca entre sílabas
        :type apertura: unicode
        :param apertura: Un string que se coloca al inicio
        :type cierre: unicode
        :param cierre: Un string que se coloca al final
        :rtype: unicode
        :return: el string con la transcripción fonética (alófonos) del texto, según los parámetros
        """
        transcripcion_texto = u''
        for orden_frase, frase in enumerate(self._frases):
            transcripcion_frase = frase.\
                transcribe_foneticamente_frase(marca_tonica=marca_tonica,
                                               incluye_pausa_previa=False,
                                               incluye_pausa_posterior=orden_frase < len(self._frases) - 1,
                                               ancha=ancha,
                                               separador=separador,
                                               apertura=u'',
                                               cierre=u'')
            if transcripcion_frase:
                if transcripcion_texto:
                    if transcripcion_texto[-1] not in [u'|', u'‖']:
                        if not transcripcion_frase[0] in [u'|', u'‖']:
                            transcripcion_texto += separador  # Toca meter el separador
                    elif transcripcion_frase[0] in [u'|', u'‖']:
                        if transcripcion_frase[0] == u'‖':
                            transcripcion_texto = transcripcion_texto[:-1] + u'‖'
                        transcripcion_frase = transcripcion_frase[1:]
                elif transcripcion_frase[0] in [u'|', u'‖']:
                    transcripcion_frase = transcripcion_frase[1:]
                transcripcion_texto += transcripcion_frase
        # Cabe la posibilidad de tener textos raros como "Sí, ¿?", que se transcribe como [ˈsi|], con una pausa,
        # porque el "¿?" final se convierte en una sílaba fonéticamente vacía (no conviene que la borremos, porque
        # quizá hagamos la transcripción ortográfica).
        if transcripcion_texto and transcripcion_texto[-1] in [u'|', u'‖']:
            transcripcion_texto = transcripcion_texto[:-1]
        return apertura + transcripcion_texto + cierre

    def get_estadisticas_segmentos_y_silabas(self, estadisticas_segmentos=None, estadisticas_silabas=None):
        u"""Se devuelven dos estructuras de datos con estadísticas sobre aspectos fonéticos del texto.

        La estructura de datos que se crea aparece en el esquema de más abajo. Ambas son muy parecidas.
        Para los segmentos, se tiene un campo +len de total agregado, y una serie de subdiccionarios para
        el ataque, el núcleo y la coda. Cada uno de estos diccionarios contiene a su vez un agregado +len y
        tantos elementos como fonemas distintos haya en esa posición. Esos elementos son de nuevo diccionarios
        con un total agregado +len y tantos elementos como alófonos tenga ese fonema en esa posición.
        De nuevo, esos elementos son diccionarios, que esta vez tienen únicamente recuentos de apariciones
        en sílabas átonas y tónicas (y el agregado +len).

        Se puede ejemplificar así (los ejemplos vienen con grafemas como "ñ", pero los índices son fonemas IPA.)

        a = {"+len": X,
             "ata":
                {"+len": X,
                 "n":
                    {"+len": X,
                     "n": {"+len": total, "ato": recuento, "ton": recuento},
                     "m": {"+len": total, "ato": recuento, "ton": recuento},
                     "ñ": {"+len": total, "ato": recuento, "ton": recuento},
                     ...
                    },
                 "s":
                    {"+len": X,
                     "s": {"+len": total, "ato": recuento, "ton": recuento},
                     "s:": {"+len": total, "ato": recuento, "ton": recuento},
                     ...
                    },
                 ...
                },
             "nuc":
                {"+len": X,
                 "a":
                    {"+len": X,
                     "a": {"+len": total, "ato": recuento, "ton": recuento},
                     ...
                    },
                 ...
                },
             "cod":
                {"+len": X,
                 ...
                }
            }

        En cuanto a los recuentos de sílabas se tiene una estructura homóloga. En vez de tener posiciones
        en la sílaba, ahora se tienen campos que indican el tipo de sílaba (en formato CCSVSCC), con
        elementos que son diccionarios con elementos que representan fonológicamente las distintas sílabas
        encontradas, y cada uno tiene un elemento por combinación alofónica de esos fonemas de la sílaba,
        y finalmente tenemos los recuentos en átonas y tónicas.

        a = {"+len": X,
             "CVC":
                {"+len": X,
                 "den":
                    {"+len": X,
                     "den": {"+len": total, "ato": recuento, "ton": recuento},
                     "dem": {"+len": total, "ato": recuento, "ton": recuento},
                     "deñ": {"+len": total, "ato": recuento, "ton": recuento},
                     ...
                    },
                 "din":
                    {"+len": X,
                     "din": {"+len": total, "ato": recuento, "ton": recuento},
                     "dim": {"+len": total, "ato": recuento, "ton": recuento},
                     "diñ": {"+len": total, "ato": recuento, "ton": recuento},
                     ...
                    },
                 ...
                },
             "CCV":
                {"+len": X,
                 "tra":
                    {"+len": X,
                     "tra": {"+len": total, "ato": recuento, "ton": recuento},
                     ...
                    },
                 ...
                },
            }

        :type estadisticas_segmentos: {}
        :param estadisticas_segmentos: Si no está vacío, da el resultado previo de hacer un recuento
            de segmentos. Añadiremos las estadísticas de este texto a estas estadísticas previas.
        :type estadisticas_silabas: {}
        :param estadisticas_silabas: Si no está vacío, da el resultado previo de hacer un recuento
            de sílabas. Añadiremos las estadísticas de este texto a estas estadísticas previas.
        :rtype: ({}, {})
        :return: las estructuras de datos con los recuentos de segmentos y de sílabas.
        """
        if not estadisticas_segmentos:
            # No se partía de un recuento previo. Creamos la estructura de datos
            estadisticas_segmentos = {"+len": 0, "ata": {"+len": 0}, "nuc": {"+len": 0}, "cod": {"+len": 0}}
        if not estadisticas_silabas:
            # No se partía de un recuento previo. Creamos la estructura de datos
            estadisticas_silabas = {"+len": 0}

        # A contar...
        for frase in self._frases:
            for palabra in frase.get_palabras():
                for silaba in palabra.get_silabas():
                    # Contabilizamos acentos primarios y secundarios como "tónicas"
                    tonicidad = "ton" if (silaba.get_tonica() == ACPR or silaba.get_tonica() == ACSC) else "ato"
                    # Extraemos los alófonos de la palabra en cada una de sus tres posiciones de ataque, núcleo y coda
                    alofonos_y_posiciones = [(alofono, "ata") for alofono in silaba.get_alofonos_ataque()]
                    alofonos_y_posiciones += [(alofono, "nuc") for alofono in silaba.get_alofonos_nucleo()]
                    alofonos_y_posiciones += [(alofono, "cod") for alofono in silaba.get_alofonos_coda()]
                    # Para cada posición, añadimos los datos al diccionario del recuento
                    for (alofono, posicion) in alofonos_y_posiciones:
                        fonema_ipa = alofono.get_fonema_padre_ipa()
                        alofono_ipa = alofono.get_alofono_ipa()
                        if not fonema_ipa or not alofono_ipa:
                            continue
                        if fonema_ipa not in estadisticas_segmentos[posicion]:
                            # No habíamos encontrado aún este fonema para esta posición. Creamos la estructura
                            estadisticas_segmentos[posicion][fonema_ipa] = {"+len": 0}
                        if alofono_ipa not in estadisticas_segmentos[posicion][fonema_ipa]:
                            # No habíamos encontrado aún este alófono para esta posición. Creamos la estructura
                            estadisticas_segmentos[posicion][fonema_ipa][alofono_ipa] = {"+len": 0, "ton": 0, "ato": 0}
                        # Añadimos los recuentos en su posición exacta y actualizamos los agregados
                        estadisticas_segmentos[posicion][fonema_ipa][alofono_ipa][tonicidad] += 1
                        estadisticas_segmentos[posicion][fonema_ipa][alofono_ipa]["+len"] += 1
                        estadisticas_segmentos[posicion][fonema_ipa]["+len"] += 1
                        estadisticas_segmentos[posicion]["+len"] += 1
                        estadisticas_segmentos["+len"] += 1

                    # Vemos qué tipo de sílaba tenemos
                    tipo_silaba = ("C" * len(silaba.get_alofonos_ataque())) +\
                                  ("S" if silaba.get_fonema_semiconsonante() else "") + "V" +\
                                  ("S" if silaba.get_fonema_semivocal() else "") +\
                                  ("C" * len(silaba.get_alofonos_coda()))
                    if not tipo_silaba:
                        continue
                    if tipo_silaba not in estadisticas_silabas:
                        # La primera vez que vemos este tipo de sílaba: creamos la estructura en el diccionario
                        estadisticas_silabas[tipo_silaba] = {"+len": 0}
                    fonemas_ipa = silaba.transcribe_fonologicamente_silaba(marca_tonica=False,
                                                                           incluye_pausa_previa=False,
                                                                           incluye_pausa_posterior=False,
                                                                           transcribe_fonemas_aparentes=False)
                    if fonemas_ipa not in estadisticas_silabas[tipo_silaba]:
                        # La primera vez que vemos esta combinación de fonemas. Creamos la estructura.
                        estadisticas_silabas[tipo_silaba][fonemas_ipa] = {"+len": 0}
                    alofonos_ipa = silaba.transcribe_foneticamente_silaba(marca_tonica=False,
                                                                          incluye_pausa_previa=False,
                                                                          incluye_pausa_posterior=False)
                    if alofonos_ipa not in estadisticas_silabas[tipo_silaba][fonemas_ipa]:
                        # La primera vez que vemos esta combinación de alófonos. Creamos la estructura.
                        estadisticas_silabas[tipo_silaba][fonemas_ipa][alofonos_ipa] = {"+len": 0, "ton": 0, "ato": 0}
                    # Añadimos los recuentos en su posición exacta y actualizamos los agregados
                    estadisticas_silabas[tipo_silaba][fonemas_ipa][alofonos_ipa][tonicidad] += 1
                    estadisticas_silabas[tipo_silaba][fonemas_ipa][alofonos_ipa]["+len"] += 1
                    estadisticas_silabas[tipo_silaba][fonemas_ipa]["+len"] += 1
                    estadisticas_silabas[tipo_silaba]["+len"] += 1
                    estadisticas_silabas["+len"] += 1

        return estadisticas_segmentos, estadisticas_silabas
