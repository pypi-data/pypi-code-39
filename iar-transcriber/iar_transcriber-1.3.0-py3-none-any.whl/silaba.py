#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Silaba, que organiza los grafemas/fonemas/alófonos en sus posiciones dentro de una sílaba.

La clase Silaba representa a una sílaba y contiene internamente tres estructuras: la de grafemas, la de fonemas y la
de alófonos. En cada una de ellas se ubican los grafemas/fonemas/alófonos en posiciones concretas que indican su
posición en la sílaba: ataque, semiconsonante, vocal, semivocal y coda, además de las posibles pausas previas y
posteriores.
La sílaba también contiene información sobre su tonicidad y sobre si queda ubicada a inicio y/o fin de plabra.
Se dispone de multitud de métodos para manipular las distintas posiciones de la sílaba en cualquiera de las tres
estructuras, así como para crear transcripciones.
"""

from __future__ import print_function
from iar_transcriber.sil_consts import ATON
from iar_transcriber.fonema import FonemaConsonante, FonemaSemiconsonante, FonemaVocal, FonemaSemivocal, FonemaPausa
from iar_transcriber.fon_consts import FONEMAS, FONEMA_VACIO
from iar_transcriber.alofono import AlofonoConsonante, AlofonoSemiconsonante, AlofonoVocal, AlofonoSemivocal, AlofonoPausa
from iar_transcriber.alof_consts import ALOFONOS_NUCLEO_ORALES, ALOFONOS_NUCLEO_NASALES, ALOFONOS_ATAQUE, ALOFONOS_CODA, ALOFONO_VACIO

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


# TODO: prefijos latinos y los falsos inicios de palabra
# TODO: hiatos-diptongos invisibles ortográficamente: con-ti-núa/con-ti-nua/con-ti-nu-á (vos);
# pú-a/pu-á/pua (pie/pié, guion/guión, ion/ión).

DEBUG = False  # Si está a True, cualquier cambio en grafemas/fonemas/alófonos actualiza la transcripcion que toque
if DEBUG:
    print(u'Atención: el módulo silaba está con el DEBUG on')


class Silaba:
    u"""La clase Silaba representa una sílaba, con los grafemas/fonemas/alófonos estructurados en sus posiciones.

    Esta clase se utiliza para representar una sílaba. Se tiene una estructura interna en la que caben
    un total de 9 fonemas (en este orden): pausa (previa), consonante (ataque complejo), consonante (ataque),
    semiconsonante, vocal, semivocal, consonante (coda), consonante (coda compleja), pausa (posterior).
    Con estas 9 posiciones se puede representar cualquier sílaba del español en términos segmentales.

    Además de la representación en términos de fonemas, se realiza una estructura homóloga para los alófonos.
    Por otra parte, también se guarda la representación ortográfica (estructurada), para poder hacer cambios
    y obtener la representación ortográfica incluyendo el cambio.

    También se guarda información sobre la tonicidad de la sílaba, o sobre si está ubicada al inicio de una
    palabra, al final, o ambos. Esto último es importante para realizar el resilabeo.
    """

    def __init__(self):
        u"""Constructor para la clase Silaba.
        """
        # Inicializamos las listas de fonemas/alófonos a sus 9 elementos vacíos.
        self._fonemas = [FONEMA_VACIO] * 9  # Estructura para organizar los fonemas. Inicialmente vacío.
        self._alofonos = [ALOFONO_VACIO] * 9  # Estructura para organizar los alófonos. Inicialmente vacío.
        # La estructura de grafemas es algo distinta a la de fonemas y alófonos, principalmente porque cada
        # posición en la lista no es un elemento de tipo Grafema, sino una lista de elementos de tipo Grafema.
        # Además, tiene 7 posiciones en vez de 9 (como cada elemento es una lista, se funden todos los grafemas
        # de ataque en una única posición, y lo mismo con la coda).
        # Las listas de cada posición contendrán los grafemas asignados a dicha posición, en este orden de posiciones:
        # pausa previa, ataque, semiconsonante, vocal, semivocal, coda, pausa posterior.
        self._grafemas = [[], [], [], [], [], [], []]
        self._tonica = ATON  # Inicialmente se marca la tonicidad de la sílaba como átona
        self._inicio_palabra = False  # Se marcará a True si esta sílaba está a inicio de palabra
        self._final_palabra = False  # Se marcará a True si esta sílaba está a final de palabra
        if DEBUG:
            self.__trans_fon = u''  # Para el debugging.
            self.__trans_alo = u''  # Para el debugging.
            self.__trans_ort = u''  # Para el debugging.

    def reset_silaba(self):
        u"""Resetea la sílaba, asignando a sus atributos los valores iniciales. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.__init__()
        return self

    def get_inicio_palabra(self):
        u"""Indica si esta sílaba está a inicio de palabra.

        :rtype: bool
        :return: True si la sílaba está a inicio de palabra, False si no
        """
        return self._inicio_palabra

    def set_inicio_palabra(self, inicio_palabra):
        u"""Se activa el marcador que indica que esta sílaba está a inicio de palabra, con el valor del parámetro.

        :type inicio_palabra: bool
        :param inicio_palabra: El valor booleano que trasladaremos al marcador.
        :return: None
        """
        self._inicio_palabra = inicio_palabra

    def get_final_palabra(self):
        u"""Indica si esta sílaba está a final de palabra.

        :rtype: bool
        :return: True si la sílaba está a final de palabra, False si no
        """
        return self._final_palabra

    def set_final_palabra(self, final_palabra):
        u"""Se activa el marcador que indica que esta sílaba está a final de sílaba, con el valor del parámetro.

        :type final_palabra: bool
        :param final_palabra: El valor booleano que trasladaremos al marcador.
        :return: None
        """
        self._final_palabra = final_palabra

    def get_grafemas(self, incluye_pausas=False):
        u"""Se devuelve una list con los grafemas de la sílaba, incluyendo los signos ortográficos de pausas o no, según
        indique el parámetro. La estructura de grafemas mete en cada posición potencialmente más de un grafema, o
        incluso ninguno (no hay un "grafema vacío" como en los fonemas y alófonos), pero en este método se devuelve
        una única lista lineal de los grafemas, haciendo una unión de las listas para cada posición.

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: [Grafema]
        :return: La lista de los grafemas (incluyendo pausas o no) de la sílaba
        """
        if incluye_pausas:
            return [grafema for posicion in self._grafemas for grafema in posicion]
        else:
            return [grafema for posicion in self._grafemas[1:-1] for grafema in posicion]

    def get_fonemas(self, incluye_pausas=False):
        u"""Se devuelve una list con los fonemas de la sílaba, incluyendo los fonemas de pausas o no, según el parámetro

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir los fonemas de pausas, False si no
        :rtype: [Fonema]
        :return: La lista los fonemas (incluyendo pausas o no) de la sílaba
        """
        if incluye_pausas:
            return [fonema for fonema in self._fonemas if fonema.get_fonema_ipa()]
        else:
            return [fonema for fonema in self._fonemas[1:8] if fonema.get_fonema_ipa()]

    def get_alofonos(self, incluye_pausas=False):
        u"""Se devuelve una lista con los alófonos de la sílaba, incluyendo los alófonos de pausas o no, según parámetro

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir los alófonos de pausas, False si no
        :rtype: [Alofono]
        :return: La lista de los alófonos (incluyendo pausas o no) de la sílaba
        """
        if incluye_pausas:
            return [alofono for alofono in self._alofonos if alofono.get_alofono_ipa()]
        else:
            return [alofono for alofono in self._alofonos[1:8] if alofono.get_alofono_ipa()]

    def transcribe_ortograficamente_silaba(self, marca_tonica, incluye_pausas):
        u"""Se devuelve la transcripción ortográfica de la sílaba, incluyendo las pausas o no, según el parámetro

        :type marca_tonica: bool
        :param marca_tonica: Si está a True, se incluyen los símbolos fonéticos de tonicidad. Si está a False, se omiten
        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: unicode
        :return: La transcripción ortográfica de la sílaba
        """
        return (self._tonica if marca_tonica else ATON) +\
            u''.join([grafema.get_grafema_txt() for grafema in self.get_grafemas(incluye_pausas)])

    def transcribe_fonologicamente_silaba(self, marca_tonica, incluye_pausa_previa, incluye_pausa_posterior,
                                          transcribe_fonemas_aparentes):
        u"""Se devuelve la transcripción fonológica de la sílaba, según los parámetros

        En la transcripción fonológica se incluyen o no las marcas de tonicidad y de las pausas según los parámetros.
        Además, cabe la posibilidad de transcribir los "fonemas aparentes", que habitualmente se corresponde con
        el fonema inicial determinado por el grafema, pero que puede ser otro si hay alguna modificación fonética
        que genere un alófono que se corresponda habitualmente con un fonema distinto.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True, se incluyen los símbolos fonéticos de tonicidad. Si está a False, se omiten
        :type incluye_pausa_previa: bool
        :param incluye_pausa_previa: True si se deben incluir las pausas previas, False si no
        :type incluye_pausa_posterior: bool
        :param incluye_pausa_posterior: True si se deben incluir las pausas posteriores, False si no
        :type transcribe_fonemas_aparentes: bool
        :param transcribe_fonemas_aparentes: Si está a True, se transcriben los fonemas aparentes. Así, la transcripción
        de <convino> y <combino> se diferencia en la primera nasal (en coda), pero usando los fonemas aparentes, la
        transcripción de de <convino> se transforma y se hace igual a la de <combino>: /kombino/
        :rtype: unicode
        :return: La transcripción fonológica de la sílaba, según los parámetros
        """
        transcripcion = self._tonica if marca_tonica else ATON
        if transcribe_fonemas_aparentes:
            transcripcion += u''.join([alofono.get_fonema_aparente_ipa() for alofono in self._alofonos[1:8]])
        else:
            transcripcion += u''.join([fonema.get_fonema_ipa() for fonema in self._fonemas[1:8]])

        pausa_previa_ipa = self._fonemas[0].get_fonema_ipa() if incluye_pausa_previa else u''
        pausa_posterior_ipa = self._fonemas[8].get_fonema_ipa() if incluye_pausa_posterior else u''
        if transcripcion:
            return pausa_previa_ipa + transcripcion + pausa_posterior_ipa
        else:
            if pausa_previa_ipa == u'‖' or pausa_posterior_ipa == u'‖':
                return u'‖'
            elif pausa_previa_ipa or pausa_posterior_ipa:
                return u'|'
        return transcripcion

    def transcribe_foneticamente_silaba(self, marca_tonica, incluye_pausa_previa, incluye_pausa_posterior, ancha=False):
        u"""Se devuelve la transcripción fonética de la sílaba, según los parámetros

        Se devuelve un str con la transcripción fonética de la sílaba, incluyendo o no la transcripción de las marcas
        de tonicidad y de las pausas según los parámetros. Además, cabe la posibilidad de hacer una transcripción
        fonética estrecha (por defecto) o ancha, según el parámetro.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True, se incluyen los símbolos fonéticos de tonicidad. Si está a False, se omiten
        :type incluye_pausa_previa: bool
        :param incluye_pausa_previa: True si se debe incluir la pausa previa, False si no.
        :type incluye_pausa_posterior: bool
        :param incluye_pausa_posterior: True si se debe incluir la pausa posterior, False si no.
        :type ancha: bool
        :param ancha: True si se quiere una transcripción ancha, False si se prefiere estrecha.
        :rtype: unicode
        :return: La transcripción fonética de la sílaba, según los parámetros
        """
        transcripcion = self._tonica if marca_tonica else ATON
        transcripcion += u''.join([alofono.get_alofono_ipa() for alofono in self._alofonos[1:8]])
        pausa_previa_ipa = self._alofonos[0].get_alofono_ipa() if incluye_pausa_previa else u''
        pausa_posterior_ipa = self._alofonos[8].get_alofono_ipa() if incluye_pausa_posterior else u''
        if transcripcion:
            return pausa_previa_ipa + transcripcion + pausa_posterior_ipa
        else:
            if pausa_previa_ipa == u'‖' or pausa_posterior_ipa == u'‖':
                return u'‖'
            elif pausa_previa_ipa or pausa_posterior_ipa:
                return u'|'
        if ancha:
            # Hacemos una simplificación de algunos símbolos.
            transcripcion = transcripcion.replace(u'i̞', u'i')
            transcripcion = transcripcion.replace(u'ɛ', u'e')
            transcripcion = transcripcion.replace(u'ɑ', u'a')
            transcripcion = transcripcion.replace(u'ɔ', u'o')
            transcripcion = transcripcion.replace(u'u̞', u'u')
            transcripcion = transcripcion.replace(u'β̞', u'β')
            transcripcion = transcripcion.replace(u'd̪', u'd')
            transcripcion = transcripcion.replace(u'ð̞', u'ð')
            transcripcion = transcripcion.replace(u't̟', u't')
            transcripcion = transcripcion.replace(u't̪', u't')
            transcripcion = transcripcion.replace(u'ɣ̞', u'ɣ')
            transcripcion = transcripcion.replace(u'k̠', u'k')
            transcripcion = transcripcion.replace(u'k̟', u'k')
            transcripcion = transcripcion.replace(u'n̠', u'ɲ')
            transcripcion = transcripcion.replace(u'ɴ', u'ŋ')
            transcripcion = transcripcion.replace(u'f̬', u'f')
            transcripcion = transcripcion.replace(u'θ̬', u'θ')
            transcripcion = transcripcion.replace(u's̬', u's')
            transcripcion = transcripcion.replace(u'z̪', u's')
            transcripcion = transcripcion.replace(u's̪', u's')
            transcripcion = transcripcion.replace(u'χ', u'x')
            transcripcion = transcripcion.replace(u'ʝ̞', u'ʝ')
            transcripcion = transcripcion.replace(u'l̠', u'ʎ')
        return transcripcion

    def get_grafemas_pausa_previa(self):
        u"""Se devuelve una lista con los grafemas ubicados en la posición de pausa previa

        :rtype: [Grafema]
        :return: una [Grafema] con los grafemas correspondientes a la pausa previa (o [] si no hay)
        """
        return self._grafemas[0]

    def get_fonema_pausa_previa(self):
        u"""Se devuelve el fonema de la pausa previa

        :rtype: FonemaPausa
        :return: El Fonema correspondientes a la pausa previa, o None si no hay
        """
        return self._fonemas[0] if self._fonemas[0].get_fonema_ipa() else None

    def get_alofono_pausa_previa(self):
        u"""Se devuelve el alófono de la pausa previa

        :rtype: AlofonoPausa
        :return: El Alofono correspondientes a la pausa previa, o None si no hay
        """
        return self._alofonos[0] if self._alofonos[0].get_alofono_ipa() else None

    def append_grafema_pausa_previa(self, grafema_pausa):
        u"""Se añade por detrás un grafema de pausa previa

        :rtype grafema_pausa: Grafema
        :param grafema_pausa: El grafema que se va añadir
        :return: None
        """
        self._grafemas[0].append(grafema_pausa)
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafema_pausa_previa(self, grafema_pausa):
        u"""Se añade por delante un grafema de pausa previa

        :type grafema_pausa: Grafema
        :param grafema_pausa: El grafema que se va añadir
        :return: None
        """
        self._grafemas[0] = [grafema_pausa] + self._grafemas[0]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def set_fonema_pausa_previa(self, fonema_pausa):
        u"""Se fija el fonema de pausa previa

        :rtype fonema_pausa: FonemaPausa
        :param fonema_pausa: El fonema de pausa
        :return: None
        """
        self._fonemas[0] = fonema_pausa
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def set_alofono_pausa_previa(self, alofono_pausa):
        u"""Se fija el alofono de pausa previa

        :rtype alofono_pausa: AlofonoPausa
        :param alofono_pausa: El alófono de pausa
        :return: None
        """
        self._alofonos[0] = alofono_pausa
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def reset_grafemas_pausa_previa(self):
        u"""Se eliminan los grafemas de pausa previa. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._grafemas = [[]] + self._grafemas[1:]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
        return self

    def reset_fonema_pausa_previa(self):
        u"""Se elimina el fonema de pausa previa. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._fonemas = [FONEMA_VACIO] + self._fonemas[1:]
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
        return self

    def reset_alofono_pausa_previa(self):
        u"""Se elimina el alófono de pausa previa. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._alofonos = [ALOFONO_VACIO] + self._alofonos[1:]
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def reset_pausa_previa(self):
        u"""Se eliminan los grafemas/fonema/alófono de pausa previa. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.reset_grafemas_pausa_previa()
        self.reset_fonema_pausa_previa()
        self.reset_alofono_pausa_previa()
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def get_grafemas_ataque(self, incluye_pausas=False):
        u"""Devuelve la lista de grafemas ubicados en posición de ataque (incluyendo o no la pausa previa)

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluye en el resultado los grafemas de pausa previa
        :rtype: [Grafema]
        :return: La lista de grafemas en posicion de ataque en esta sílaba
        """
        if incluye_pausas:
            return [grafema for posicion in self._grafemas[0 if incluye_pausas else 1:2] for grafema in posicion]
        else:
            return self._grafemas[1]

    def get_fonemas_ataque(self, incluye_pausas=False):
        u"""Devuelve la lista de fonemas ubicados en posición de ataque

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluye en el resultado el fonema de pausa previa
        :rtype: [FonemaConsonante]
        :return: La lista con los fonemas en posicion de ataque en esta sílaba
        """
        return [fonema for fonema in self._fonemas[0 if incluye_pausas else 1:3] if fonema.get_fonema_ipa()]

    def get_alofonos_ataque(self, incluye_pausas=False):
        u"""Devuelve la lista de alófonos ubicados en posición de ataque

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluye en el resultado el alófono de pausa previa
        :rtype: [AlofonoConsonante]
        :return: La lista con los alófonos en posicion de ataque en esta sílaba
        """
        return [alofono for alofono in self._alofonos[0 if incluye_pausas else 1:3] if alofono.get_fonema_padre_ipa()]

    def append_grafema_ataque(self, grafema_ataque):
        u"""Se añade por detrás un grafema de ataque

        :type grafema_ataque: Grafema
        :param grafema_ataque: El grafema que se va añadir
        :return: None
        """
        self._grafemas[1].append(grafema_ataque)
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def append_grafemas_ataque(self, grafemas_ataque):
        u"""Se añade por detrás un grafema de ataque

        :type grafemas_ataque: [Grafema]
        :param grafemas_ataque: La lista de grafemas que se va añadir
        :return: None
        """
        self._grafemas[1] += grafemas_ataque
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafema_ataque(self, grafema_ataque):
        u"""Se añade por delante un grafema de ataque

        :type grafema_ataque: Grafema
        :param grafema_ataque: El grafema que se va añadir
        :return: None
        """
        self._grafemas[1] = [grafema_ataque] + self._grafemas[1]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafemas_ataque(self, grafemas_ataque):
        u"""Se añade por delante un grafema de ataque

        :type grafemas_ataque: [Grafema]
        :param grafemas_ataque: La lista de grafemas que se va añadir
        :return: None
        """
        grafemas_ataque += self._grafemas[1]
        self._grafemas[1] = grafemas_ataque
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def append_fonema_ataque(self, fonema_ataque):
        u"""Se añade por detrás un fonema de ataque

        :type fonema_ataque: FonemaConsonante
        :param fonema_ataque: El fonema que se va añadir
        :return: None
        """
        self._fonemas[1] = self._fonemas[2]
        self._fonemas[2] = fonema_ataque
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def prepend_fonema_ataque(self, fonema_ataque):
        u"""Se añade por delante un fonema de ataque.

        Se diferencia bastante con el append, puesto que cuando usamos el append es porque es una consonante pegada
        a un vocoide. Con el prepend, en principio puede haber una consonante posterior y entonces existe la
        posibilidad de tener un ataque geminado, por ejemplo.

        :type fonema_ataque: FonemaConsonante
        :param fonema_ataque: El fonema que se va añadir
        :return: None
        """
        if not self._fonemas[2].get_fonema_ipa():
            # Si no había ninguna consonante en ataque, metemos esta.
            self._fonemas[2] = fonema_ataque
        elif not self._fonemas[1].get_fonema_ipa():
            # Sí había una primera consonante de ataque y esta es la segunda
            if self._fonemas[2].get_fonema_ipa()[0] == fonema_ataque.get_fonema_ipa()[0]:
                # Dos consonantes iguales. Alargamos el ataque.
                self._fonemas[2] = FONEMAS[self._fonemas[2].get_fonema_ipa().replace(u'ː', u'') + u'ː']
            else:
                self._fonemas[1] = fonema_ataque
        elif self._fonemas[1].get_fonema_ipa()[0] == fonema_ataque.get_fonema_ipa()[0]:
            # Había una 2ª consonante de ataque, igual a la que nos entra. Alargamos la 2ª consonante de ataque
            self._fonemas[1] = FONEMAS[self._fonemas[1].get_fonema_ipa().replace(u'ː', u'') + u'ː']
        else:
            # Había una 2ª consonante de ataque, distinta a esta. La machacamos y metemos la nueva (en cualquier caso
            # el ataque no sigue la fonotáctica del español, al haber tres consonantes en ataque).
            self._fonemas[1] = fonema_ataque
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def append_alofono_ataque(self, alofono_ataque):
        u"""Se añade por detrás un alófono de ataque.

        :type alofono_ataque: AlofonoConsonante
        :param alofono_ataque: El alófono que se va añadir
        :return: None
        """
        self._alofonos[1] = self._alofonos[2]
        self._alofonos[2] = alofono_ataque
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def prepend_alofono_ataque(self, alofono_ataque):
        u"""Se añade por delante un alófono de ataque.

        :type alofono_ataque: AlofonoConsonante
        :param alofono_ataque: El alófono que se va añadir
        :return: None
        """
        if not self._alofonos[2].get_fonema_padre_ipa():
            self._alofonos[2] = alofono_ataque
        else:
            # Si ya hubiera una 2ª consonante de ataque, la machacamos. Es un caso ilegal en español en cualquier caso.
            self._alofonos[1] = alofono_ataque
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def set_grafemas_ataque(self, grafemas_ataque):
        u"""Se fijan los grafemas de ataque

        :type grafemas_ataque: [Grafema]
        :param grafemas_ataque: La lista de grafemas que deben meterse como ataque
        :return: None
        """
        self._grafemas[1] = grafemas_ataque
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def set_fonemas_ataque(self, fonemas_ataque):
        u"""Se fijan los fonemas de ataque

        :type fonemas_ataque: [FonemaConsonante]
        :param fonemas_ataque: La lista de fonemas que deben meterse como ataque
        :return: None
        """
        self._fonemas = self._fonemas[:1] + ([FONEMA_VACIO] * (2 - len(fonemas_ataque))) +\
            fonemas_ataque + self._fonemas[3:]
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def set_alofonos_ataque(self, alofonos_ataque):
        u"""Se fijan los alófonos de ataque. Entre 0 y 2 alófonos.

        :type alofonos_ataque: [AlofonoConsonante]
        :param alofonos_ataque: La lista de alófonos que deben meterse como ataque
        :return: None
        """
        alofonos_ataque = alofonos_ataque[:2]  # Si hay más de dos, sólo vamos a usar los dos primeros
        self._alofonos = self._alofonos[:1] + ([ALOFONO_VACIO] * (2 - len(alofonos_ataque))) +\
            alofonos_ataque + self._alofonos[3:]
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def reset_grafemas_ataque(self):
        u"""Se eliminan los grafemas de ataque. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._grafemas = self._grafemas[:1] + [[]] + self._grafemas[2:]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
        return self

    def reset_fonemas_ataque(self):
        u"""Se eliminan los fonemas de ataque. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._fonemas = self._fonemas[:1] + ([FONEMA_VACIO] * 2) + self._fonemas[3:]
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
        return self

    def reset_alofonos_ataque(self):
        u"""Se eliminan los alófonos de ataque. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._alofonos = self._alofonos[:1] + ([ALOFONO_VACIO] * 2) + self._alofonos[3:]
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def reset_ataque(self):
        u"""Se eliminan los grafemas/fonemas/alófonos de ataque. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.reset_grafemas_ataque()
        self.reset_fonemas_ataque()
        self.reset_alofonos_ataque()
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def alarga_fonema_ataque(self):
        u"""Se toma el primer fonema de ataque y se reemplaza por su versión larga.

        :return: None
        """
        if not self._fonemas[1].get_fonema_ipa():
            if self._fonemas[2].get_fonema_ipa():
                self._fonemas[2] = FONEMAS[self._fonemas[2].get_fonema_ipa().replace(u'ː', u'') + u'ː']
        else:
            self._fonemas[1] = FONEMAS[self._fonemas[1].get_fonema_ipa().replace(u'ː', u'') + u'ː']
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def get_grafemas_cabeza(self):
        u"""Devuelve la lista de grafemas de ataque y núcleo

        :rtype: [Grafema]
        :return: La lista con los grafemas en posicion de ataque y núcleo en esta sílaba
        """
        return [grafema for posicion in self._grafemas[1:5] for grafema in posicion]

    def get_fonemas_cabeza(self):
        u"""Devuelve la lista de fonemas de ataque y núcleo

        :rtype: [Fonema]
        :return: La lista con los fonemas en posicion de ataque y núcleo en esta sílaba
        """
        return [fonema for fonema in self._fonemas[1:6] if fonema.get_fonema_ipa()]

    def get_alofonos_cabeza(self):
        u"""Devuelve la lista de alófonos de ataque y núcleo

        :rtype: [Alofono]
        :return: La lista con los alófonos en posicion de ataque y núcleo en esta sílaba
        """
        return [alofono for alofono in self._alofonos[1:6] if alofono.get_fonema_padre_ipa()]

    def get_grafemas_nucleo(self):
        u"""Devuelve la lista de grafemas de núcleo

        :rtype: [Grafema]
        :return: La lista con los grafemas en posicion de núcleo en esta sílaba
        """
        return [grafema for posicion in self._grafemas[2:5] for grafema in posicion]

    def get_fonemas_nucleo(self):
        u"""Devuelve la lista de fonemas de núcleo

        :rtype: [FonemaVocoide]
        :return: La lista con los fonemas en posicion de núcleo en esta sílaba
        """
        return [fonema for fonema in self._fonemas[3:6] if fonema.get_fonema_ipa()]

    def get_alofonos_nucleo(self):
        u"""Devuelve la lista de alófonos de núcleo

        :rtype: [AlofonoVocoide]
        :return: La lista con los alófonos en posicion de núcleo en esta sílaba
        """
        return [alofono for alofono in self._alofonos[3:6] if alofono.get_fonema_padre_ipa()]

    def get_grafemas_semiconsonante(self):
        u"""Devuelve la lista de grafemas de semiconsonante

        :rtype: [Grafema]
        :return: La lista con los grafemas en posicion de semiconsonante en esta sílaba
        """
        return self._grafemas[2]

    def get_fonema_semiconsonante(self):
        u"""Devuelve el fonema semiconsonante si hay, o None si no

        :rtype: FonemaSemiconsonante
        :return: El Fonema de semiconsonante, o None si no tiene
        """
        return self._fonemas[3] if self._fonemas[3].get_fonema_ipa() else None

    def get_alofono_semiconsonante(self):
        u"""Devuelve el alófono semiconsonante si hay, o None si no

        :rtype: AlofonoSemiconsonante
        :return: El Alofono de semiconsonante, o None si no tiene
        """
        return self._alofonos[3] if self._alofonos[3].get_fonema_padre_ipa() else None

    def append_grafema_semiconsonante(self, grafema_semiconsonante):
        u"""Se añade por detrás un grafema de semiconsonante

        :type grafema_semiconsonante: Grafema
        :param grafema_semiconsonante: El grafema que se va añadir
        :return: None
        """
        self._grafemas[2].append(grafema_semiconsonante)
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafema_semiconsonante(self, grafema_semiconsonante):
        u"""Se añade por delante un grafema de semiconsonante

        :type grafema_semiconsonante: Grafema
        :param grafema_semiconsonante: El grafema que se va añadir
        :return: None
        """
        self._grafemas[2] = [grafema_semiconsonante] + self._grafemas[2]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def set_fonema_semiconsonante(self, fonema_semiconsonante):
        u"""Se fija el fonema de semiconsonante

        :type fonema_semiconsonante: FonemaSemiconsonante
        :param fonema_semiconsonante: El fonema de semiconsonante
        :return: None
        """
        self._fonemas[3] = fonema_semiconsonante
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def set_alofono_semiconsonante(self, alofono_semiconsonante):
        u"""Se fija el alofono de semiconsonante

        :type alofono_semiconsonante: AlofonoSemiconsonante
        :param alofono_semiconsonante: El alófono de semiconsonante
        :return: None
        """
        self._alofonos[3] = alofono_semiconsonante
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def reset_grafemas_semiconsonante(self):
        u"""Se eliminan los grafemas de semiconsonante. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._grafemas[2] = []
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
        return self

    def reset_fonema_semiconsonante(self):
        u"""Se elimina el fonema de semiconsonante. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._fonemas[3] = FONEMA_VACIO
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
        return self

    def reset_alofono_semiconsonante(self):
        u"""Se elimina el alófono de semiconsonante. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._alofonos[3] = ALOFONO_VACIO
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def reset_semiconsonante(self):
        u"""Se elimina el grafema/fonema/alófono de semiconsonante. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.reset_grafemas_semiconsonante()
        self.reset_fonema_semiconsonante()
        self.reset_alofono_semiconsonante()
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def vocaliza_semiconsonante(self):
        u"""Se reemplaza la vocal por la vocalización de la semiconsonante y se elimina la semiconsonante.

        Para vocalizar una semiconsonante simplemente tomamos la vocal cerrada con el punto de articulación
        y nasalización correspondiente.

        Se modifican tanto fonemas como alófonos y grafemas.

        :return: None
        """
        semiconsonante = self.get_alofono_semiconsonante()
        if not semiconsonante:
            return  # Nada que hacer
        # El cambio en grafemas es trivial: simplemente se mueven los grafemas de la posición de semiconsonante, y
        # se machaca el valor que tuviera la vocal. Luego resetearemos la semiconsonante y la borraremos
        self.set_grafemas_vocal(self.get_grafemas_semiconsonante())
        ataque = self.get_alofonos_ataque()
        vocal = self.get_alofono_vocal()
        vocal_ipa = vocal.get_alofono_ipa().replace(u'ː', u'')  # Para poder comparar mejor quitamos el diacrítico
        semiconsonante_ipa = semiconsonante.get_alofono_ipa()
        if semiconsonante_ipa == u'j':
            self.set_grafemas_vocal(self.get_grafemas_semiconsonante())
            self.set_fonema_vocal(FONEMAS[u'i'])
            # Para un mejor empalme, escogemos la versión abierta o cerrada coincidente con la apertura de la vocal
            # fuerte del diptongo, o se usa la versión abierta cuando la consonante previa es una /r/ (corta o larga).
            if vocal_ipa in [u'ɛ', u'ɑ', u'ɔ', u'u̞'] or\
                    (ataque and ataque[0].get_alofono_ipa().replace(u'ː', u'') == u'r'):
                self.set_alofono_vocal(ALOFONOS_NUCLEO_ORALES[u'i'][0])  # La primera opción es el alófono abierto
            else:
                self.set_alofono_vocal(ALOFONOS_NUCLEO_ORALES[u'i'][-1])  # La última opción es el alófono cerrado
        elif semiconsonante_ipa == u'j̃':
            self.set_fonema_vocal(FONEMAS[u'i'])
            # Para un mejor empalme, escogemos la versión abierta o cerrada coincidente con la apertura de la vocal
            # fuerte del diptongo.
            if vocal_ipa in [u'ɔ̃', u'ũ̞']:  # /e/ y /a/ no se abren con nasal en coda.
                self.set_alofono_vocal(ALOFONOS_NUCLEO_NASALES[u'i'][-1])  # La abierta es la última
            else:
                self.set_alofono_vocal(ALOFONOS_NUCLEO_NASALES[u'i'][0])  # La cerrada es la primera
        elif semiconsonante_ipa == u'w':
            self.set_fonema_vocal(FONEMAS[u'u'])
            # Para un mejor empalme, escogemos la versión abierta o cerrada coincidente con la apertura de la vocal
            # fuerte del diptongo, o se usa la versión abierta cuando la consonante previa es una /r/ (corta o larga).
            if vocal_ipa in [u'i̞', u'ɛ', u'ɑ', u'ɔ'] or\
                    (ataque and ataque[0].get_alofono_ipa().replace(u'ː', u'') == u'r'):
                self.set_alofono_vocal(ALOFONOS_NUCLEO_ORALES[u'u'][0])  # La primera opción es el alófono abierto
            else:
                self.set_alofono_vocal(ALOFONOS_NUCLEO_ORALES[u'u'][-1])  # La última opción es el alófono cerrado
        elif semiconsonante_ipa == u'w̃':
            self.set_fonema_vocal(FONEMAS[u'u'])
            # Para un mejor empalme, escogemos la versión abierta o cerrada coincidente con la apertura de la vocal
            # fuerte del diptongo.
            if vocal_ipa in [u'ĩ̞', u'ɔ̃']:  # /e/ y /a/ no se abren con nasal en coda.
                self.set_alofono_vocal(ALOFONOS_NUCLEO_NASALES[u'u'][-1])  # La abierta es la última
            else:
                self.set_alofono_vocal(ALOFONOS_NUCLEO_NASALES[u'u'][0])  # La cerrada es la primera
        self.reset_semiconsonante()

    def get_grafemas_vocal(self):
        u"""Devuelve la lista de grafemas de vocal

        :rtype: [Grafema]
        :return: la lista con los grafemas en posicion de vocal en esta sílaba
        """
        return self._grafemas[3]

    def get_fonema_vocal(self):
        u"""Devuelve el fonema vocal si hay, o None si no

        :rtype: FonemaVocal
        :return: El Fonema de vocal, o None si no tiene
        """
        return self._fonemas[4] if self._fonemas[4].get_fonema_ipa() else None

    def get_alofono_vocal(self):
        u"""Devuelve el alófono vocal si hay, o None si no

        :rtype: AlofonoVocal
        :return: El Alofono de vocal, o None si no tiene
        """
        return self._alofonos[4] if self._alofonos[4].get_fonema_padre_ipa() else None

    def append_grafema_vocal(self, grafema_vocal):
        u"""Se añade por detrás un grafema de vocal

        :type grafema_vocal: Grafema
        :param grafema_vocal: El grafema que se va añadir
        :return: None
        """
        self._grafemas[3].append(grafema_vocal)
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafema_vocal(self, grafema_vocal):
        u"""Se añade por delante un grafema de pausa previa

        :type grafema_vocal: Grafema
        :param grafema_vocal: El grafema que se va añadir
        :return: None
        """
        self._grafemas[3] = [grafema_vocal] + self._grafemas[3]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def set_grafemas_vocal(self, grafemas_vocal):
        u"""Se fijan los grafemas de ataque

        :type grafemas_vocal: [Grafema]
        :param grafemas_vocal: La lista de grafemas que deben meterse como vocal
        :return: None
        """
        self._grafemas[3] = grafemas_vocal
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def set_fonema_vocal(self, fonema_vocal):
        u"""Se fija el fonema de vocal

        :type fonema_vocal: FonemaVocal
        :param fonema_vocal: El fonema de vocal
        :return: None
        """
        self._fonemas[4] = fonema_vocal
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def set_alofono_vocal(self, alofono_vocal):
        u"""Se fija el alofono de vocal

        :type alofono_vocal: AlofonoVocal
        :param alofono_vocal: El alófono de vocal
        :return: None
        """
        self._alofonos[4] = alofono_vocal
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def reset_grafemas_vocal(self):
        u"""Se eliminan los grafemas de vocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._grafemas[3] = []
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
        return self

    def reset_fonema_vocal(self):
        u"""Se elimina el fonema de vocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._fonemas[4] = FONEMA_VACIO
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
        return self

    def reset_alofono_vocal(self):
        u"""Se elimina el alófono de vocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._alofonos[4] = ALOFONO_VACIO
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def reset_vocal(self):
        u"""Se eliminan los grafemas/fonema/alófono de vocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.reset_grafemas_vocal()
        self.reset_fonema_vocal()
        self.reset_alofono_vocal()
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def get_grafemas_semivocal(self):
        u"""Devuelve la lista de grafemas de semivocal

        :rtype: [Grafema]
        :return: la [Grafema] con los grafemas en posicion de semivocal en esta sílaba
        """
        return self._grafemas[4]

    def get_fonema_semivocal(self):
        u"""Devuelve el fonema semivocal si hay, o None si no

        :rtype: FonemaSemivocal
        :return: El Fonema de semivocal, o None si no tiene
        """
        return self._fonemas[5] if self._fonemas[5].get_fonema_ipa() else None

    def get_alofono_semivocal(self):
        u"""Devuelve el alófono semivocal si hay, o None si no

        :rtype: AlofonoSemivocal
        :return: El Alofono de semivocal, o None si no tiene
        """
        return self._alofonos[5] if self._alofonos[5].get_fonema_padre_ipa() else None

    def append_grafema_semivocal(self, grafema_semivocal):
        u"""Se añade por detrás un grafema de semivocal

        :type grafema_semivocal: Grafema
        :param grafema_semivocal: El grafema que se va añadir
        :return: None
        """
        self._grafemas[4].append(grafema_semivocal)
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafema_semivocal(self, grafema_semivocal):
        u"""Se añade por delante un grafema de vocal

        :type grafema_semivocal: Grafema
        :param grafema_semivocal: El grafema que se va añadir
        :return: None
        """
        self._grafemas[4] = [grafema_semivocal] + self._grafemas[4]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def set_fonema_semivocal(self, fonema_semivocal):
        u"""Se fija el fonema de vocal

        :type fonema_semivocal: FonemaSemivocal
        :param fonema_semivocal: El fonema de semivocal
        :return: None
        """
        self._fonemas[5] = fonema_semivocal
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def set_alofono_semivocal(self, alofono_semivocal):
        u"""Se fija el alofono de semivocal

        :type alofono_semivocal: AlofonoSemivocal
        :param alofono_semivocal: El alófono de semivocal
        :return: None
        """
        self._alofonos[5] = alofono_semivocal
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def reset_grafemas_semivocal(self):
        u"""Se eliminan los grafemas de semivocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._grafemas[4] = []
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
        return self

    def reset_fonema_semivocal(self):
        u"""Se elimina el fonema de semivocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._fonemas[5] = FONEMA_VACIO
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
        return self

    def reset_alofono_semivocal(self):
        u"""Se elimina el alófono de semivocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._alofonos[5] = ALOFONO_VACIO
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def reset_semivocal(self):
        u"""Se eliminan los grafemas/fonema/alófono de semivocal. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.reset_grafemas_semivocal()
        self.reset_fonema_semivocal()
        self.reset_alofono_semivocal()
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def vocaliza_semivocal(self):
        u"""Se reemplaza la vocal por la vocalización de la semivocal y se elimina la semivocal.

        Para vocalizar una semivocal simplemente tomamos la vocal cerrada con el punto de articulación y nasalización
        correspondiente. Se modifican tanto fonemas como alófonos y grafemas.

        :return: None
        """
        semivocal = self.get_alofono_semivocal()
        if not semivocal:
            return  # Nada que hacer
        # El cambio en grafemas es trivial: simplemente se mueven los grafemas de la posición de semivocal, y
        # se machaca el valor que tuviera la vocal. Luego resetearemos la semivocal y la borraremos
        self.set_grafemas_vocal(self.get_grafemas_semiconsonante())
        semivocal_ipa = semivocal.get_alofono_ipa()
        # La sílaba es cerrada (si no, no se llamaría a esta función), así que la vocal que escogemos es siempre
        # la cerrada.
        if semivocal_ipa in [u'i̯']:
            self.set_fonema_vocal(FONEMAS[u'i'])
            self.set_alofono_vocal(ALOFONOS_NUCLEO_ORALES[u'i'][0])  # La cerrada es la primera
        elif semivocal_ipa in [u'ĩ̯']:
            self.set_fonema_vocal(FONEMAS[u'i'])
            self.set_alofono_vocal(ALOFONOS_NUCLEO_NASALES[u'i'][-1])  # La última opción es el alófono cerrado
        elif semivocal_ipa in [u'u̯']:
            self.set_fonema_vocal(FONEMAS[u'u'])
            self.set_alofono_vocal(ALOFONOS_NUCLEO_ORALES[u'u'][0])  # La cerrada es la primera
        elif semivocal_ipa in [u'ũ̯']:
            self.set_fonema_vocal(FONEMAS[u'u'])
            self.set_alofono_vocal(ALOFONOS_NUCLEO_NASALES[u'u'][-1])  # La última opción es el alófono cerrado
        self.reset_semivocal()

    def get_grafemas_coda(self, incluye_pausas=False):
        u"""Devuelve la lista de grafemas de coda (incluyendo o no los de pausa posterior)

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: [Grafema]
        :return: La lista con los grafemas en posicion de coda en esta sílaba (más los de pausa, según el parámetro)
        """
        if incluye_pausas:
            return [grafema for posicion in self._grafemas[5:7 if incluye_pausas else 6] for grafema in posicion]
        else:
            return self._grafemas[5]

    def get_fonemas_coda(self, incluye_pausas=False):
        u"""Devuelve la lista de fonemas de coda (incluyendo o no los de pausa posterior)

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: [FonemaConsonante]
        :return: La lista con los fonemas en posicion de coda en esta sílaba
        """
        return [fonema for fonema in self._fonemas[6:9 if incluye_pausas else 8] if fonema.get_fonema_ipa()]

    def get_alofonos_coda(self, incluye_pausas=False):
        u"""Devuelve la lista de alófonos de coda (incluyendo o no los de pausa posterior)

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: [AlofonoConsonante]
        :return: La lista con los fonemas en posicion de coda en esta sílaba
        """
        return [alofono for alofono in self._alofonos[6:9 if incluye_pausas else 8] if alofono.get_fonema_padre_ipa()]

    def append_grafemas_coda(self, grafemas_coda):
        u"""Se añade por detrás un grafema de coda

        :type grafemas_coda: [Grafema]
        :param grafemas_coda: La lista con los grafemas que se van a añadir
        :return: None
        """
        self._grafemas[5] += grafemas_coda
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def append_grafema_coda(self, grafema_coda):
        u"""Se añade por detrás un grafema de coda

        :type grafema_coda: Grafema
        :param grafema_coda: El grafema que se va añadir
        :return: None
        """
        self._grafemas[5].append(grafema_coda)
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def append_fonema_coda(self, fonema_coda):
        u"""Se añade por detrás un fonema de coda

        :type fonema_coda: FonemaConsonante
        :param fonema_coda: El fonema que se va añadir
        :return: None
        """
        if not self._fonemas[6].get_fonema_ipa():
            self._fonemas[6] = fonema_coda
        elif not self._fonemas[7].get_fonema_ipa():
            self._fonemas[7] = fonema_coda
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def append_alofono_coda(self, alofono_coda):
        u"""Se añade por detrás un alófono de coda

        :type alofono_coda: AlofonoConsonante
        :param alofono_coda: El alófono que se va añadir
        :return: None
        """
        if not self._alofonos[6].get_fonema_padre_ipa():
            self._alofonos[6] = alofono_coda
        elif not self._alofonos[7].get_fonema_padre_ipa():
            self._alofonos[7] = alofono_coda
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def prepend_grafemas_coda(self, grafemas_coda):
        u"""Se añade por delante una lista de grafemas de vocal

        :type grafemas_coda: [Grafema]
        :param grafemas_coda: La lista con los grafemas que se van a añadir
        :return: None
        """
        grafemas_coda += self._grafemas[5]
        self._grafemas[5] = grafemas_coda
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafema_coda(self, grafema_coda):
        u"""Se añade por delante un grafema de coda

        :type grafema_coda: Grafema
        :param grafema_coda: El grafema que se va añadir
        :return: None
        """
        self._grafemas[5] = [grafema_coda] + self._grafemas[5]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_fonema_coda(self, fonema_coda):
        u"""Se añade por delante un fonema de coda

        :type fonema_coda: FonemaConsonante
        :param fonema_coda: El fonema que se va añadir
        :return: None
        """
        if self._fonemas[6].get_fonema_ipa() and\
                self._fonemas[6].get_fonema_ipa()[0] == fonema_coda.get_fonema_ipa()[0]:
            # Dos consonantes iguales. Alargamos la coda.
            self._fonemas[6] = FONEMAS[self._fonemas[6].get_fonema_ipa().replace(u'ː', u'') + u'ː']
        else:
            self._fonemas[7] = self._fonemas[6]
            self._fonemas[6] = fonema_coda
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def prepend_alofono_coda(self, alofono_coda):
        u"""Se añade por delante un alófono de coda

        :type alofono_coda: AlofonoConsonante
        :param alofono_coda: El alófono que se va añadir
        :return: None
        """
        self._alofonos[7] = self._alofonos[6]
        self._alofonos[6] = alofono_coda
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def set_fonemas_coda(self, fonemas_coda):
        u"""Se fijan los fonemas de coda

        :type fonemas_coda: [FonemaConsonante]
        :param fonemas_coda: La lista que se van a poner como coda
        :return: None
        """
        fonemas_coda = fonemas_coda[:2]
        self._fonemas = self._fonemas[:6] + fonemas_coda + ([FONEMA_VACIO] * (2 - len(fonemas_coda))) +\
            self._fonemas[8:]
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def set_alofonos_coda(self, alofonos_coda):
        u"""Se fijan los alófonos de coda

        :type alofonos_coda: [AlofonoConsonante]
        :param alofonos_coda: La [AlofonoConsonante] que meteremos como coda
        :return: None
        """
        alofonos_coda = alofonos_coda[:2]
        self._alofonos = self._alofonos[:6] + alofonos_coda + ([ALOFONO_VACIO] * (2 - len(alofonos_coda))) +\
            self._alofonos[8:]
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def reset_grafemas_coda(self):
        u"""Se eliminan los grafemas de coda. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._grafemas = self._grafemas[:5] + [[]] + self._grafemas[6:]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
        return self

    def reset_fonemas_coda(self):
        u"""Se eliminan los fonemas de coda. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._fonemas = self._fonemas[:6] + ([FONEMA_VACIO] * 2) + [self._fonemas[8]]
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
        return self

    def reset_alofonos_coda(self):
        u"""Se eliminan los alófonos de coda. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._alofonos = self._alofonos[:6] + ([ALOFONO_VACIO] * 2) + [self._alofonos[8]]
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def reset_coda(self):
        u"""Se eliminan los grafemas/fonemas/alófonos de coda. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.reset_grafemas_coda()
        self.reset_fonemas_coda()
        self.reset_alofonos_coda()
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def alarga_fonema_coda(self):
        u"""Se toma el primer fonema de coda y se reemplaza por su versión larga.

        :return: None
        """
        if self._fonemas[6].get_fonema_ipa():
            self._fonemas[6] = FONEMAS[self._fonemas[6].get_fonema_ipa().replace(u'ː', u'') + u'ː']
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def recorta_coda(self):
        u"""Se elimina el último fonema de coda.

        :return: None
        """
        indice = 7 if self._fonemas[7].get_fonema_ipa() else 6
        self._fonemas[indice] = FONEMA_VACIO
        self._alofonos[indice] = ALOFONO_VACIO
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def get_grafemas_rima(self, incluye_pausas=False):
        u"""Devuelve la lista de grafemas de núcleo y coda (incluyendo o no los de pausa posterior)

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: [Grafema]
        :return: La lista con los grafemas en posicion de coda en esta sílaba (más los de pausa, según el parámetro)
        """
        return [grafema for posicion in self._grafemas[2:7 if incluye_pausas else 6] for grafema in posicion]

    def get_fonemas_rima(self, incluye_pausas=False):
        u"""Devuelve la lista de fonemas de núcleo y coda (incluyendo o no los de pausa posterior)

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: [Fonema]
        :return: La lista con los fonemas en posicion de núcleo y coda en esta sílaba
        """
        return [fonema for fonema in self._fonemas[3:9 if incluye_pausas else 8] if fonema.get_fonema_ipa()]

    def get_alofonos_rima(self, incluye_pausas=False):
        u"""Devuelve la lista de alófonos de núcleo y coda (incluyendo o no los de pausa posterior)

        :type incluye_pausas: bool
        :param incluye_pausas: True si se deben incluir las pausas, False si no
        :rtype: [Alofono]
        :return: La lista con los alófonos en posicion de núcleo y coda en esta sílaba
        """
        return [alofono for alofono in self._alofonos[3:9 if incluye_pausas else 8] if alofono.get_fonema_padre_ipa()]

    def get_grafemas_pausa_posterior(self):
        u"""Devuelve la lista de grafemas de pausa posterior

        :rtype: [Grafema]
        :return: La lista con los grafemas en posicion de pausa posterior
        """
        return self._grafemas[6]

    def get_fonema_pausa_posterior(self):
        u"""Devuelve el fonema pausa posterior si hay, o None si no

        :rtype: FonemaPausa
        :return: El Fonema de pausa posterior, o None si no tiene
        """
        return self._fonemas[8] if self._fonemas[8].get_fonema_ipa() else None

    def get_alofono_pausa_posterior(self):
        u"""Devuelve el alófono de pausa posterior si hay, o None si no

        :rtype: AlofonoPausa
        :return: El Alofono de pausa posterior, o None si no tiene
        """
        return self._alofonos[8] if self._alofonos[8].get_alofono_ipa() else None

    def append_grafema_pausa_posterior(self, grafema_pausa):
        u"""Se añade por detrás un grafema de pausa

        :type grafema_pausa: Grafema
        :param grafema_pausa: El grafema que se va añadir
        :return: None
        """
        self._grafemas[6].append(grafema_pausa)
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def prepend_grafema_pausa_posterior(self, grafema_pausa):
        u"""Se añade por delante un grafema de pausa posterior

        :type grafema_pausa: Grafema
        :param grafema_pausa: El grafema que se va añadir
        :return: None
        """
        self._grafemas[6] = [grafema_pausa] + self._grafemas[6]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.

    def set_fonema_pausa_posterior(self, fonema_pausa):
        u"""Se fija el fonema de vocal

        :type fonema_pausa: FonemaPausa
        :param fonema_pausa: El fonema de pausa
        :return: None
        """
        self._fonemas[8] = fonema_pausa
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.

    def set_alofono_pausa_posterior(self, alofono_pausa):
        u"""Se fija el alofono de pausa posterio

        :type alofono_pausa: AlofonoPausa
        :param alofono_pausa: El alófono de pausa
        :return: None
        """
        self._alofonos[8] = alofono_pausa
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def reset_grafemas_pausa_posterior(self):
        u"""Se eliminan los grafemas de pausa posterior. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._grafemas = self._grafemas[:6] + [[]]
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
        return self

    def reset_fonema_pausa_posterior(self):
        u"""Se elimina el fonema de pausa posterior. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._fonemas = self._fonemas[:8] + [FONEMA_VACIO]
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
        return self

    def reset_alofono_pausa_posterior(self):
        u"""Se elimina el alófono de pausa posterior. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self._alofonos = self._alofonos[:8] + [ALOFONO_VACIO]
        if DEBUG:
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def reset_pausa_posterior(self):
        u"""Se eliminan los grafemas/fonema/alófono de pausa posterior. Devolvemos la sílaba tras el cambio.

        :rtype: Silaba
        :return: La sílaba, tras realizar el reseteo
        """
        self.reset_grafemas_pausa_posterior()
        self.reset_fonema_pausa_posterior()
        self.reset_alofono_pausa_posterior()
        if DEBUG:
            self.__trans_ort = self.transcribe_ortograficamente_silaba(False, True)  # Para el debugging.
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.
        return self

    def get_tonica(self):
        u"""Devuelve el valor de la tonicidad de esta sílaba.

        :rtype: unicode
        :return: el str que representa la tonicidad (u'' si es átona, o el símbolo de tipo de acento IPA)
        """
        return self._tonica

    def set_tonica(self, tonica):
        u"""Marca esta sílaba como tónica, con el tipo de acento que indica el parámetro.

        :type tonica: unicode
        :param tonica: un string con el valor de tonicidad de esta sílaba (u'' si es átona o el símbolo IPA que toque)
        :return: None
        """
        self._tonica = tonica
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def acorta_segmentos_largos(self):
        u"""Busca fonemas y alófonos largo y los sustituye por sus variedades de duración normal.

        En principio, puede haber consonantes largas en ataque o coda, o vocales en el núcleo.

        :return: None
        """
        fonemas_ataque = self.get_fonemas_ataque()
        fonemas_ataque_cortos = []
        alofonos_ataque = self.get_alofonos_ataque()
        alofonos_ataque_cortos = []
        for orden_fonema_ataque, fonema_ataque in enumerate(fonemas_ataque):
            fonema_ataque_ipa = fonema_ataque.get_fonema_ipa()
            if u'ː' in fonema_ataque_ipa:
                fonema_ataque_corto = FONEMAS[fonema_ataque_ipa.replace(u'ː', u'')]
            else:
                fonema_ataque_corto = fonema_ataque
            fonemas_ataque_cortos.append(fonema_ataque_corto)
            if orden_fonema_ataque < len(alofonos_ataque):
                alofono_ataque = alofonos_ataque[orden_fonema_ataque]
                alofono_ataque_ipa = alofono_ataque.get_alofono_ipa()
                if u'ː' in alofono_ataque_ipa:
                    alofono_ataque_corto_ipa = alofono_ataque_ipa.replace(u'ː', u'')
                    for alofono_ataque_corto in ALOFONOS_ATAQUE[fonema_ataque_corto.get_fonema_ipa()]:
                        if alofono_ataque_corto.get_alofono_ipa() == alofono_ataque_corto_ipa:
                            alofonos_ataque_cortos.append(alofono_ataque_corto)
                            break
                else:
                    alofonos_ataque_cortos.append(alofono_ataque)
        self.set_fonemas_ataque(fonemas_ataque_cortos)
        self.set_alofonos_ataque(alofonos_ataque_cortos)

        # Miramos la vocal
        fonema_vocal_ipa = self.get_fonema_vocal().get_fonema_ipa()
        alofono_vocal_ipa = self.get_alofono_vocal().get_alofono_ipa()
        if u'ː' in fonema_vocal_ipa + alofono_vocal_ipa:
            fonema_vocal_corto_ipa = fonema_vocal_ipa.replace(u'ː', u'')
            self.set_fonema_vocal(FONEMAS[fonema_vocal_corto_ipa])
            alofono_vocal_ipa = self.get_alofono_vocal().get_alofono_ipa()
            alofono_vocal_corta_ipa = alofono_vocal_ipa.replace(u'ː', u'')
            for alofono in (ALOFONOS_NUCLEO_ORALES[fonema_vocal_corto_ipa]
                            if fonema_vocal_corto_ipa in ALOFONOS_NUCLEO_ORALES else
                            ALOFONOS_NUCLEO_NASALES[fonema_vocal_corto_ipa]):
                if alofono.get_alofono_ipa() == alofono_vocal_corta_ipa:
                    self.set_alofono_vocal(alofono)

        # Vamos a por la coda
        fonemas_coda = self.get_fonemas_coda()
        fonemas_coda_cortos = []
        alofonos_coda = self.get_alofonos_coda()
        alofonos_coda_cortos = []
        for orden_fonema_coda, fonema_coda in enumerate(fonemas_coda):
            fonema_coda_ipa = fonema_coda.get_fonema_ipa()
            if u'ː' in fonema_coda_ipa:
                fonema_coda_corto = FONEMAS[fonema_coda_ipa.replace(u'ː', u'')]
            else:
                fonema_coda_corto = fonema_coda
            fonemas_coda_cortos.append(fonema_coda_corto)
            if orden_fonema_coda < len(alofonos_coda):
                alofono_coda = alofonos_coda[orden_fonema_coda]
                alofono_coda_ipa = alofono_coda.get_alofono_ipa()
                if u'ː' in alofono_coda_ipa:
                    alofono_coda_corto_ipa = alofono_coda_ipa.replace(u'ː', u'')
                    for alofono_coda_corto in ALOFONOS_CODA[fonema_coda_corto.get_fonema_ipa()]:
                        if alofono_coda_corto.get_alofono_ipa() == alofono_coda_corto_ipa:
                            alofonos_coda_cortos.append(alofono_coda_corto)
                            break
                else:
                    alofonos_coda_cortos.append(alofono_coda)
        self.set_fonemas_coda(fonemas_coda_cortos)
        self.set_alofonos_coda(alofonos_coda_cortos)

        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
            self.__trans_alo = self.transcribe_foneticamente_silaba(True, True, True)  # Para el debugging.

    def fuerza_fonemas_aparentes(self):
        u"""Cambia los fonemas por sus fonemas aparentes según el alófono que hayan expresado dichos fonemas.

        El fonema aparente es aquel que coincide con la representación del alófono. Es decir, si por circunstancias
        fonéticas el fonema /n/ se expresa como [m] (como en <convino>), se cambia dicho fonema /n/ por el fonema /m/
        como si la ortografía fuera <combino>. Aparte de las nasales, esto afecta a oclusivas (se sonorizan en coda)
        y en general a todos aquellos fonemas que tengan algún alófono que coincida con un fonema distinto.

        :return: None
        """
        for orden_fonema in range(0, 9):
            fonema_aparente_ipa = self._alofonos[orden_fonema].get_fonema_aparente_ipa()
            self._fonemas[orden_fonema] = FONEMAS[fonema_aparente_ipa] \
                if fonema_aparente_ipa else FONEMA_VACIO
        if DEBUG:
            self.__trans_fon = self.transcribe_fonologicamente_silaba(True, True, True, False)  # Para el debugging.
