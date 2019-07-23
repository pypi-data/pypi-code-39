#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Transcriptor, que transcribe ortográfica/fonética/fonológicamente un texto

Esta clase tiene una funcionalidad restringida, y en su mayor parte se tienen métodos que hacen llamadas a
métodos de la clase Texto.
"""

from __future__ import print_function
from iar_transcriber.texto import Texto

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Transcriptor:
    u"""Esta clase contiene métodos estáticos que producen transcripciones
    """

    def __init__(self):
        u"""Constructor para la clase Transcriptor
        """
        pass

    @staticmethod
    def transcribe(texto, tipo="alo", resilabea=True,
                   incluye_separadores=True, separador=u'',
                   incluye_delimitadores=True, apertura=u'', cierre=u'',
                   marca_tonica=True, transcribe_fonemas_aparentes=False, inserta_epentesis=True,
                   ancha=False):
        u"""Devuelve la transcripción del texto de entrada, del tipo indicado y con las opciones dadas en los parámetros

        :type texto: unicode
        :param texto: El texto que se pretende transcribir.
        :type tipo: str
        :param tipo: Indica el tipo de transcripción a realizar. Puede ser: "fon" (fonológica), "alo" (fonética)
            o "ort" (ortográfica)
        :type resilabea: bool
        :param resilabea: Si está a True se resilabean las palabras de cada frase. Si no, no se hace.
        :type incluye_separadores: bool
        :param incluye_separadores: Si está a True, se incluyen separadores entre sílabas
        :type separador: unicode
        :param separador: La cadena de texto que meteremos entre sílabas
        :type incluye_delimitadores: bool
        :param incluye_delimitadores: Si está a True, se incluyen delimitadores de la transcripción al principio y al
            final de la transcripción. Estos delimitadores por defecto son u'/' para la transcripción fonológica
             y u'[', u']' en la fonética.
        :type apertura: unicode
        :param apertura: La cadena de caracteres que se mete al inicio de la transcripción
        :type cierre: unicode
        :param cierre: La cadena de caracteres que se mete al final de la transcripción
        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen (también se meten en la transcripción "ortográfica")
        :type transcribe_fonemas_aparentes: bool
        :param transcribe_fonemas_aparentes: Si está a True, en la transcripción fonológica no se transcriben los
            fonemas indicados por los grafemas, sino los indicados por la pronunciación. Así, si se están transcribiendo
            fonemas aparentes, las palabras "combino" y "convino" tienen idéntica transcripción fonológica.
        :type inserta_epentesis: bool
        :param inserta_epentesis: Si está a True se inserta una [e] epentética en sílabas con ataque complejo con /s/
            inicial, tipo "stop", "snob" o "slip"
        :type ancha: bool
        :param ancha: Si está a True, la transcripción fonética que se devuelve es la transcripción fonética ancha.
            Si está a False, se devuelve la transcripción fonética estrecha.
        :rtype: unicode
        :return: La cadena de caracteres unicode con la transcripción deseada del texto de entrada
        """
        objeto_texto = Texto(texto,
                             resilabea=resilabea and tipo != "ort",
                             calcula_alofonos=tipo == "alo",
                             inserta_epentesis=inserta_epentesis and tipo == "alo",
                             organiza_grafemas=tipo == "ort")
        if tipo == "ort":
            # Decidimos si metemos algún carácter delimitador/separador de la transcripción y cuál
            separador = u'' if not incluye_separadores else separador if separador else u'-'
            apertura = u'' if not incluye_delimitadores else apertura if apertura else u''
            cierre = u'' if not incluye_delimitadores else cierre if cierre else u''
            return objeto_texto.transcribe_ortograficamente_texto(marca_tonica, separador, apertura, cierre)
        elif tipo == "fon":
            # Decidimos si metemos algún carácter delimitador/separador de la transcripción y cuál
            separador = u'' if not incluye_separadores else separador if separador else u'.'
            apertura = u'' if not incluye_delimitadores else apertura if apertura else u'/'
            cierre = u'' if not incluye_delimitadores else cierre if cierre else u'/'
            return objeto_texto.transcribe_fonologicamente_texto(marca_tonica, transcribe_fonemas_aparentes,
                                                                 separador, apertura, cierre)
        elif tipo == "alo":
            # Decidimos si metemos algún carácter delimitador/separador de la transcripción y cuál
            separador = u'' if not incluye_separadores else separador if separador else u'.'
            apertura = u'' if not incluye_delimitadores else apertura if apertura else u'['
            cierre = u'' if not incluye_delimitadores else cierre if cierre else u']'
            return objeto_texto.transcribe_foneticamente_texto(marca_tonica, ancha, separador, apertura, cierre)


if __name__ == "__main__":
    print(Transcriptor.transcribe(u'Esta es la transcripción por defecto: con alófonos y resilabeados'))
    print(Transcriptor.transcribe(u'Esto es una transcripción fonológica sin resilabeo', tipo="fon", resilabea=False))
    print(Transcriptor.transcribe(u'También se puede hacer una transcripción ortográfica, '
                                  u'marcando los extremos de sílaba y las sílabas tónicas', tipo="ort"))
    print(Transcriptor.transcribe(u'Se puede evitar el resilabeo si es necesario', resilabea=False))
    print(Transcriptor.transcribe(u'Inserta epéntesis en palabras como stop o spor', inserta_epentesis=True))
    print(Transcriptor.transcribe(u'O las deja como están: stop o spor', inserta_epentesis=False))
    print(Transcriptor.transcribe(u'Se puede hacer una transcripción fonética ancha', ancha=True))
    print(Transcriptor.transcribe(u'Se puede hacer una transcripción fonética estrecha'))
    print(Transcriptor.transcribe(u'Además, expande números y otros caracteres: hoy, 8/2/2017, a las 13:40 '
                                  u'y con 15,4ºC en mi casa, vino Mª con un nº de lotería del siglo XIX. '
                                  u'Dice CC.OO. por SMS, que en la UGT tienen NIFs o DNIs de la URSS',
                                  tipo="ort", marca_tonica=False, incluye_separadores=False))
