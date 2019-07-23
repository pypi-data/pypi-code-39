#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona las clases Palabra y Juntura (una especialización de Palabra), utilizadas para estructurar el texto.

La clase Palabra toma el texto de entrada y crea una estructura interna de la palabra, organizada en sílabas, que
a su vez contienen grafemas, fonemas y alófonos y tiene una serie de características propias, como la tonicidad.
También se tiene una serie de métodos auxiliares que tratan cadenas de texto y extraen los signos de puntuación y otros.

La clase Juntura es una especialización de la clase Palabra y se utiliza para realizar el resilabeo: se crea una
Palabra con dos sílabas en contacto de dos palabras distintas, y se reorganizan los fonemas y se recalculan alófonos.
"""

from __future__ import print_function
import re
from num2words import num2words
import unicodedata
from roman import fromRoman, InvalidRomanNumeralError
from dateutil.parser import parse
from nltk.tokenize import RegexpTokenizer

from iar_transcriber.fras_consts import MESES
from iar_transcriber.pal_consts import PALABRAS_ATONAS
from iar_transcriber.silaba import Silaba
from iar_transcriber.sil_consts import ATON, ACPR, ACSC
from iar_transcriber.grafema import Digrafo, GrafemaConsonante, GrafemaSemiconsonante, GrafemaVocal, GrafemaSemivocal,\
    GrafemaMudo, GrafemaPausa, MonografoPausa, MonografoOrdinal, GrafemaVocoide, GrafemaNumero, GrafemaSimbolo
from iar_transcriber.graf_consts import MONOGRAFOS, MASC, TILDES_OPUESTAS, DIGRAFOS
from iar_transcriber.fonema import FonemaSemiconsonante
from iar_transcriber.fon_consts import FONEMAS, CERR, ANTE, LADE, DEAL, POAL, PALA, NASA, OCLU, LATE, VIBS
from iar_transcriber.alof_consts import ALOFONOS_CODA, ALOFONOS_ATAQUE, ALOFONOS_PAUSA, ALOFONOS_NUCLEO_NASALES, ALOFONOS_NUCLEO_ORALES

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Palabra:
    u"""La clase Palabra es una representación estructurada (fonética, alofónica y ortográficamente) de una palabra.

    En esta clase se convierte una palabra (representada por un string) en una representación estructurada.
    Se convierten los caracteres a grafemas agrupándolos según corresponda (por ejemplo, dígrafos), y desambiguando
    su valor fonético. Después se silabean los fonemas, y tras ello se calculan los alófonos con los que se expresan.

    La clase tiene únicamente un atributo: una lista de objetos Silaba, que estructuran cada una de las sílabas de
    la palabra.
    """

    def __init__(self, palabra_texto=u'', silabas=None, calcula_alofonos=True, inserta_epentesis=False,
                 organiza_grafemas=False):
        u""" El constructor para los objetos de la clase Palabra

        :type palabra_texto: unicode
        :param palabra_texto: El texto que queremos procesar y convertir en un objeto Palabra. Si se da la
            lista de sílabas para construir el objeto, se obvia este parámetro. Las palabras se procesan junto con
            los caracteres de pausa y signos ortográficos que tenga a su alrededor.
        :type silabas: [Silaba]
        :param silabas: Es posible construir el objeto palabra a partir de una lista de sílabas en vez de
            utilizar un str. Así podemos modificar las sílabas, añadir, modificar, y crear la palabra a partir de
            ellas. También se utiliza cuando se realiza el resilabeo, para recalcular los fonemas/alófonos en las
            junturas entre palabras.
        :type calcula_alofonos: bool
        :param calcula_alofonos: Por defecto se calculan únicamente los fonemas. Si este parámetro está a
            True, entonces también se crea la estructura de alófonos y se calculan sus realizaciones.
        :type inserta_epentesis: bool
        :param inserta_epentesis: Si está a True, entonces se inserta una e
        :type organiza_grafemas: bool
        :param organiza_grafemas: Si está a True, se crea la estructura de grafemas organizados en sílabas y colocados
            dentro de ella en sus posiciones correspondientes. Si está a False, no se crea esta estructura y por lo
            tanto no se podrá realizar la transcripción ortográfica de la palabra (aunque haciéndolo así, la
            transcripción fonética es más rápida).
        """
        if silabas:
            # Se usa en caso de que seamos una Juntura (subclase de Palabra). También si hacemos modificaciones
            # en palabras.
            self._silabas = silabas
            if calcula_alofonos:
                self.calcula_alofonos()
        elif palabra_texto:
            # Lo más habitual es crear la palabra a partir de sus representación como cadena de caracteres
            self._silabas = self.silabea(palabra_texto, inserta_epentesis, organiza_grafemas)
            if calcula_alofonos and self.get_fonemas(incluye_pausas=True):
                self.calcula_alofonos()
        else:
            # Palabra vacía
            self._silabas = []

    def get_silabas(self):
        u"""Devuelve la lista de sílabas de la palabra.

        :rtype: [Silaba]
        :return: Devuelve una lista de objetos Silaba que representa a la palabra como lista (ordenada) de sílabas.
        """
        return self._silabas

    def get_silaba(self, orden_silaba=-1):
        u"""Devuelve la sílaba en la posición indicada

        :rtype: Silaba
        :return: Devuelve un objeto Silaba que representa a la sílaba indicada por el parámetro.
        """
        return self._silabas[orden_silaba]

    def get_grafemas(self, incluye_pausas=False):
        u"""Devuelve una lista con los grafemas presentes en la palabra. Incluye o no las pausas según el parámetro.

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluyen los posibles grafemas de pausas. Si no, no se incluyen.
        :rtype: [Grafema]
        :return: Devuelve una lista de objetos Grafema que representa a la palabra como lista (ordenada) de grafemas
        """
        return [grafema for silaba in self._silabas for grafema in silaba.get_grafemas(incluye_pausas)]

    def get_fonemas(self, incluye_pausas=False):
        u"""Devuelve una lista con los fonemas presentes en la palabra. Incluye o no las pausas según el parámetro.

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluyen los posibles fonemas de pausas. Si no, no se incluyen.
        :rtype: [Fonema]
        :return: Devuelve una lista de objetos Fonema que representa a la palabra como lista (ordenada) de fonemas
        """
        return [fonema for silaba in self._silabas for fonema in silaba.get_fonemas(incluye_pausas)]

    def get_alofonos(self, incluye_pausas=False):
        u"""Devuelve una lista con los alófonos presentes en la palabra. Incluye o no las pausas según el parámetro.

        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True se incluyen los posibles alófonos de pausas. Si no, no se incluyen.
        :rtype: [Alofono]
        :return: Devuelve una lista de objetos Alofono que representa a la palabra como lista (ordenada) de alófonos
        """
        return [alofono for silaba in self._silabas for alofono in silaba.get_alofonos(incluye_pausas)]

    @staticmethod
    def es_palabra_tonica(palabra_texto):
        u"""Devuelve el booleano que dice si la palabra es tónica (tiene alguna sílaba tónica) o no (es átona)

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres que conforma la palabra
        :rtype: bool
        :return: True si la palabra tiene alguna sílaba tónica (lo habitual), False si no (palabras gramaticales)
        """
        # Eliminamos pausas y símbolos de la derecha
        posicion_final = len(palabra_texto) - 1
        while posicion_final > 0 and palabra_texto[posicion_final] in MONOGRAFOS \
                and (isinstance(MONOGRAFOS[palabra_texto[posicion_final]][0], GrafemaPausa) or
                     isinstance(MONOGRAFOS[palabra_texto[posicion_final]][0], GrafemaSimbolo) or
                     (isinstance(MONOGRAFOS[palabra_texto[posicion_final]][0], GrafemaMudo) and
                      palabra_texto[posicion_final].lower() != u'h')):
            posicion_final -= 1
        # Eliminamos pausas y símbolos de la izquierda
        posicion_inicial = 0
        while posicion_inicial <= posicion_final and palabra_texto[posicion_inicial] in MONOGRAFOS\
                and (isinstance(MONOGRAFOS[palabra_texto[posicion_inicial]][0], GrafemaPausa) or
                     isinstance(MONOGRAFOS[palabra_texto[posicion_inicial]][0], GrafemaSimbolo) or
                     (isinstance(MONOGRAFOS[palabra_texto[posicion_inicial]][0], GrafemaMudo) and
                      palabra_texto[posicion_inicial].lower() != u'h')):
            posicion_inicial += 1
        return posicion_inicial < posicion_final and\
            palabra_texto[posicion_inicial:posicion_final + 1].lower() not in PALABRAS_ATONAS

    def get_posicion_tonica(self):
        u"""Devuelve la posición de la sílaba tónica (CONTADA DESDE EL FINAL) o 0 si es átona.

        La sílaba tónica es aquella en la recaiga el acento primario.

        :rtype: int
        :return: la posición de la sílaba tónica: 0 si es átona, -1 si es aguda, -2 llana, -3 esdrújula...
        """
        silabas = [(o, s) for (o, s) in enumerate(self._silabas) if s.get_tonica() == ACPR]
        if not silabas:  # Palabra átona
            return 0  # El resultado 0 significa "palabra átona"
        # Devolvemos el orden inverso de la única sílaba con ACPR.
        return silabas[0][0] - len(self._silabas)

    def contiene_hiato(self):
        u"""Devuelve True si la palabra contiene un hiato, o False si no

        :rtype: bool
        :return: True si hay hiato, False si no
        """
        posicion_tonica = self.get_posicion_tonica()
        if posicion_tonica == 0:  # Palabra átona. Nunca tienen tilde, y por tanto, no tienen hiatos
            return False
        silaba_tonica = self._silabas[posicion_tonica]
        # Si la sílaba tónica no es la primera, y además no tiene ataque ni semiconsonante (en principio si hubiera
        # solo semiconsonante y no consonante se habría consonantizado la semiconsonante, así que no sería posible que
        # no hubiera ataque y sí semiconsonante, pero las cosas cambian) y además tiene vocal cerrada, hay hiato. Esto
        # es debido a que en este caso además es imposible que la sílaba anterior tenga coda, con lo que estaría en
        # contacto con (semi)vocal. Esto sería un hiato "a derechas": baúl, raíl...
        # También lo hay si la sílaba tónica no es la última no tiene coda ni semivocal y es cerrada, y la sílaba
        # que sigue no tiene ni ataque ni semiconsonate (mismo comentario sobre la semiconsonante que antes).
        if silaba_tonica.get_fonema_vocal().get_abertura() == CERR and\
                ((abs(posicion_tonica) < len(self._silabas) and not silaba_tonica.get_fonemas_ataque() and
                  not silaba_tonica.get_fonema_semiconsonante()) or
                 (posicion_tonica != -1 and not silaba_tonica.get_fonemas_coda() and
                  not silaba_tonica.get_fonema_semivocal() and
                  not self._silabas[posicion_tonica + 1].get_fonemas_ataque() and
                  not self._silabas[posicion_tonica + 1].get_fonema_semiconsonante())):
            return True
        return False

    def set_tilde(self, con_tilde):
        u"""Hace cambios en los grafemas de las sílabas para cambiar entre grafema con o sin tilde según se indique.

        Además, tras realizar el cambio devuelve una cadena de texto con la palabra modificada

        :type con_tilde: bool
        :param con_tilde: Si es True se tilda la tónica, si es False se elimina la tilde.
        :rtype: unicode
        :return: La transcripción ortográfica de la palabra tras poner/quitar la tilde
        """
        posicion_tonica = self.get_posicion_tonica()  # Consideramos que sólo la sílaba tónica puede llevar tilde.
        if posicion_tonica != 0:  # Si no hay sílabas tónicas, no habrá tilde que quitar
            nueva_vocal = []  # Puede haber más de un grafema, por ejemplo si hay mudos
            for grafema_vocal in self._silabas[posicion_tonica].get_grafemas_vocal():
                # Puede haber grafemas mudos que no hay que tocar
                grafema_texto = grafema_vocal.get_grafema_txt()
                if grafema_texto in TILDES_OPUESTAS and con_tilde != grafema_vocal.get_tilde():
                    # Cambiamos el grafema de vocal acentuada por el de la vocal sin acentuar o a la inversa
                    grafema_vocal = MONOGRAFOS[TILDES_OPUESTAS[grafema_texto]][0]
                nueva_vocal.append(grafema_vocal)
            self._silabas[posicion_tonica].set_grafemas_vocal(nueva_vocal)
        return self.transcribe_ortograficamente_palabra(marca_tonica=False, incluye_pausas=True,
                                                        separador=u'', apertura=u'', cierre=u'')

    def ajusta_tildes(self):
        u"""Según la tonicidad expresada en las sílabas, se ajustan las tildes de los grafemas vocales.

        Para ello se siguen las normas de la RAE, y también se acentúan convenientemente los hiatos.
        Cuando creamos una palabra, le podemos añadir o quitar posteriormente sílabas (sufijos), pero no modificar la
        tonicidad, que se suele mantener en la misma sílaba. Pero para asegurarnos de que tras el cambio la tilde de
        la sílaba tónica es correcta, se usa este método.

        :rtype: unicode
        :return: La trascripción ortográfica tras haber tildado o no según corresponda
        """
        self.set_tilde(con_tilde=False)
        if self.contiene_hiato():
            # Los hiatos siempre se acentúan.
            self.set_tilde(con_tilde=True)
        else:
            posicion_tonica = self.get_posicion_tonica()
            # Si la posición tónica es 0, la palabra es átona y no lleva tilde, simplemente devolvemos lo que hay
            if posicion_tonica in [-1, -2]:
                if len(self._silabas) > 1:  # Los monosílabos no se tildan. OJO: Diacríticos
                    # Analizamos la palabra ortográficamente. Ahora mismo no hay tilde, y vemos si la palabra
                    # resultante es aguda o llana. Si no coincide este análisis con la tonicidad ya conocida de la
                    # palabra, tendremos que poner la tilde.
                    se_lee_llana = False
                    grafemas_coda = self._silabas[-1].get_grafemas_coda()
                    if grafemas_coda:
                        if grafemas_coda[-1].get_grafema_txt()[-1].lower() in u'ns':
                            # Polisílaba y en -n/-s. Sin tildes, es llana
                            se_lee_llana = True
                    else:
                        grafemas_semivocal = self._silabas[-1].get_grafemas_semivocal()
                        if grafemas_semivocal:
                            if grafemas_semivocal[-1].get_grafema_txt()[-1].lower() in u'iu':
                                # Polisílaba y acabada en semivocal ortográficamente "i"/"u". Sin tildes, es llana
                                se_lee_llana = True
                        else:
                            grafema_vocal = self._silabas[-1].get_grafemas_nucleo()[-1]
                            if grafema_vocal.get_grafema_txt() in u'ieaou':  # La vocal puede ser "y": tepuy
                                # Polisílaba, sin coda final y acabada en vocal. Sin tildes, es llana
                                se_lee_llana = True
                    if (posicion_tonica == -1 and se_lee_llana) or (posicion_tonica == -2 and not se_lee_llana):
                        self.set_tilde(con_tilde=True)
            elif posicion_tonica <= -3:  # Palabra (sobre)esdrújula
                self.set_tilde(con_tilde=True)
        return self.transcribe_ortograficamente_palabra(marca_tonica=False, incluye_pausas=True,
                                                        separador=u'', apertura=u'', cierre=u'')

    @staticmethod
    def extrae_grafemas(palabra_texto):
        u"""Toma una cadena de caracteres y extrae los grafemas que la componen.

        Devuelve la lista de grafemas (teniendo en cuenta dígrafos). Cada grafema incluye la información del fonema
        que representa. Como un mismo carácter puede hacer referencia a más de un fonema (según el entorno),
        la lista devuelta ya está desambiguada, incluyendo los grafemas con la expresión fonética adecuada.

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres que conforma la palabra.
        :rtype: [Grafema]
        :return: La lista de grafemas desambiguados (pero no silabeados)
        """
        longitud = len(palabra_texto)
        posicion = 0
        grafemas_multifonemicos = []
        # Para cada carácter o grupo de caracteres, extraemos la lista de grafemas que puede representar, cada uno de
        # ellos con su realización fonética.
        while posicion < longitud:
            posibles_grafemas = ()
            # Primero probamos con los dígrafos.
            if posicion + 1 < longitud:
                # Hay al menos dos caracteres, probemos con los dígrafos antes.
                doble_caracter = palabra_texto[posicion:posicion + 2]
                if doble_caracter in DIGRAFOS:
                    for posible_grafema in DIGRAFOS[doble_caracter]:
                        # Podría ser "gu", o "tz" a final de palabra, así que comprobamos que no sean dos monógrafos.
                        # También daría problemas una combinación, no muy legal, de tipo "párrroco", con una erre larga
                        # o algo como polllo, que debería ser pol.llo.
                        if posible_grafema.es_grafema_compatible([],
                                                                 MONOGRAFOS[palabra_texto[posicion + 2]]
                                                                 if (posicion + 2 < longitud and
                                                                     palabra_texto[posicion + 2] in MONOGRAFOS) else [],
                                                                 [],
                                                                 []):
                            posibles_grafemas = (posible_grafema, )
                            posicion += 2
                            break

            if not posibles_grafemas:
                # No hemos encontrado un dígrafo. Probaremos con los monógrafos.
                caracter = palabra_texto[posicion]
                if caracter in MONOGRAFOS:
                    # Está. Lo cogemos.
                    posibles_grafemas = MONOGRAFOS[caracter]
                else:
                    caracter_normalizado = unicodedata.normalize('NFKD', caracter).encode('ascii', 'ignore')
                    if caracter_normalizado in MONOGRAFOS:
                        # Hemos hecho una conversión del tipo: führer -> fuhrer.
                        posibles_grafemas = MONOGRAFOS[caracter_normalizado]
                posicion += 1

            grafemas_multifonemicos += [posibles_grafemas] if posibles_grafemas else []

        # Eliminamos todas las opciones fonéticas inválidas y dejamos una única variante fonética por grafema.
        grafemas_monofonemicos = []
        if not grafemas_multifonemicos:
            # Si la palabra está vacía, no hay nada que hacer
            return grafemas_monofonemicos
        for orden_grafema_multifonemico, grafema_multifonemico in enumerate(grafemas_multifonemicos):
            if len(grafema_multifonemico) == 1:
                # Este grafema siempre se corresponde con un único fonema, así que no hay problemas.
                grafemas_monofonemicos += [grafema_multifonemico[0]]
                continue

            distancia_a_previo = 1
            grafema_previo = grafemas_monofonemicos[orden_grafema_multifonemico - distancia_a_previo]\
                if orden_grafema_multifonemico - distancia_a_previo >= 0 else None
            while grafema_previo and isinstance(grafema_previo, GrafemaMudo):
                # Saltamos el grafema mudo.
                distancia_a_previo += 1
                if orden_grafema_multifonemico - distancia_a_previo >= 0:
                    grafema_previo = grafemas_monofonemicos[orden_grafema_multifonemico - distancia_a_previo]
                else:
                    grafema_previo = None
                    break
            distancia_a_posterior = 1
            grafema_multifonemico_posterior = grafemas_multifonemicos[orden_grafema_multifonemico +
                                                                      distancia_a_posterior]\
                if orden_grafema_multifonemico + distancia_a_posterior < len(grafemas_multifonemicos) else None
            while grafema_multifonemico_posterior and isinstance(grafema_multifonemico_posterior[0], GrafemaMudo):
                # Saltamos el grafema mudo.
                distancia_a_posterior += 1
                if orden_grafema_multifonemico + distancia_a_posterior < len(grafemas_multifonemicos):
                    grafema_multifonemico_posterior = grafemas_multifonemicos[orden_grafema_multifonemico +
                                                                              distancia_a_posterior]
                else:
                    grafema_multifonemico_posterior = None
                    break
            # Necesitamos el grafema post-posterior porque puede hacer cambios:
            # muy -> cuyo (de semic.+vocal -> vocal+consonante)
            distancia_a_post_posterior = distancia_a_posterior + 1
            grafema_multifonemico_post_posterior = grafemas_multifonemicos[orden_grafema_multifonemico +
                                                                           distancia_a_post_posterior]\
                if orden_grafema_multifonemico + distancia_a_post_posterior < len(grafemas_multifonemicos) else None
            while grafema_multifonemico_post_posterior and isinstance(grafema_multifonemico_post_posterior[0],
                                                                      GrafemaMudo):
                # Saltamos el grafema mudo.
                distancia_a_post_posterior += 1
                if orden_grafema_multifonemico + distancia_a_post_posterior < len(grafemas_multifonemicos):
                    grafema_multifonemico_post_posterior = grafemas_multifonemicos[orden_grafema_multifonemico +
                                                                                   distancia_a_post_posterior]
                else:
                    grafema_multifonemico_post_posterior = None
                    break

            # Necesitamos el grafema post-post-posterior porque puede hacer cambios:
            # uiu -> uyu; uiui -> güigüi
            distancia_a_post_post_posterior = distancia_a_post_posterior + 1
            grafema_multifonemico_post_post_posterior = grafemas_multifonemicos[orden_grafema_multifonemico +
                                                                                distancia_a_post_post_posterior]\
                if orden_grafema_multifonemico + distancia_a_post_post_posterior < len(grafemas_multifonemicos)\
                else None
            while grafema_multifonemico_post_post_posterior and\
                    isinstance(grafema_multifonemico_post_post_posterior[0], GrafemaMudo):
                # Saltamos el grafema mudo.
                distancia_a_post_post_posterior += 1
                if orden_grafema_multifonemico + distancia_a_post_post_posterior < len(grafemas_multifonemicos):
                    grafema_multifonemico_post_post_posterior = \
                        grafemas_multifonemicos[orden_grafema_multifonemico + distancia_a_post_post_posterior]
                else:
                    grafema_multifonemico_post_post_posterior = None
                    break

            # Tras haber extraído los fonemas no mudos previos y anteriores, procedemos a desambiguar el valor
            # fonético de los grafemas que puedan tener más de una representación fonética.
            for orden_variante_fonetica, variante_fonetica in enumerate(grafema_multifonemico):
                if variante_fonetica.es_grafema_compatible(grafema_previo,
                                                           grafema_multifonemico_posterior,
                                                           grafema_multifonemico_post_posterior,
                                                           grafema_multifonemico_post_post_posterior,
                                                           distancia_a_previo):
                    grafemas_monofonemicos += [variante_fonetica]
                    break
            else:
                # Si no encuentra ninguno, es un error, pero metemos la última opción.
                grafemas_monofonemicos += [grafema_multifonemico[-1]]
                print(u'NINGÚN FONEMA PARA EL GRAFEMA', grafema_multifonemico[-1], palabra_texto)

        return grafemas_monofonemicos

    @staticmethod
    def silabea(palabra_texto, inserta_epentesis=False, organiza_grafemas=False):
        u"""
        silabea(str palabra_texto, bool inserta_epentesis=False, bool organiza_grafemas=True) -> [Silaba]

        Este método es de los más importantes de la clase: toma una lista de objetos Grafema (que incluye el valor del
        fonema concreto al que representa) y los agrupa en sílabas, ubicándolos en su posición adecuada dentro de la
        estructura de la sílaba.
        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres que representa la palabra.
        :type inserta_epentesis: bool
        :param inserta_epentesis: Si está a True realiza epéntesis fonética de una /e/ si la palabra empieza
            por /s/ seguida de consonante. Por defecto no la mete, y en cualquier caso se mete sólo en la representación
            fonética y no en la ortográfica.
        :type organiza_grafemas: bool
        :param organiza_grafemas: Si está a True, se introducen los mudos dentro de la sílaba (solo afecta a la
            transcripción ortográfica).
        :rtype: [Silaba]
        :return: La lista de objetos de la clase Silaba
        """
        grafemas = Palabra.extrae_grafemas(palabra_texto)
        silabas = []
        indices_vocales = []
        indices_semiconsonantes = []
        indices_semivocales = []
        indices_consonantes = []
        indices_ataques = []
        indices_codas = []
        indices_mudos = []
        indices_pausas = []
        # PROCESADO DE VOCALES
        # Creamos tantas sílabas como vocales y creamos los índices de grafemas para cada tipo de grafema.
        for orden_grafema, grafema in enumerate(grafemas):
            if isinstance(grafema, GrafemaVocal):
                indices_vocales.append(orden_grafema)
                # Se crea la estructura silábica: una sílaba por vocal
                silaba = Silaba()
                silaba.set_fonema_vocal(FONEMAS[grafema.get_fonemas_ipa()[0]])
                if organiza_grafemas:
                    silaba.append_grafema_vocal(grafema)
                # Si hay tilde, lo marcamos en principio como acento primario (quizá sea secundario, como en hábilmente)
                silaba.set_tonica(ACPR if grafema.get_tilde() else ATON)
                silabas.append(silaba)
            elif isinstance(grafema, GrafemaSemiconsonante):
                # OJO: en cosas como huevo -> gwebo, la u semiconsonante se representa como grafema consonántico
                # con doble fonema (como la <x>), donde el segundo es la semiconsonante w.
                indices_semiconsonantes.append(orden_grafema)
            elif isinstance(grafema, GrafemaSemivocal):
                indices_semivocales.append(orden_grafema)
            elif isinstance(grafema, GrafemaConsonante):
                indices_consonantes.append(orden_grafema)
            elif isinstance(grafema, GrafemaMudo):
                indices_mudos.append(orden_grafema)
            elif isinstance(grafema, GrafemaPausa):
                indices_pausas.append(orden_grafema)
        if not indices_vocales:
            # Como se han calculado las "palabras legibles", si no hay ni una vocal, es que tenemos un signo de
            # puntuación sin más. Creamos una sílaba vacía y luego meteremos el grafema/fonema/alófono de pausa.
            silaba = Silaba()
            silabas.append(silaba)
            # La frase está inacabada y no tendrá caracteres alfabéticos. Metemos un valor ficticio para
            # que siga la lógica posterior.
            orden_ultimo_grafema_alfabetico = len(grafemas)
        else:
            orden_ultimo_grafema_alfabetico = next(len(grafemas) - 1 - orden_inverso
                                                   for orden_inverso, grafema in enumerate(grafemas[::-1])
                                                   if grafema.get_grafema_primario().lower() !=
                                                   grafema.get_grafema_primario().upper())

        # PROCESADO DE GLIDES
        # Metemos las semiconsonantes y semivocales en las sílabas que toque
        for orden_semiconsonante in indices_semiconsonantes:
            grafema = grafemas[orden_semiconsonante]
            # A la fuerza hay una vocal posterior a este grafema
            orden_silaba = next(indice for indice, posicion in enumerate(indices_vocales)
                                if posicion > orden_semiconsonante)
            silabas[orden_silaba].set_fonema_semiconsonante(FONEMAS[grafema.get_fonemas_ipa()[-1]])
            if organiza_grafemas:
                silabas[orden_silaba].append_grafema_semiconsonante(grafema)

        for orden_semivocal in indices_semivocales:
            grafema = grafemas[orden_semivocal]
            # A la fuerza hay una vocal anterior a este grafema
            orden_silaba = next(len(indices_vocales) - 1 - orden_inverso_silaba
                                for orden_inverso_silaba, orden_vocal in enumerate(indices_vocales[::-1])
                                if orden_vocal < orden_semivocal)
            silabas[orden_silaba].set_fonema_semivocal(FONEMAS[grafema.get_fonemas_ipa()[-1]])
            if organiza_grafemas:
                silabas[orden_silaba].append_grafema_semivocal(grafema)

        # PROCESADO DE CONSONANTES
        # Metemos las consonantes seguidas de vocoide como ataque (simple o 2º fonema de ataque complejo).
        # El resto de consonantes serán codas salvo que sean combinables en ataque complejo o geminado, o que sean
        # previas a la primera vocal.
        for orden_grafema in indices_consonantes[::-1]:
            grafema = grafemas[orden_grafema]
            orden_siguiente_no_mudo = orden_grafema + 1  # Primera aproximación
            if orden_siguiente_no_mudo <= orden_ultimo_grafema_alfabetico and\
                    orden_siguiente_no_mudo in indices_mudos:
                orden_siguiente_no_mudo = next(indice for indice in range(orden_siguiente_no_mudo + 1,
                                                                          orden_ultimo_grafema_alfabetico + 2)
                                               if indice not in indices_mudos or
                                               indice > orden_ultimo_grafema_alfabetico)
            if orden_siguiente_no_mudo in indices_codas + [orden_ultimo_grafema_alfabetico + 1]\
                    or (orden_siguiente_no_mudo in indices_semiconsonantes and
                        orden_siguiente_no_mudo > orden_grafema + 1):
                # Es coda, puesto que el siguiente grafema no mudo es una coda (o no hay más caracteres alfabéticos
                # después), o bien sigue una semiconsonante (que se consonantiza, pero bueno) con al menos un mudo
                # entre medias. Reconocemos cosas como exhuésped, sinhueso, deshielo... que silabeamos como
                # ex-hués-ped, sin-hue-so y des-hie-lo, consonantizando la semivocal (exgüésped, singüeso, desyelo).
                # Si no hay semivocal y mudo previo, como en inhóspito o exhumado, sí se mete como ataque
                # y silabeamos como i-nhós-pi-to y e-xhu-mado.
                indices_codas.append(orden_grafema)
                orden_silaba = next(len(indices_vocales) - 1 - orden_inverso_silaba
                                    for orden_inverso_silaba, orden_vocal in enumerate(indices_vocales[::-1])
                                    if orden_vocal < orden_grafema)
                # No se permiten laterales palatales en coda. Se cambia a la lateral alveolar. Así, las múltiples
                # realizaciones dialectales de <ll> son siempre /l/ en coda.
                if grafema.get_grafema_primario() == u'l':
                    if FONEMAS[grafema.get_fonemas_ipa()[0]].get_pda() in [PALA, POAL]:
                        # Convertimos la palatal en alveolar
                        grafema = DIGRAFOS[u'll'][-1] if isinstance(grafema, Digrafo) else MONOGRAFOS[u'l'][0]
                silabas[orden_silaba].prepend_fonema_coda(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                if organiza_grafemas:
                    silabas[orden_silaba].prepend_grafema_coda(grafema)
            elif orden_siguiente_no_mudo in indices_vocales + indices_semiconsonantes:
                # Es ataque (simple o segundo fonema de ataque complejo)
                indices_ataques.append(orden_grafema)
                orden_silaba = next(indice for indice, posicion in enumerate(indices_vocales)
                                    if posicion >= orden_grafema)
                if organiza_grafemas:
                    silabas[orden_silaba].prepend_grafema_ataque(grafema)
                if len(grafema.get_fonemas_ipa()) == 1:
                    silabas[orden_silaba].prepend_fonema_ataque(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                else:
                    if isinstance(FONEMAS[grafema.get_fonemas_ipa()[-1]], FonemaSemiconsonante):
                        # Somos la gw de huevo, maxwell, alahuita. El grafema expresa un fonema doble: ataque-semicons.
                        silabas[orden_silaba].prepend_fonema_ataque(FONEMAS[grafema.get_fonemas_ipa()[0]])
                        silabas[orden_silaba].set_fonema_semiconsonante(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                    elif orden_silaba > 0:
                        # Somos la x no inicial: doble fonema /k/ (coda) + /s/ (ataque, ya metido)
                        silabas[orden_silaba].prepend_fonema_ataque(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                        silabas[orden_silaba - 1].prepend_fonema_coda(FONEMAS[grafema.get_fonemas_ipa()[0]])
            elif orden_siguiente_no_mudo in indices_ataques:
                # Puede ser ataque complejo o coda
                # Sólo los grupos p/b/k/g/f + l/r y t/d + r son ataques complejos.
                # Podemos tener grupos consonánticos raros a principio de palabra en cultismo o extranjerismos como:
                # cn- (cnidario), gn- (gnomo, gnosis), mn- (mnemotecnia), pn- (pneuma), ps- (psiquiatra, pseudo),
                # pt- (ptolemaico), ts- (tsunami, tse-tse).
                # En general todas las consonantes antes del primer vocoide se consideran ataque, pero internamente
                # donde se acumulan las posibles combinaciones ilegales es en las codas. Así que estos ataques de
                # cultismos no se aceptan si están prefijados.
                # TODO: tema de prefijos latinos y formas tipo para-psicología o minignomo.
                # Vemos si la consonante es combinable como ataque complejo de la sílaba cuyo núcleo es el primero que
                # está en posición posterior a esta consonante.
                orden_silaba = next(indice for indice, posicion in enumerate(indices_vocales)
                                    if posicion > orden_grafema)
                grafema_siguiente = grafemas[orden_siguiente_no_mudo]
                if orden_silaba == 0 or\
                        ((FONEMAS[grafema.get_fonemas_ipa()[-1]].get_mda() == OCLU or
                          FONEMAS[grafema.get_fonemas_ipa()[-1]].get_pda() == LADE) and
                         FONEMAS[grafema_siguiente.get_fonemas_ipa()[0]].get_mda() in [VIBS, LATE] and
                            FONEMAS[grafema_siguiente.get_fonemas_ipa()[0]].get_pda() not in [PALA] and
                            (FONEMAS[grafema.get_fonemas_ipa()[-1]].get_pda() != DEAL or
                             FONEMAS[grafema_siguiente.get_fonemas_ipa()[0]].get_mda() == VIBS)):
                    # Una de dos: es la primera sílaba, o es un ataque complejo válido.
                    # Se coloca en ataque.
                    indices_ataques.append(orden_grafema)
                    silabas[orden_silaba].prepend_fonema_ataque(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                    if organiza_grafemas:
                        silabas[orden_silaba].prepend_grafema_ataque(grafema)
                elif grafema.get_fonemas_ipa()[-1][0] == grafema_siguiente.get_fonemas_ipa()[0][0]:
                    # Hay dos fonemas iguales seguidos que se podrían unir en una consonante larga. Cosas como Botta se
                    # silabean como bo-tta, y no como bot-ta, porque en cualquier caso formarán una geminada que se
                    # colocará como ataque.
                    # No obstante, si el fonema está duplicado pero el grafema no (obvio, subversivo), lo metemos
                    # como coda, separando los dos fonemas (ob-vio, sub-ver-si-vo). También se deja en coda si hay
                    # algún mudo entre la coda y el ataque
                    indices_ataques.append(orden_grafema)
                    silabas[orden_silaba].prepend_fonema_ataque(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                    if organiza_grafemas:
                        if grafema.get_grafema_txt().lower() == grafema_siguiente.get_grafema_txt().lower() and\
                                orden_siguiente_no_mudo == orden_grafema + 1:
                            silabas[orden_silaba].prepend_grafema_ataque(grafema)
                        else:
                            silabas[orden_silaba - 1].prepend_grafema_coda(grafema)
                else:
                    # No estamos en la primera silaba y no es ataque geminado ni complejo.
                    # Se coloca en coda.
                    indices_codas.append(orden_grafema)
                    if len(grafema.get_fonemas_ipa()) > 1:
                        silabas[orden_silaba - 1].prepend_fonema_coda(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                    # No se permiten laterales palatales en coda. Se cambia a la lateral alveolar. Así, las múltiples
                    # realizaciones dialectales de <ll> son siempre /l/ en coda.
                    if grafema.get_grafema_primario() == u'l':
                        if FONEMAS[grafema.get_fonemas_ipa()[0]].get_pda() in [PALA, POAL]:
                            # Convertimos la palatal en alveolar
                            grafema = DIGRAFOS[u'll'][-1] if isinstance(grafema, Digrafo) else MONOGRAFOS[u'l'][0]
                    silabas[orden_silaba - 1].prepend_fonema_coda(FONEMAS[grafema.get_fonemas_ipa()[0]])
                    if organiza_grafemas:
                        silabas[orden_silaba - 1].prepend_grafema_coda(grafema)

        # PROCESADO DE PAUSAS
        for orden_grafema in indices_pausas:
            grafema = grafemas[orden_grafema]
            if (indices_vocales and orden_grafema < orden_ultimo_grafema_alfabetico) or\
                    (not indices_vocales and
                     (grafema.get_grafema_primario() in u'¡¿({[' and not silabas[-1].get_fonema_pausa_posterior())):
                # Las pausas anteriores están, obviamente, antes del último grafema alfabético, si hay letras, y
                # mientras no hayamos considerado a algún grafema de pausa previa como pausa posterior.
                if not silabas[0].get_fonema_pausa_previa() or\
                        silabas[0].get_fonema_pausa_previa().get_fonema_ipa()[-1] != u'‖':
                    silabas[0].set_fonema_pausa_previa(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                if organiza_grafemas:
                    silabas[0].append_grafema_pausa_previa(grafema)
            else:
                # Y si no, es posterior.
                if not silabas[-1].get_fonema_pausa_posterior() or \
                        grafema.get_fonemas_ipa()[-1] == u'‖':
                    silabas[-1].set_fonema_pausa_posterior(FONEMAS[grafema.get_fonemas_ipa()[-1]])
                if organiza_grafemas:
                    silabas[-1].append_grafema_pausa_posterior(grafema)

        if organiza_grafemas and indices_mudos:
            # PROCESADO DE MUDOS
            # Solo son relevantes si queremos hacer transformaciones ortográficas de algún tipo. Si sólo queremos
            # resultados fonéticos es mejor no entrar en estas cosas, que retrasan la transcripción.
            # Se colocan con la (semi)consonante o (semi)vocal según la preferencia que se explica más adelante.
            if not indices_vocales:
                # Estamos intentando procesar alguna palabra que es una sigla. Normalmente se tendría que haber
                # expandido el lema, pero eso no es siempre necesario. Metemos todos los grafemas como pausas
                # o como ataques. Como es una situación irregular, ignoramos los fonemas y nos centramos en los
                # grafemas
                for grafema in grafemas:
                    if isinstance(grafema, GrafemaPausa):
                        if silabas[0].get_grafemas_ataque():
                            silabas[0].append_grafema_pausa_posterior(grafema)
                        else:
                            silabas[0].append_grafema_pausa_previa(grafema)
                    else:
                        silabas[0].append_grafema_ataque(grafema)
                silabas[0].set_inicio_palabra(True)
                silabas[0].set_final_palabra(True)
                return silabas

            orden_primer_no_mudo = min(indices_ataques + indices_semiconsonantes + indices_vocales)
            # Los grafemas que hemos usado hasta ahora (todos menos los mudos) están ubicados en su posición en las
            # sílabas que se han creado. Para cada posición podemos tener más de un grafema. Con lo que creamos
            # grafemas_usados que es una lista de (posiciones) listas de grafemas. Las posiciones vacías se descartan.
            # Posteriormente añadiremos los mudos en sus posiciones adecuadas, y como son copias, al modificar
            # las listas se modificarán automáticamente en su posición correspondiente dentro de la sílaba adecuada.
            grafemas_usados = []
            for silaba in silabas:
                if silaba.get_grafemas_pausa_previa():
                    grafemas_usados += [silaba.get_grafemas_pausa_previa()]
                if silaba.get_grafemas_ataque():
                    grafemas_usados += [silaba.get_grafemas_ataque()]
                if silaba.get_grafemas_semiconsonante():
                    grafemas_usados += [silaba.get_grafemas_semiconsonante()]
                if silaba.get_grafemas_vocal():
                    grafemas_usados += [silaba.get_grafemas_vocal()]
                if silaba.get_grafemas_semivocal():
                    grafemas_usados += [silaba.get_grafemas_semivocal()]
                if silaba.get_grafemas_coda():
                    grafemas_usados += [silaba.get_grafemas_coda()]
                if silaba.get_grafemas_pausa_posterior():
                    grafemas_usados += [silaba.get_grafemas_pausa_posterior()]
            for orden_grafema_mudo in indices_mudos:
                grafema_mudo = grafemas[orden_grafema_mudo]
                if orden_grafema_mudo < orden_primer_no_mudo or\
                        (((orden_grafema_mudo + 1 in indices_semiconsonantes + indices_vocales + indices_semivocales) or
                          (orden_grafema_mudo + 1 in indices_ataques and
                          grafemas[orden_grafema_mudo + 1].get_grafema_primario() == u'i')) and
                         orden_grafema_mudo - 1 not in indices_ataques):
                    # El grafema mudo está al inicio de la palabra, sigue vocoide (o una <i> consonantizada en ataque,
                    # como en <deshielo>), y además lo anterior no es ataque.
                    # El mudo se mete en la misma posición que el siguiente grafema.
                    # Se ha de buscar el grafema ya asignado que esté actualmente en la posicion del mudo
                    # (puesto que estamos recorriendo la lista de izquierda a derecha), y meter el mudo en ese
                    # mismo grupo justo antes de ese grafema.
                    unir_al_siguiente_grafema = True
                    orden_grafema_a_localizar = orden_grafema_mudo
                else:
                    # El grafema mudo no está al inicio de la palabra y además, estamos precedidos de ataque o no
                    # estamos seguidos de vocoide. En cosas como Buddha, se organiza bu-ddha, siendo la <h> parte del
                    # ataque y no de la vocal. Igualmente, en buhto, silabeamos buh-to.
                    # Se añade al anterior: a la izquierda
                    # Se ha de buscar el grafema ya asignado que esté actualmente en la posición anterior al mudo,
                    # y meterlo en ese mismo grupo justo después de ese grafema
                    unir_al_siguiente_grafema = False
                    orden_grafema_a_localizar = orden_grafema_mudo - 1
                # Sabiendo ya dónde hay que meterlo, metemos el grafema mudo donde toque dentro de grafemas_usados
                # (y por tanto, dentro de la propia estructura de la sílaba). Debemos incluirlo en la posición adecuada
                # y además dentro de la lista para esa posición, ubicarlo justo antes o después de un cierto grafema
                orden_grafema_verificandose = -1
                for orden_grupo, grafemas_en_grupo in enumerate(grafemas_usados):  # Un "grupo" es ataque, semivocal...
                    for orden_en_posicion, grafema in enumerate(grafemas_en_grupo):
                        orden_grafema_verificandose += 1
                        if orden_grafema_verificandose == orden_grafema_a_localizar:
                            # Lo hemos encontrado.
                            # Metemos el mudo en este grupo justo antes o después de este grafema
                            grafemas_usados[orden_grupo].insert(orden_en_posicion +
                                                                (0 if unir_al_siguiente_grafema else 1), grafema_mudo)
                            break
                    else:  # Si no hemos salido del for con un break, porque no lo hemos encontrado...
                        continue  # ... seguimos con el siguiente grupo
                    break  # No hemos seguido con el siguiente grupo, luego lo hemos encontrado. Acabamos

        # Puesto que es una palabra completa, marcamos las sílabas del extremo para que así conste. Esto es importante
        # para cuando realicemos el resilabeo, ya que sólo recalcularemos las sílabas en contacto entre palabras (que
        # realmente son la inmensa mayoría de las sílabas).
        silabas[0].set_inicio_palabra(True)
        silabas[-1].set_final_palabra(True)

        # ASIGNACIÓN DE TONICIDAD
        if Palabra.es_palabra_tonica(palabra_texto):
            # Asignamos la tonicidad. Primero nos basamos en las vocales con tilde.
            adverbio_mente = (len(silabas) > 2 and
                              silabas[-2].transcribe_fonologicamente_silaba(False, False, False, False) +
                              silabas[-1].transcribe_fonologicamente_silaba(False, False, False, False) == u'mente')
            hay_tilde = False
            hay_tilde_secundaria = False
            # Recorremos las sílabas desde la última a la primera
            for orden_inverso_silaba, silaba in enumerate(silabas[::-1]):
                if silaba.get_tonica():  # Si ya habíamos marcado la sílaba como tónica, es porque había tilde o -mente
                    if not hay_tilde:  # Si no habíamos encontrado tilde...
                        hay_tilde = True  # ... ahora ya sí.
                        if adverbio_mente and orden_inverso_silaba > 2:
                            hay_tilde_secundaria = True
                            silaba.set_tonica(ACSC)
                    else:  # Es un adverbio en -mente, o había más de una vocal con tilde
                        # Los consideramos como acentos secundarios (solo la última sílaba tónica tiene primario)
                        silaba.set_tonica(ACSC)
            # Si no había vocales con tilde, seguimos las reglas de ortografía.
            if not hay_tilde or (adverbio_mente and not hay_tilde_secundaria):
                if adverbio_mente:
                    orden_ultimo_grafema_alfabetico -= 5
                if (len(silabas) > (3 if adverbio_mente else 1)) and\
                        grafemas[orden_ultimo_grafema_alfabetico].get_grafema_primario().lower() in u'ieaouns':
                    # Polisílaba sin tildes acabada en vocal o n/s: Llana
                    silabas[-4 if adverbio_mente else -2].set_tonica(ACSC if adverbio_mente else ACPR)
                else:
                    # Monosílabo o polisílaba sin tildes no acabada en vocal o n/s: Aguda
                    silabas[-3 if adverbio_mente else -1].set_tonica(ACSC if adverbio_mente else ACPR)
            if adverbio_mente:
                silabas[-2].set_tonica(ACPR)

        # ADICIÓN DE E EPENTÉTICA
        # Metemos una "e" epentética en caso de que tengamos una "s" seguida de consonante al inicio de la palabra.
        # Esto significa que la "s" pasa de ataque a coda de una sílaba extra previa.
        # Sólo se mete en la transcripción fonética (más adelante se insertará el alófono), y no en la ortográfica
        if inserta_epentesis and len(silabas[0].get_fonemas_ataque()) > 1\
                and silabas[0].get_fonemas_ataque()[0].get_fonema_ipa() == u's':
            silaba_epentetica = Silaba()
            silaba_epentetica.set_fonema_vocal(FONEMAS[u'e'])
            silabas[0].set_fonemas_ataque(silabas[0].get_fonemas_ataque()[1:])
            silaba_epentetica.append_fonema_coda(FONEMAS[u's'])
            silabas[0].set_inicio_palabra(False)
            silabas = [silaba_epentetica] + silabas
            silabas[0].set_inicio_palabra(True)
        return silabas

    def calcula_alofonos(self):
        u"""Calcula los alófonos con los que se expresan los fonemas de la Palabra (y crea su estructura interna)

        Este método es de los más importantes de la clase: una vez la palabra está silabeada, con este método se
        calculan los alófonos con que se expresan los fonemas, según su posición en la sílaba y los fonemas del entorno.
        También se vuelve a utilizar tras hacer el resilabeo. Es importante este doble uso, ya que cabe la posibilidad
        de que los alófonos que expresen dos sílabas en contacto cambien si ambas sílabas son parte de la misma palabra
        o si no.

        Para cada fonema, se extrae la lista de posibles alófonos. Cada alófono contiene unas reglas que indican
        cuándo es un alófono válido o no; además de tener un método que, basándose en dichas reglas, evalúa si
        el fonema es compatible o no con su entorno fonético. Gracias a ello, en este método simplemente tenemos que
        ir procesando los fonemas, para cada uno sacar la lista de alófonos posibles según su ubicacion en la sílaba,
        y desambiguar quedándonos únicamente con el alófono (o alófonos) que representen a cada fonema.

        :return: None
        """
        # La clase Juntura es una subclase de Palabra y hereda sus métodos. Se usa para hacer el resilabeado de la
        # Frase, y por tanto cambia fonemas de unas sílabas a otras, pudiendo incluso dejar alguna sílaba vacía.
        # Esto es importante saberlo, porque se actúa de forma ligeramente distinta que si se está alofonizando
        # una palabra aislada.
        resilabeando = isinstance(self, Juntura)
        # Procesamos las sílabas de la última a la primera. En caso de que estemos llamando a este método porque
        # hayamos resilabeado una frase y se deba recalcular los alófonos, sólo recalcularemos la sílaba intermedia
        # de las tres de las que consta la Juntura, que es la sílaba de interés (las otras dos son su entorno previo
        # y posterior) y está en segunda posición.
        for orden_silaba in (range(len(self._silabas) - 1, -1, -1) if not resilabeando else [1]):
            # Para calcular los alófonos de esta sílaba, necesitamos un entorno consistente en la sílaba anterior y la
            # siguiente a la sílaba cuya realización alofónica estamos procesando. Si estamos en el extremos, metemos
            # una sílaba vacía.
            silaba_anterior = self._silabas[orden_silaba - 1] if orden_silaba > 0 else Silaba()
            silaba_actual = self._silabas[orden_silaba]
            silaba_siguiente = self._silabas[orden_silaba + 1] if orden_silaba < len(self._silabas) - 1 else Silaba()
            # El entorno es de tipo [Fonema]
            entorno = silaba_anterior.get_fonemas() + silaba_actual.get_fonemas() + silaba_siguiente.get_fonemas()

            # PAUSA POSTERIOR
            silaba_actual.reset_alofono_pausa_posterior()
            if silaba_actual.get_fonema_pausa_posterior():
                silaba_actual.set_alofono_pausa_posterior(
                    ALOFONOS_PAUSA[silaba_actual.get_fonema_pausa_posterior().get_fonema_ipa()][0])

            # CODA
            if not resilabeando or silaba_siguiente.get_fonemas():
                # Procesamos la coda únicamente si no estamos resilabeando o si verdaderamente hay algo después
                silaba_actual.reset_alofonos_coda()
                if silaba_actual.get_fonemas_coda():
                    # Extraemos el/los fonema(s) de coda y extraemos todas sus realizaciones alofónicas
                    posicion_final = len(entorno) - len(silaba_siguiente.get_fonemas()) - 1
                    posicion_inicial = posicion_final - len(silaba_actual.get_fonemas_coda())
                    for posicion_en_entorno in range(posicion_final, posicion_inicial, - 1):
                        posibles_alofonos = ALOFONOS_CODA[entorno[posicion_en_entorno].get_fonema_ipa()]
                        if len(posibles_alofonos) == 1:
                            # Es un fonema que solo tiene una realización alofónica en coda, así que no buscamos más.
                            silaba_actual.prepend_alofono_coda(posibles_alofonos[0])
                            continue
                        # Hay más de una opción, toca desambiguar
                        for posible_alofono in posibles_alofonos:
                            # Probamos si cumple las restricciones para ser el alófono que va en este entorno
                            if posible_alofono.es_alofono_compatible(entorno, posicion_en_entorno):
                                silaba_actual.prepend_alofono_coda(posible_alofono)
                                break

            # Vamos a procesar el núcleo, para lo que nos es necesario saber si dicho núcleo está rodeado de nasales,
            # en cuyo caso los alófonos del núcleo serán los nasalizados. Lo será si el ataque es nasal y la coda
            # también, y en caso de no tener coda, también vale con que el ataque siguiente sea nasal.
            entorno_nasal = (silaba_actual.get_fonemas_ataque() and
                             silaba_actual.get_fonemas_ataque()[0].get_mda() == NASA) and\
                            ((silaba_actual.get_fonemas_coda() and
                              silaba_actual.get_fonemas_coda()[0].get_mda() == NASA) or
                             (not silaba_actual.get_fonemas_coda() and silaba_siguiente.get_fonemas_ataque() and
                              silaba_siguiente.get_fonemas_ataque()[0].get_mda() == NASA))

            # NÚCLEO: SEMIVOCAL
            # Seguimos un mismo patrón con semivocales, vocales y semiconsonantes
            silaba_actual.reset_alofono_semivocal()
            if silaba_actual.get_fonema_semivocal():
                posicion_en_entorno = len(entorno) - len(silaba_siguiente.get_fonemas()) -\
                    len(silaba_actual.get_fonemas_coda()) - 1
                # Escogemos los alófonos nasales u orales según corresponda
                if entorno_nasal:
                    posibles_alofonos = ALOFONOS_NUCLEO_NASALES[entorno[posicion_en_entorno].get_fonema_ipa()]
                else:
                    posibles_alofonos = ALOFONOS_NUCLEO_ORALES[entorno[posicion_en_entorno].get_fonema_ipa()]
                if len(posibles_alofonos) == 1:
                    # Solo hay una opción, así que nada que pensar.
                    silaba_actual.set_alofono_semivocal(posibles_alofonos[0])
                else:
                    # Miramos las opciones posibles y nos quedamos con la compatible
                    for posible_alofono in posibles_alofonos:
                        if posible_alofono.es_alofono_compatible(entorno, posicion_en_entorno):
                            silaba_actual.set_alofono_semivocal(posible_alofono)
                            break

            # NÚCLEO: VOCAL
            silaba_actual.reset_alofono_vocal()
            # Aunque es un caso raro, puede haber cosas como "No, ¿?", donde "¿?" forma una sílaba, con apertura y
            # cierre. Estas sílabas atípicas (necesarias para la transcripción ortográfica) no tienen núcleo.
            if silaba_actual.get_fonema_vocal():
                posicion_en_entorno = len(silaba_anterior.get_fonemas() + silaba_actual.get_fonemas_ataque()) +\
                    (1 if silaba_actual.get_fonema_semiconsonante() else 0)
                if entorno_nasal:
                    posibles_alofonos = ALOFONOS_NUCLEO_NASALES[entorno[posicion_en_entorno].get_fonema_ipa()]
                else:
                    posibles_alofonos = ALOFONOS_NUCLEO_ORALES[entorno[posicion_en_entorno].get_fonema_ipa()]
                if len(posibles_alofonos) == 1:
                    silaba_actual.set_alofono_vocal(posibles_alofonos[0])
                else:
                    for posible_alofono in posibles_alofonos:
                        if posible_alofono.es_alofono_compatible(entorno, posicion_en_entorno):
                            silaba_actual.set_alofono_vocal(posible_alofono)
                            break

            # NÚCLEO: SEMICONSONANTE
            silaba_actual.reset_alofono_semiconsonante()
            if silaba_actual.get_fonema_semiconsonante():
                posicion_en_entorno = len(silaba_anterior.get_fonemas() + silaba_actual.get_fonemas_ataque())
                if entorno_nasal:
                    posibles_alofonos = ALOFONOS_NUCLEO_NASALES[entorno[posicion_en_entorno].get_fonema_ipa()]
                else:
                    posibles_alofonos = ALOFONOS_NUCLEO_ORALES[entorno[posicion_en_entorno].get_fonema_ipa()]
                if len(posibles_alofonos) == 1:
                    silaba_actual.set_alofono_semiconsonante(posibles_alofonos[0])
                else:
                    for posible_alofono in posibles_alofonos:
                        if posible_alofono.es_alofono_compatible(entorno, posicion_en_entorno):
                            silaba_actual.set_alofono_semiconsonante(posible_alofono)
                            break

            # ATAQUE
            # El ataque es más delicado de procesar. Debido a que este método se usa para hacer el cálculo de alófonos
            # inicial, pero también en el resilabeo (al realizar cambios fonéticos se recalculan los alófonos de las
            # sílabas en contacto entre dos palabras), no siempre se comporta igual. Existen algunos alófonos de coda
            # que no aparecen nunca entre medias de palabra, sólo a final, y esos alófonos deben en ocasiones mantenerse
            # tras el resilabeo (y por lo tanto se utiliza un alófono "anómalo"). Por ejemplo, si tenemos <boj alto>
            # nos queda [ˈbɔ.ˈx̥ɑl̪.t̪o] y no [ˈbɔ.ˈxɑl̪.t̪o], aunque [x̥] no pueda aparecer en principio en ataque.
            # En la práctica, si nos ha llegado a esta sílaba un alófono de ataque enmudecido (propio de la coda
            # únicamente) porque se haya pasado de una palabra anterior, dejamos los alófonos que ya tuviera la sílaba.
            if not silaba_actual.get_alofonos_ataque() or\
                    u'̥' not in silaba_actual.get_alofonos_ataque()[0].get_alofono_ipa():
                silaba_actual.reset_alofonos_ataque()
                if silaba_actual.get_fonemas_ataque():
                    posicion_inicial = len(silaba_anterior.get_fonemas()) - 1
                    posicion_final = posicion_inicial + len(silaba_actual.get_fonemas_ataque())
                    for posicion_en_entorno in range(posicion_final, posicion_inicial, - 1):
                        posibles_alofonos = ALOFONOS_ATAQUE[entorno[posicion_en_entorno].get_fonema_ipa()]
                        if len(posibles_alofonos) == 1:
                            silaba_actual.prepend_alofono_ataque(posibles_alofonos[0])
                            continue
                        for posible_alofono in posibles_alofonos:
                            if posible_alofono.es_alofono_compatible(entorno, posicion_en_entorno):
                                silaba_actual.prepend_alofono_ataque(posible_alofono)
                                break

            # PAUSA PREVIA
            silaba_actual.reset_alofono_pausa_previa()
            if silaba_actual.get_fonema_pausa_previa():
                silaba_actual.set_alofono_pausa_previa(
                    ALOFONOS_PAUSA[silaba_actual.get_fonema_pausa_previa().get_fonema_ipa()][0])

    def transcribe_ortograficamente_palabra(self, marca_tonica=False, incluye_pausas=False,
                                            separador=u'-', apertura=u'<', cierre=u'>'):
        u"""Se devuelve la transcripción ortográfica de la palabra, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True, se incluye en la transcripción las pausas que toda palabra aislada
            tiene (al inicio y) al final por el hecho de estar aislada.
        :type separador: unicode
        :param separador: Un string que se coloca entre sílabas
        :type apertura: unicode
        :param apertura: Un string que se coloca al inicio
        :type cierre: unicode
        :param cierre: Un string que se coloca al final
        :rtype: unicode
        :return: La transcripción ortográfica de la palabra, según los parámetros
        """
        transcripcion_palabra = u''
        for orden_silaba, silaba in enumerate(self._silabas):
            transcripcion_silaba = silaba.transcribe_ortograficamente_silaba(marca_tonica, incluye_pausas)
            if transcripcion_silaba:  # Puede haber sílabas vacías aunque no debería si se resilabea sobre copia
                transcripcion_palabra += (separador if transcripcion_palabra else u'') + transcripcion_silaba
        return apertura + transcripcion_palabra + cierre

    def transcribe_fonologicamente_palabra(self, marca_tonica=True, incluye_pausa_previa=False,
                                           incluye_pausa_posterior=False, transcribe_fonemas_aparentes=False,
                                           separador=u'.', apertura=u'/', cierre=u'/'):
        u"""Se devuelve la transcripción fonológica de la palabra, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type incluye_pausa_previa: bool
        :param incluye_pausa_previa: Si está a True, se incluye en la transcripción las pausas que toda palabra aislada
            tiene al inicio por el hecho de estar aislada. Si estamos transcribiendo una frase, nos interesa ponerlo a
            False para que no las incluya.
        :type incluye_pausa_posterior: bool
        :param incluye_pausa_posterior: Si está a True, se incluye en la transcripción las pausas que toda palabra
            tiene al final por el hecho de estar aislada. Si estamos transcribiendo una frase, nos interesa ponerlo a
            False para que no las incluya.
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
        :return: La transcripción fonológica (fonemas) de la palabra, según los parámetros
        """
        transcripcion_palabra = u''
        for orden_silaba, silaba in enumerate(self._silabas):
            transcripcion_silaba = silaba.transcribe_fonologicamente_silaba(
                marca_tonica,
                orden_silaba > 0 or incluye_pausa_previa,
                orden_silaba < len(self._silabas) - 1 or incluye_pausa_posterior,
                transcribe_fonemas_aparentes)
            if transcripcion_silaba:  # Puede haber sílabas vacías
                transcripcion_palabra += (separador if transcripcion_palabra else u'') + transcripcion_silaba
        return apertura + transcripcion_palabra + cierre

    def transcribe_foneticamente_palabra(self, marca_tonica=True, incluye_pausa_previa=False,
                                         incluye_pausa_posterior=False, ancha=False,
                                         separador=u'.', apertura=u'[', cierre=u']'):
        u"""Se devuelve la transcripción fonética de la palabra, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type incluye_pausa_previa: bool
        :param incluye_pausa_previa: Si está a True, se incluye en la transcripción las pausas que toda palabra aislada
            tiene al inicio por el hecho de estar aislada. Si estamos transcribiendo una frase, nos interesa ponerlo a
            False para que no las incluya.
        :type incluye_pausa_previa: bool
        :param incluye_pausa_previa: Si está a True, se incluye en la transcripción las pausas que toda palabra aislada
            tiene al inicio por el hecho de estar aislada. Si estamos transcribiendo una frase, nos interesa ponerlo a
            False para que no las incluya.
        :type incluye_pausa_posterior: bool
        :param incluye_pausa_posterior: Si está a True, se incluye en la transcripción las pausas que toda palabra
            aislada tiene al final por el hecho de estar aislada. Si estamos transcribiendo una frase, nos interesa
            ponerlo a False para que no las incluya.
        :type separador: unicode
        :param separador: Un string que se coloca entre sílabas
        :type apertura: unicode
        :param apertura: Un string que se coloca al inicio
        :type cierre: unicode
        :param cierre: Un string que se coloca al final
        :type ancha: bool
        :param ancha: Si está a True se devuelve la transcripción ancha. Está a False se devuelve la transcripción
            estrecha (por defecto).
        :rtype: unicode
        :return: el string con la transcripción fonética (alófonos) de la palabra, según los parámetros
        """
        transcripcion_palabra = u''
        for orden_silaba, silaba in enumerate(self._silabas):
            transcripcion_silaba = silaba.\
                transcribe_foneticamente_silaba(marca_tonica,
                                                orden_silaba > 0 or incluye_pausa_previa,
                                                orden_silaba < len(self._silabas) - 1 or incluye_pausa_posterior,
                                                ancha)
            if transcripcion_silaba:  # Puede haber sílabas vacías
                transcripcion_palabra += (separador if transcripcion_palabra else u'') + transcripcion_silaba
        return apertura + transcripcion_palabra + cierre

    def elimina_silaba(self, orden_silaba=-1):
        u"""Se elimina la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la vocal.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        orden_silaba = (orden_silaba + len(self._silabas)) % len(self._silabas)
        self._silabas = self._silabas[:orden_silaba] + self._silabas[orden_silaba + 1:]
        return self

    def reset_pausa_previa(self, orden_silaba=0):
        u"""Se elimina la pausa previa de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la pausa previa.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_pausa_previa()
        return self

    def set_pausa_previa(self, orden_silaba=0):
        u"""Se elimina la pausa previa de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la pausa previa.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_pausa_previa()
        return self

    def reset_ataque(self, orden_silaba=0):
        u"""Se elimina el ataque de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear el ataque.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_ataque()
        return self

    def reset_semiconsonante(self, orden_silaba=0):
        u"""Se elimina la semiconsonante de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la semiconsonante.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_semiconsonante()
        return self

    def reset_vocal(self, orden_silaba=0):
        u"""Se elimina la vocal de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la vocal.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_vocal()
        return self

    def reset_semivocal(self, orden_silaba=-1):
        u"""Se elimina la semivocal de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la semivocal.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_semivocal()
        return self

    def reset_coda(self, orden_silaba=-1):
        u"""Se elimina la coda de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la coda.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_coda()
        return self

    def reset_pausa_posterior(self, orden_silaba=-1):
        u"""Se elimina la pausa posterior de la sílaba indicada por el parámetro

        :type orden_silaba: int
        :param orden_silaba: El orden de la sílaba a la que vamos a resetear la pausa posterior.
                             Puede ser un valor negativo para contar la posición desde el final.
        :rtype: Palabra
        :return: Se devuelve la propia palabra tras haber hecho la modificación.
        """
        if (0 <= orden_silaba < len(self._silabas)) or (orden_silaba < 0 < abs(orden_silaba) <= len(self._silabas)):
            self._silabas[orden_silaba].reset_pausa_posterior()
        return self

    def sigue_fonotactica(self, restringe_coda_final=False):
        u"""Indica si la palabra silabeada sigue la fonotáctica española

        Los problemas están en la combinación de consonantes en ataque o en coda. Nos aseguramos
        de que no haya combinaciones atípicas al español en estas posiciones.

        :rtype: bool
        :return: True si la palabra sigue la fonotáctica española, False si no.
        """
        if not self._silabas:
            return False
        for orden_silaba, silaba in enumerate(self._silabas):
            if orden_silaba == 0:
                # En el ataque sólo hay problemas al inicio de palabra. Si no, esas aglomeraciones
                # de consonantes pasan siempre a la coda
                ataque = silaba.get_fonemas_ataque(incluye_pausas=False)
                if len(ataque) > 1:
                    # En ataque complejo sólo se acepta oclusiva o f + líquida (excepto d/t + l)
                    # Se aceptan los fonemas largos, y de ahí que dejemos pasar la vibrante múltiple
                    # OJO: el carácter del grafema g es distinto del del alófono ɡ (aunque parezca el mismo aquí)
                    if ataque[0].get_fonema_ipa()[0] not in [u'b', u'p', u'd', u't', u'ɡ', u'k', u'f'] or\
                            ataque[1].get_fonema_ipa()[0] not in [u'l', u'ɾ', u'r']:  # Consideramos r = ɾː
                        # No es una combinación válida
                        return False
                    if ataque[0].get_fonema_ipa()[0] in [u'd', u't'] and ataque[1].get_fonema_ipa()[0] in [u'l']:
                        # Casi, pero no. "Atlántico" lo silabeamos como at-lán-ti-co, como ad-lá-te-res
                        return False
            coda = silaba.get_fonemas_coda(incluye_pausas=False)
            if coda and len(coda) > 1:
                if restringe_coda_final and (orden_silaba == len(self._silabas) - 1):
                    # Técnicamente, en coda final sólo se permiten fonemas alveolares: /nslɾr/.
                    # Tenemos un poco de manga ancha
                    if coda[0].get_fonema_ipa()[0] not in [u'ɾ', u'r', u'm', u'n', u'l', u'b', u'd', u'k'] or \
                            coda[1].get_fonema_ipa()[0] not in [u's']:  # Consideramos r = ɾː
                        # No es una combinación válida
                        return False
                else:
                    # En coda compleja sólo se acepta /lɾrmnbdgptk/ + /s/, o /n/ + /θ/.
                    # La verdad es que /ls/ y /ms/ no son validas en puridad, pero hay cosas como "Ámsterdam" o "vals".
                    # Las oclusivas + /s/ se permiten por la existencia de los grupos /ds/, /bs/ y /gs/ (adscrito,
                    # abstracto, examen), y porque las oclusivas sordas en coda se sonorizan. No son combinaciones del
                    # todo legales, pero ciertamente son pronunciables.
                    # OJO: el carácter del grafema g es distinto del del alófono ɡ (aunque parezca el mismo aquí)
                    if coda[0].get_fonema_ipa()[0] not in [u'ɾ', u'r', u'm', u'n', u'l',
                                                           u'b', u'd', u'ɡ', u'p', u't', u'k'] or \
                            coda[1].get_fonema_ipa()[0] not in [u's', u'θ']:  # Consideramos r = ɾː
                        # No es una combinación válida
                        return False
                    if coda[1].get_fonema_ipa()[0] in [u'θ'] and coda[0].get_fonema_ipa()[0] not in [u'm', u'n']:
                        # Casi, pero no. Se acepta "Sanz", pero "perz" pues no.
                        return False
        # Si hemos llegado hasta aquí, todas las sílabas cumplían la fonotáctica
        return True

    @staticmethod
    def convierte_a_palabras_legibles(palabra_texto, palabra_texto_previa=u'', palabra_texto_siguiente=u''):
        """Devuelve la palabra legible (expansión ortográfica) de la palabra indicada.

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres que queremos convertir a palabras legibles
        :type palabra_texto_previa: unicode
        :param palabra_texto_previa: la palabra anterior
        :type palabra_texto_siguiente: unicode
        :param palabra_texto_siguiente: la palabra siguiente
        :rtype: unicode
        :return: La cadena de caracteres con las palabras legibles que se han creado para esta palabra. Puede
            coincidir con la palabra de entrada (si esta ya era legible) o puede constar de una o varias palabras
            separadas por espacios.
        """
        # El español es un idioma con una ortografía eminentemente fonética. Sin embargo existen algunos
        # poquísimos digamos "anacronismos" ortográficos, como el uso del grafema <x> con valor fonético de
        # /x/ en las palabras "México" y "Texas" y sus derivados. Ponemos la <j> e lugar de la <x> y se
        # soluciona el problema.
        # OJO: Esto afecta a la transcripción ortográfica. Si entra "México" devolverá "Méjico", y no es igual
        if u'méxic' in palabra_texto.lower() or u'mexic' in palabra_texto.lower() or\
                u'texas' in palabra_texto.lower() or u'texan' in palabra_texto.lower():
            palabra_texto = palabra_texto.lower().replace(u'xic', u'jic').replace(u'texa', u'teja')
        puntuacion_anterior, palabra_texto_sin_puntuacion, puntuacion_posterior = Palabra.\
            extrae_puntuacion(palabra_texto)
        if not palabra_texto_sin_puntuacion:
            # Solo es puntuación. Algo raro, solo puede ocurrir en frases vacías
            return palabra_texto
        if palabra_texto_sin_puntuacion[-1] in MONOGRAFOS \
                and isinstance(MONOGRAFOS[palabra_texto_sin_puntuacion[-1]][0], MonografoOrdinal):
            # Aparece un símbolo que indica que se trata de un número ordinal. Lo usaremos más adelante
            grafema_ordinal = MONOGRAFOS[palabra_texto_sin_puntuacion[-1]][0]
        else:
            grafema_ordinal = None

        # Verificamos si la palabra incluye dígitos
        if Palabra.contiene_numeros(palabra_texto_sin_puntuacion):
            # La palabra contiene números. Veremos qué tipo de palabra tenemos, porque puede ser unicamente
            # una cifra, incluyendo o no la marca de negativo, separadores de miles o coma decimal; o bien
            # puede ser un ordinal, o un porcentaje/grado... Vamos verificando y según lo que encontremos,
            # actuamos.
            if grafema_ordinal:
                # Tenemos un grafema ordinal al final (º, ª...). Comprobamos si el número previo es correcto.
                if Palabra.es_numero(palabra_texto_sin_puntuacion[:-1]) and palabra_texto_sin_puntuacion[0] != u'0':
                    # Tenemos un número (grupo de dígitos).
                    # Parece un ordinal correcto, pero puede ser un decimal, o un número negativo
                    if u',' not in palabra_texto_sin_puntuacion and palabra_texto_sin_puntuacion[0] != u'-'\
                            and (not palabra_texto_siguiente or palabra_texto_siguiente[0] != u'C' or
                                 palabra_texto_siguiente[1:].lower() != palabra_texto_siguiente[1:].upper()):
                        # Lo tomamos como ordinal. Eliminamos los puntos de separación de miles ("en 1.000ª
                        # posición")
                        numero_texto = palabra_texto_sin_puntuacion.replace(u'.', u'')
                        palabra_ordinal = num2words(int(numero_texto[:-1]), ordinal=True, lang="es")
                        # Ajustamos el género (por defecto es masculino) según el grafema ordinal usado.
                        palabra_ordinal = palabra_ordinal[:-1] +\
                            (palabra_ordinal[-1].replace(u'o', u'a')
                             if grafema_ordinal.get_genero() != MASC else palabra_ordinal[-1])
                        palabra_texto = puntuacion_anterior + palabra_ordinal + puntuacion_posterior
                        return palabra_texto
                    elif grafema_ordinal.get_genero() != MASC:
                        # Nos entra un número aparentemente decimal, pero con marca de ordinal, que además es
                        # femenino.
                        # Algo raro como 10,8ª que no es legal, así que deletreamos.
                        return puntuacion_anterior +\
                            Palabra.deletrea(palabra_texto_sin_puntuacion, agrupa_numeros=True) + puntuacion_posterior
                    else:
                        # Lo tomamos como grados (23,8º).
                        # Se quita la marca y se procesa como número decimal (más adelante)
                        palabra_texto_sin_puntuacion = palabra_texto_sin_puntuacion[:-1]
                else:
                    # Bien lo previo al grafema ordinal no es un número, bien hay ceros a la izquierda.
                    # Deletreamos.
                    return puntuacion_anterior + Palabra.deletrea(palabra_texto_sin_puntuacion, agrupa_numeros=True) + \
                        puntuacion_posterior
            # Si no hemos salido, es que tenemos un número cardinal (quizá decimal, quizá negativo,
            # o incluso con marca de porcentaje, grado...); o quizá sea una fecha, hora...
            porcentaje = palabra_texto_sin_puntuacion[-1] == u'%'
            if porcentaje:
                # De momento quitamos la marca de porcentaje y después añadiremos el "por ciento"
                palabra_texto_sin_puntuacion = palabra_texto_sin_puntuacion[:-1]
            if Palabra.es_numero(palabra_texto_sin_puntuacion):
                # No es hora, ni fecha ni nada. Es número, número.
                # No obstante, si es decimal, tendremos que pronunciar "dos números": diez coma doce.
                if u',' in palabra_texto_sin_puntuacion:
                    # Decimal. Quitamos los puntos pero reemplazamos la coma por punto (nuestra marca de
                    # separación).
                    numero_texto = palabra_texto_sin_puntuacion.replace(u'.', u'').replace(u',', u'.')
                else:
                    # No es decimal. Quitamos los puntos porque es todo un mismo número
                    numero_texto = palabra_texto_sin_puntuacion.replace(u'.', u'')
                numero_partido = numero_texto.split(u'.')  # Si hay punto es porque es decimal
                palabra_texto = puntuacion_anterior + num2words(float(numero_partido[0]), False, "es")
                if len(numero_partido) == 2:  # Efectivamente, es decimal
                    if len(numero_partido[1]) > 3 or numero_partido[1][0] == u'0':
                        # La parte decima empieza por 0: 12,017; o es muy larga (más de 3 dígitos): 7,5278
                        # Se prefiere deletrear la parte decimal
                        palabra_texto += u' coma ' + Palabra.deletrea(numero_partido[1], agrupa_numeros=False)
                    else:
                        # Es una parte decimal que se puede expresar bien como cifra
                        palabra_texto += u' coma ' + num2words(float(numero_partido[1]), False, "es")
                palabra_texto = palabra_texto.replace(u'dieciseis', u'dieciséis')  # num2words falla
                palabra_texto += (u' por ciento' if porcentaje else u'') +\
                                 (u' grados' if grafema_ordinal else u'') + puntuacion_posterior
                return palabra_texto
            elif not re.findall(u'[^0-9.:\-/\\\]', palabra_texto_sin_puntuacion):
                # La palabra no es un número "plano", sino que incluye otros caracteres que indican que es
                # posiblemente una fecha o una hora.
                try:
                    # Intentamos parsear la fecha/hora con el dateutil.parse
                    fecha = parse(palabra_texto_sin_puntuacion, dayfirst=True)
                except (ValueError, OverflowError):
                    # No ha sido capaz y ha petado. No es una fecha.
                    fecha = None
                if fecha:
                    # Es una fecha u hora.
                    if u':' in palabra_texto_sin_puntuacion and \
                            not re.findall(u'[^0-9.:]', palabra_texto_sin_puntuacion):
                        # Hay un ":" y los demás caracteres son compatibles con una hora. Puede ser del
                        # tipo 22:43:17
                        # No admitimos decimales (se admiten decimales solo con "," y no con punto).
                        numero_texto = palabra_texto_sin_puntuacion.replace(u'.', u':')  # ":"es nuestra marca
                        numero_partido = [int(num) for num in numero_texto.split(u':')]
                        # El problema es que podemos tener o no los segundos. Los minutos deben tener dos
                        # dígitos.
                        if len(numero_texto.split(u':')[1]) > 1 and\
                                ((len(numero_partido) == 2 and numero_partido[0] < 24 and numero_partido[1] < 60) or
                                 (len(numero_partido) == 3 and numero_partido[0] < 24 and numero_partido[1] < 60 and
                                 numero_partido[2] < 60)):
                            # Parece una hora válida. En caso de tener dos números, el primero podría ser
                            # hora o minuto.
                            if len(numero_partido) == 3 or numero_partido[0] < 24:
                                # Si el primero puede ser hora, lo tomamos como hora antes que como minuto
                                hora = (int(numero_partido[0]) % 12)\
                                    if (int(numero_partido[0]) % 12) > 0 else 12
                                hora_siguiente = hora + 1 if hora < 12 else 1
                                palabra_texto = puntuacion_anterior +\
                                    num2words(hora
                                              if numero_partido[1] < 31 else hora_siguiente, False, "es").\
                                    replace(u'uno', u'una')  # La hora es femenina
                                # Nos hemos comido la hora, dejamos los minutos al inicio.
                                numero_partido = numero_partido[1:]
                            if int(numero_partido[0]) == 0:
                                palabra_texto += u' en punto'
                            elif int(numero_partido[0]) == 15:
                                palabra_texto += u' y cuarto'
                            elif int(numero_partido[0]) < 30:
                                palabra_texto += u' y ' + num2words(int(numero_partido[0]), False, "es")
                            elif int(numero_partido[0]) == 30:
                                palabra_texto += u' y media'
                            elif int(numero_partido[0]) == 45:
                                palabra_texto += u' menos cuarto'
                            elif int(numero_partido[0]) < 60:
                                # No hace falta poner el "menos", sale del signo de la resta.
                                palabra_texto += u' ' + num2words(int(numero_partido[0]) - 60, False, "es")
                            if len(numero_partido) == 2:
                                # Hay segundos
                                palabra_texto += u' y ' + num2words(int(numero_partido[1]), False, "es") +\
                                                 u' segundos'
                            palabra_texto = palabra_texto.replace(u'dieciseis', u'dieciséis')  # num2words mal
                            palabra_texto += puntuacion_posterior
                            return palabra_texto
                    elif not re.findall(u'[^0-9\-/\\\]', palabra_texto_sin_puntuacion):
                        # Por los caracteres que contiene la palabra, parece ser una fecha.
                        # Ecualizamos el divisor de días/meses/años y lo ponemos como /
                        numero_texto = palabra_texto_sin_puntuacion.replace(u'.', u'/').replace(u'\\', u'/')
                        numero_partido = [int(num) for num in numero_texto.split(u'/')]
                        # El problema es que podemos tener o no el día (10/2010) o el año (27/07).
                        if (len(numero_partido) == 2 and ((numero_partido[0] < 32 and numero_partido[1] < 13) or
                                                          (numero_partido[0] < 13))) or\
                                (len(numero_partido) == 3 and numero_partido[0] < 32 and numero_partido[1] < 13):
                            # Parece una fecha válida. En caso de tener dos números, el primero podría ser
                            # día o mes.
                            if len(numero_partido) == 3 or (numero_partido[0] < 32 and numero_partido[1] < 13):
                                # Si el primero puede ser día, lo tomamos como día antes que como mes
                                palabra_texto = puntuacion_anterior + num2words(fecha.day, False, "es") +\
                                                u' de '
                                # Nos hemos comido el día, dejamos el mes al inicio.
                                numero_partido = numero_partido[1:]
                            # En una fecha, el mes siempre aparece
                            palabra_texto += MESES[fecha.month - 1]
                            if len(numero_partido) > 1:
                                palabra_texto += u' de ' + num2words(fecha.year, False, "es")
                            palabra_texto = palabra_texto.replace(u'dieciseis', u'dieciséis')  # num2words mal
                            palabra_texto += puntuacion_posterior
                            return palabra_texto

            # Hay mezcla de caracteres y números. Deletreamos
            palabra_texto = Palabra.deletrea(palabra_texto_sin_puntuacion, agrupa_numeros=True)
            return palabra_texto
        elif grafema_ordinal:  # º, ª... también aparecen en abreviaturas (ahora no hay números)
            if grafema_ordinal.get_genero() == MASC:
                if palabra_texto_sin_puntuacion[:-1].lower() == u'n':
                    palabra_texto = puntuacion_anterior + u'número' + puntuacion_posterior
            elif palabra_texto_sin_puntuacion[:-1].lower() == u'm':
                palabra_texto = puntuacion_anterior + u'María' + puntuacion_posterior
            return palabra_texto
        elif Palabra.contiene_mayusculas(palabra_texto_sin_puntuacion) and\
                (not Palabra.contiene_minusculas(palabra_texto_sin_puntuacion) or
                 (not Palabra.contiene_minusculas(palabra_texto_sin_puntuacion[:-1]) and
                 palabra_texto_sin_puntuacion[-1] == u's')):
            # Podría ser un número romano o un acrónimo. Hacemos una comprobación simple
            if (not re.findall(u'[^IVXLCDM]', palabra_texto_sin_puntuacion) and
                    ((u'ii' in palabra_texto_sin_puntuacion.lower() or
                      u'xx' in palabra_texto_sin_puntuacion.lower() or
                      u'mm' in palabra_texto_sin_puntuacion.lower()) or
                     ((palabra_texto_previa == u'' or
                       (not Palabra.contiene_mayusculas(palabra_texto_previa) or
                        Palabra.contiene_minusculas(palabra_texto_previa))) and
                      (palabra_texto_siguiente == u'' or
                       (not Palabra.contiene_mayusculas(palabra_texto_siguiente) or
                        Palabra.contiene_minusculas(palabra_texto_siguiente)))))):
                # Lo consideramos número romano. Salvo que sean ºC.
                if palabra_texto_sin_puntuacion != u'C' or palabra_texto_previa == u'' or\
                        palabra_texto_previa[-1] not in [u'º', u'°']:
                    try:
                        # Intentamos convertirlo en número romano
                        palabra_texto = puntuacion_anterior + \
                            num2words(fromRoman(palabra_texto_sin_puntuacion), False, "es").\
                            replace(u'dieciseis', u'dieciséis') + puntuacion_posterior
                    except InvalidRomanNumeralError:
                        # No era romano. Deletreamos.
                        palabra_texto = puntuacion_anterior + \
                            Palabra.deletrea(palabra_texto_sin_puntuacion) + puntuacion_posterior
                else:
                    # Son grados centígrados
                    palabra_texto = puntuacion_anterior + u'centígrados' + puntuacion_posterior
                return palabra_texto
            elif u'.' in palabra_texto_sin_puntuacion:
                # Lo consideramos un acrónimo. Si contiene caracteres duplicados lo deletreamos y si no,
                # de momento eliminamos los puntos para intentar silabearlo.
                # Si no se consigue, se terminará deletreando.
                if len(palabra_texto_sin_puntuacion.split(u'.')[0]) == 1:
                    # Solo hay un caracter entre puntos. Quitamos los puntos y deletrearemos o no,
                    # dependiendo de que sea silabeable o no.
                    palabra_texto = palabra_texto_sin_puntuacion.replace(u'.', u'')
                else:
                    # Hay más de un carácter. Deletreamos del tirón
                    return puntuacion_anterior + Palabra.deletrea(palabra_texto_sin_puntuacion.replace(u'.', u'')) +\
                        (puntuacion_posterior if puntuacion_posterior != u'.' else u'')
            elif not Palabra(palabra_texto=palabra_texto_sin_puntuacion,
                             calcula_alofonos=False,
                             organiza_grafemas=False).sigue_fonotactica(restringe_coda_final=True):
                # Parece ser un acrónimo no pronunciable. Deletreamos.
                return puntuacion_anterior + Palabra.deletrea(palabra_texto_sin_puntuacion) +\
                       puntuacion_posterior
            else:
                # Si no, pues dejamos palabra_texto como está.
                palabra_texto = puntuacion_anterior + palabra_texto_sin_puntuacion + puntuacion_posterior

        # Vemos si hemos conseguido una expansión satisfactoria
        if not [letra for letra in palabra_texto
                if letra in MONOGRAFOS and isinstance(MONOGRAFOS[letra][0], GrafemaVocoide)]:
            # No contiene vocoides
            if not re.findall(u'[^IVXLCDM]', palabra_texto_sin_puntuacion):
                # Lo consideramos número romano.
                try:
                    # Si cuela como romano, lo compramos.
                    palabra_texto = puntuacion_anterior +\
                        num2words(fromRoman(palabra_texto_sin_puntuacion), False, "es").\
                        replace(u'dieciseis', u'dieciséis') + puntuacion_posterior
                except InvalidRomanNumeralError:
                    # Podemos tener casos como "DVD" en los que nos demos cuenta de que no es un nº romano.
                    # Pero en otros casos puede fallar: MIL -> "mil cuarenta y nueve", XL -> "cuarenta"
                    palabra_texto = puntuacion_anterior +\
                        Palabra.deletrea(palabra_texto_sin_puntuacion) + puntuacion_posterior
            else:
                # Si no hay vocales, deletreamos.
                palabra_texto = puntuacion_anterior + \
                    Palabra.deletrea(palabra_texto_sin_puntuacion) + puntuacion_posterior
        return palabra_texto

    @staticmethod
    def deletrea(palabra_texto, agrupa_numeros=False):
        """Devuelve el texto que representa el deletreo de esta palabra.

        Cuando deletreamos una cadena de caracteres, deletreamos cada carácter por separado (excepto los números,
        que se pueden agrupar) y ponemos como átonas todas las sílabas menos la sílaba tónica de la última palabra
        legible que extraigamos. Así, UGT será "ugeté", CC.OO. será "ceceoó"... También aceptamos plurales, como
        ONGs, que será "oenegés", y aceptamos pero no requerimos que haya puntos de separación (requerimos mayúsculas).

        :type palabra_texto: unicode
        :param palabra_texto: la palabra que pretendemos deletrear
        :type agrupa_numeros: bool
        :param agrupa_numeros: Si está a True, agrupamos dígitos consecutivos en un único número. Si no, cada dígito
            se deletrea por separado.
        :return:
        """
        if palabra_texto[-1] == u's' and len(palabra_texto) > 1 and \
                not Palabra.contiene_no_alfabeticos(palabra_texto[:-1]) and \
                not Palabra.contiene_minusculas(palabra_texto[:-1]):
            # Tenemos una lista de mayúsculas acabadas en "s". Consideramos que es plural y quitamos la "s"
            plural = True
            palabra_texto = palabra_texto[:-1]
        else:
            plural = False

        palabra_texto_deletreada = u''  # Aquí guardaremos el valor final
        # Usualmente un token es un carácter, salvo que agrupemos algún número
        if not agrupa_numeros:
            tokens = [caracter for caracter in palabra_texto]
        else:
            # Si agrupamos los números, no vamos carácter a carácter sino que unimos aquellos que son números
            tokens = RegexpTokenizer('(?:-?[0-9]{1,27}(?:[.][0-9]{3}){0,9})|[^0-9]').tokenize(palabra_texto)

        # Vamos deletreando cada token
        for token in tokens:
            if Palabra.es_numero(token.replace(u'.', u'').replace(u',', u'.')) and token[0] != u'0':
                # El token es un número sin ceros a la izquierda. Quitamos los puntos de miles, cambiamos las
                # comas decimales por puntos, y sacamos el número.
                palabra_texto_deletreada += (u' ' if len(palabra_texto_deletreada) > 0 else u'') + \
                    num2words(int(token.replace(u'.', u'').replace(u',', u'.')), False, "es"). \
                    replace(u'dieciseis', u'dieciséis')
            elif token in MONOGRAFOS:
                # No es un número, pero es un monógrafo conocido
                palabra_texto_deletreada += (u' ' if len(palabra_texto_deletreada) > 0 else u'') + \
                    MONOGRAFOS[token][0].get_deletreo()
            else:  # Raro: algún carácter en algún alfabeto que no es el español
                caracter_normalizado = unicodedata.normalize('NFKD', token).encode('ascii', 'ignore')
                if caracter_normalizado in MONOGRAFOS:
                    palabra_texto_deletreada += (u' ' if len(palabra_texto_deletreada) > 0 else u'') + \
                        MONOGRAFOS[caracter_normalizado][0].get_deletreo()
                else:
                    # Lo omitimos sin más
                    pass

        if palabra_texto_deletreada:  # Podría estar vacío
            if isinstance(MONOGRAFOS[palabra_texto_deletreada[-1]][0], MonografoPausa):
                # El deletreo puede incluir una coma al final, pero la quitamos.
                palabra_texto_deletreada = palabra_texto_deletreada[:-1]
            if not Palabra.contiene_no_alfabeticos(palabra_texto):
                # Es una sucesión de letras. Lo palabrizamos (metemos el deletreo completo como una única palabra).
                # Quitamos las tildes o las añadimos según corresponda.
                palabras_resultantes = palabra_texto_deletreada.split(u' ')
                if len(palabras_resultantes) > 1:
                    # Si sólo hubiera un deletreado, no habría nada que hacer. Pero hay más de uno. Hay que unirlos.
                    palabra_texto_deletreada = u''.join([TILDES_OPUESTAS[letra]
                                                         if letra in u'íéáóú' else letra
                                                         for letra in u''.join(palabras_resultantes)])
                    # Hacemos un cálculo de las sílabas que tiene la última palabra del deletreo del último token.
                    # Como solo habrá deletreos de letras, con este sencillo cálculo nos vale.
                    n_silabas_ultima_palabra = len([letra for letra in palabras_resultantes[-1]
                                                    if letra in u'ieaouíéáóú'])
                    if n_silabas_ultima_palabra == 1 and palabra_texto_deletreada[-1] in u'ieaou':
                        # Era un monosílabo acabado en vocal. Tenemos que acentuar esa vocal. Ninguna de las variantes
                        # llanas lleva acento alguno.
                        palabra_texto_deletreada = palabra_texto_deletreada[:-1] + \
                            TILDES_OPUESTAS[palabra_texto_deletreada[-1]]
                # Si teníamos un acrónimo, la palabra deletreada irá en mayúsculas
                if not Palabra.contiene_minusculas(palabra_texto):
                    palabra_texto_deletreada = palabra_texto_deletreada.upper()
                if plural and palabra_texto_deletreada[-1].lower() != u's':
                    # Si tenemos marca de plural, metemos la -s del plural. Los nombres de las letras siempre acaban
                    # en vocal excepto por la <x>, a la que no añadimos la -s. Al poner la -s no modificamos el acento.
                    palabra_texto_deletreada += u's'

        return palabra_texto_deletreada

    @staticmethod
    def extrae_puntuacion(palabra_texto):
        """Toma la cadena de caracteres y separa los caracteres de signos de puntuación al inicio y al final, del resto.

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres que separaremos en partes.
        :rtype: (unicode)
        :return: Devuelve tres cadenas de texto: (puntuación anterior, palabra sin puntuación, puntuación posterior)
        """
        posicion_inicial = 0
        while posicion_inicial < len(palabra_texto) and palabra_texto[posicion_inicial] in MONOGRAFOS and \
                isinstance(MONOGRAFOS[palabra_texto[posicion_inicial]][0], MonografoPausa):
            # Avanzamos hasta que no haya pausas previas
            posicion_inicial += 1
        posicion_final = len(palabra_texto) - 1
        while posicion_final >= posicion_inicial and palabra_texto[posicion_final] in MONOGRAFOS and isinstance(
                MONOGRAFOS[palabra_texto[posicion_final]][0], MonografoPausa):
            # Retrocedemos hasta que no haya más pausas posteriores
            posicion_final -= 1  # Al salir del bucle, marca el último carácter que no es pausa
        # No quitamos los puntos finales si son partes de acrónimos. Consideramos que es acrónimo
        # si la palabra incluye algún otro punto.
        # TODO: No gestionamos las abreviaturas
        if posicion_final < len(palabra_texto) - 1 and palabra_texto[posicion_final + 1] == u'.' and \
                u'.' in palabra_texto[posicion_inicial:posicion_final + 1]:
            posicion_final += 1
        return palabra_texto[:posicion_inicial],\
            palabra_texto[posicion_inicial:posicion_final + 1],\
            palabra_texto[posicion_final + 1:] if len(palabra_texto) > posicion_final + 1 else u''

    @staticmethod
    def contiene_minusculas(palabra_texto):
        """Nos dice si la cadena de caracteres contiene alguna letra minúscula

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres en cuestión sobre la que se hará la comprobación
        :rtype: bool
        :return: True si la cadena de caracteres contiene letras minúsculas o False si no
        """
        return len([letra for letra in palabra_texto if letra != letra.upper() and letra == letra.lower()])

    @staticmethod
    def contiene_mayusculas(palabra_texto):
        """Nos dice si la cadena de caracteres contiene alguna letra mayúscula

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres en cuestión sobre la que se hará la comprobación
        :rtype: bool
        :return: True si la cadena de caracteres contiene letras mayúsculas o False si no
        """
        return len([letra for letra in palabra_texto if letra != letra.lower() and letra == letra.upper()])

    @staticmethod
    def contiene_no_alfabeticos(palabra_texto):
        """Nos dice si la cadena de caracteres contiene algún carácter no alfabético

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres en cuestión sobre la que se hará la comprobación
        :rtype: bool
        :return: True si la cadena de caracteres contiene caracteres no alfabéticos o False si no
        """
        return len([letra for letra in palabra_texto if letra.lower() == letra.upper()])

    @staticmethod
    def contiene_numeros(palabra_texto):
        """Nos dice si la cadena de caracteres contiene números

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres en cuestión sobre la que se hará la comprobación
        :rtype: bool
        :return: True si la cadena de caracteres contiene números o False si no
        """
        return len([letra for letra in palabra_texto if
                    letra in MONOGRAFOS and isinstance(MONOGRAFOS[letra][0], GrafemaNumero)])

    @staticmethod
    def contiene_simbolos(palabra_texto):
        """Nos dice si la cadena de caracteres contiene algún simbolo

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres en cuestión sobre la que se hará la comprobación
        :rtype: bool
        :return: True si la cadena de caracteres contiene símbolos o False si no
        """
        return len([letra for letra in palabra_texto if
                    letra in MONOGRAFOS and isinstance(MONOGRAFOS[letra][0], GrafemaSimbolo)])

    @staticmethod
    def es_numero(palabra_texto):
        """Nos dice si la cadena de caracteres es un número (en completo)

        :type palabra_texto: unicode
        :param palabra_texto: La cadena de caracteres en cuestión sobre la que se hará la comprobación
        :rtype: bool
        :return: True si la cadena de caracteres es un número o False si no
        """
        if u',' in palabra_texto:
            palabra_texto = palabra_texto.replace(u'.', u'').replace(u',', u'.')
        try:
            float(palabra_texto)
            return True
        except ValueError:
            return False


class Juntura(Palabra):
    u"""La clase Juntura representa sílabas de palabras distintas en contacto. Es necesaria para hacer el resilabeo.

    La clase Juntura es subclase de Palabra. Representa un tipo especial de palabra, que se crea cogiendo una
    sílaba de una palabra (la sílaba de interés) que está en un extremo (inicio o fin), junto con la sílaba previa
    y la posterior (si existen). De esta forma le damos a la sílaba de interés el entorno fonético necesario para
    que sea capaz de realizar el resilabeo, al poner las palabras en contacto.
    """
    def funde_silabas(self, calcula_alofonos):
        u"""Funde la sílaba de interés (la 2ª de 3) con la siguiente, combinando sus elementos

        Se considera que la sílaba que estamos procesando tiene núcleo, y se pegan tras él los fonemas
        de la sílaba siguiente, desde la semivocal hasta el final. Y se recalculan los alófonos si es necesario.

        :type calcula_alofonos: bool
        :param calcula_alofonos: Si está a True, se recalculan los alófonos. Si no, no se recalculan.
        :return: None
        """
        silaba_actual = self._silabas[1]
        silaba_siguiente = self._silabas[2]
        if silaba_siguiente.get_fonema_semivocal():
            silaba_actual.set_fonema_semivocal(silaba_siguiente.get_fonema_semivocal())
        coda_siguiente = silaba_siguiente.get_fonemas_coda()
        if coda_siguiente:
            for fonema_coda in coda_siguiente:
                silaba_actual.append_fonema_coda(fonema_coda)
            if calcula_alofonos:
                # Si hace falta calcular alófonos, se hará más adelante. No obstante, al resilabear, la coda tiene un
                # tratamiento especial para que alófonos usualmente válidos únicamente en coda, puedan aparecer en el
                # ataque. Al resilabear, los alófonos de coda se omiten expresamente y no se recalculan.
                for alofono in silaba_siguiente.get_alofonos_coda():
                    silaba_actual.append_alofono_coda(alofono)
        if silaba_siguiente.get_fonema_pausa_posterior():
            silaba_actual.set_fonema_pausa_posterior(silaba_siguiente.get_fonema_pausa_posterior())
        silaba_actual.set_final_palabra(silaba_actual.get_final_palabra() or silaba_siguiente.get_final_palabra())
        if silaba_actual.get_tonica() or silaba_siguiente.get_tonica():
            if ACPR in [silaba_actual.get_tonica(), silaba_siguiente.get_tonica()]:
                silaba_actual.set_tonica(ACPR)
            else:
                silaba_actual.set_tonica(ACSC)
        else:
            silaba_actual.set_tonica(ATON)
        silaba_siguiente.reset_silaba()
        if calcula_alofonos:
            self.calcula_alofonos()

    def resilabea(self, calcula_alofonos):
        u"""Realiza el resilabeo de la Juntura.

        Las palabras están silabeadas y transcritas de forma independiente, como rodeadas de pausas. Pero en la cadena
        hablada se produce el fenómeno del resilabeado.
        Con este método ponemos en contacto cada sílaba final de palabra con la inicial de la siguiente y viceversa,
        y producimos cambios fonéticos en los cortes de palabra. Estos cambios consisten en:
            - El paso de una consonante en coda al ataque siguiente (pero manteniendo el alófono que nos hubiera salido
              al silabear la palabra en solitario).
            - Cambios en la consonante de coda al coarticularse con la consonante de ataque siguiente.
            - Cambios en la estructura del núcleo: una vocal cerrada átona en ataque/coda absoluto, puede pasar a ser
              (semi)consonante/semivocal de la siguiente/anterior sílaba. Esto produce que dos sílabas colapsen en una.
            - Nasalización de núcleos silábicos al quedar entre nasales.
        Se toman las tres sílabas de la Juntura (la que se está procesando, la anterior y la siguiente), que representan
        un punto de unión entre palabras, y se resilabean, cambiando la estructura interna de las sílabas según se
        requiera, y recalculando los nuevos alófonos. Se devuelve True si se han colapsado sílabas o False si no

        :type calcula_alofonos: bool
        :param calcula_alofonos: Si está a True se recalculan los alófonos, si no, no.
        :rtype: bool
        :return: Se devuelve True si se han fundido dos sílabas en una, o False si no.
        """
        # Variables auxiliares para seguir mejor el código
        silaba_actual = self._silabas[1]
        silaba_siguiente = self._silabas[2]

        if silaba_actual.get_fonema_pausa_posterior() or not silaba_siguiente.get_fonemas():
            # Estamos en la última sílaba y la pausa final, o no sigue nada.
            # Nada que resilabear.
            if calcula_alofonos:
                # Recalculamos alófonos por si el ataque se espirantiza en caso de oclusivas.
                self.calcula_alofonos()
            return False

        # Vemos qué tipo de contacto se produce entre sílabas y según eso actuaremos de distintas formas
        # Salvo que se salga expresamente con un return, se llama a calcula_alofonos al final.
        coda_inicial = silaba_actual.get_fonemas_coda()
        ataque_final = silaba_siguiente.get_fonemas_ataque()
        if coda_inicial and ataque_final:
            # Contacto consonante-consonante. Cambios en coda y/o ataque por coarticulación (más abajo)
            # Nos aseguramos también de que los fonemas largos se pueden a su vez combinar con otros.
            consonante_coda = coda_inicial[-1].get_fonema_ipa().replace(u'ː', u'')
            consonante_ataque = ataque_final[0].get_fonema_ipa().replace(u'ː', u'')
            # OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (el 2º evita el lazo inferior)
            if consonante_coda == consonante_ataque and consonante_coda != u'm':
                # Se nos han juntado dos consonantes iguales (que no son /m/, que cambia a [nm]).
                # Se produce un alargamiento consonántico. Pasamos la consonante de coda a la segunda sílaba.
                fonema_consonante_larga = FONEMAS[consonante_ataque + u'ː']
                silaba_siguiente.set_fonemas_ataque([fonema_consonante_larga] + ataque_final[1:])
                silaba_actual.recorta_coda()  # Eliminamos el último fonema/alófono
            # Dos consonantes coarticuladas. Recalculamos alófonos (más adelante)
        elif coda_inicial and not ataque_final:
            # Contacto consonante-vocoide. CODA -> ATAQUE.
            silaba_siguiente.prepend_fonema_ataque(coda_inicial[-1])
            if calcula_alofonos:
                silaba_siguiente.prepend_alofono_ataque(silaba_actual.get_alofonos_coda()[-1])
            silaba_actual.recorta_coda()
        elif not coda_inicial and ataque_final:
            # No hay coda previa y hay ataque posterior. Nada que silabear. Recalculamos
            # (por espirantización de ataque y tal).
            pass
        # Contacto (semi)vocal-vocal (imposible la semiconsonante, pues se consonantizaría)
        elif silaba_actual.get_fonema_semivocal():
            # Contacto semivocal-vocal
            if silaba_actual.get_tonica():  # or not silaba_siguiente.get_tonica():
                # No hay la combinación de tonicidad necesaria. No hacemos nada.
                pass
            elif silaba_actual.get_fonema_semivocal().get_localizacion() != \
                    silaba_siguiente.get_fonema_vocal().get_localizacion() \
                    or silaba_siguiente.get_fonema_vocal().get_abertura() != CERR:
                # Soy/hay alto/uno, Cou/Pau arde/indio.
                # Solo consonantizamos la semivocal con localización anterior.
                if silaba_actual.get_fonema_semivocal().get_localizacion() == ANTE:
                    silaba_siguiente.prepend_fonema_ataque(FONEMAS[u'ʝ̞'])
                    silaba_actual.reset_fonema_semivocal()
                else:
                    # De momento no hacemos nada con semivocales posteriores
                    pass
            else:
                # Soy indio, Pau hunde.
                # Lo dejamos así.
                pass
        elif silaba_actual.get_fonema_semiconsonante() and silaba_actual.get_fonema_vocal().get_abertura() == CERR:
            # Hay diptongo homogéneo.
            if silaba_actual.get_fonema_vocal().get_localizacion() == \
                    silaba_siguiente.get_fonema_vocal().get_localizacion() \
                    and silaba_siguiente.get_fonema_vocal().get_abertura() == CERR:
                # Muy indio/hindú, ciu urde/hundió.
                # Se produce un alargamiento de la vocal y se funden las sílabas.
                silaba_actual.set_fonema_vocal(
                    FONEMAS[silaba_siguiente.get_fonema_vocal().get_fonema_ipa().replace(u'ː', u'') + u'ː'])
                self.funde_silabas(calcula_alofonos)
                return True
            else:
                # Muy hábil/útil, Ciu hace/urde.
                if silaba_actual.get_tonica() or not silaba_siguiente.get_tonica():
                    # No hay la combinación de tonicidad necesaria. No hacemos nada.
                    pass
                # Solo consonantizamos la vocal con localización anterior.
                elif silaba_actual.get_fonema_vocal().get_localizacion() == ANTE:
                    silaba_siguiente.prepend_fonema_ataque(FONEMAS[u'ʝ̞'])
                    silaba_actual.vocaliza_semiconsonante()
                else:
                    # De momento no hacemos nada con semivocales posteriores
                    pass
        # Contacto vocal-vocal
        elif silaba_actual.get_fonema_vocal().get_fonema_ipa() == silaba_siguiente.get_fonema_vocal().get_fonema_ipa():
            if not silaba_siguiente.get_tonica():
                # Alargamiento vocálico. Unimos las dos.
                silaba_actual.set_fonema_vocal(
                    FONEMAS[silaba_actual.get_fonema_vocal().get_fonema_ipa().replace(u'ː', u'') + u'ː'])
                self.funde_silabas(calcula_alofonos)
                return True  # Cuando hay colapso devolvemos True
        # Contacto entre vocales distintas
        elif (silaba_actual.get_fonema_vocal().get_abertura() == CERR and not silaba_actual.get_tonica()) or \
             (silaba_siguiente.get_fonema_vocal().get_abertura() == CERR and not silaba_siguiente.get_tonica()):
            # Se crea un dip/triptongo.
            if silaba_actual.get_fonema_vocal().get_abertura() != CERR:
                # Contacto entre vocal fuerte y vocal débil.
                # Creamos un DIPTONTO DECRECIENTE. Convertimos a semivocal y fundimos sílabas.
                monografo_semivocal = [monografo for monografo in
                                       MONOGRAFOS[silaba_siguiente.get_fonema_vocal().get_fonema_ipa()]
                                       if isinstance(monografo, GrafemaSemivocal)][0]
                fonema_semivocal = FONEMAS[monografo_semivocal.get_fonemas_ipa()[0]]
                silaba_actual.set_fonema_semivocal(fonema_semivocal)
                # La sílaba siguiente no puede tener semiconsonante ni semivocal (vocal cerrada).
            else:
                # Contacto entre vocal débil átona y fuerte y tónica.
                # Creamos un DIPTONGO CRECIENTE. Convertimos a (semi)consonante y fundimos sílabas.
                if not silaba_actual.get_fonemas_ataque():
                    # Aparece una consonante.
                    if silaba_actual.get_fonema_vocal().get_localizacion() == ANTE:
                        silaba_actual.append_fonema_ataque(FONEMAS[u'ʝ̞'])
                        silaba_actual.reset_fonema_semiconsonante()
                    else:
                        # OJO: el carácter del grafema g es distinto del del fonema/alófono ɡ (el 2º sin lazo inferior)
                        silaba_actual.append_fonema_ataque(FONEMAS[u'ɡ'])
                        silaba_actual.set_fonema_semiconsonante(FONEMAS[u'w'])
                else:
                    # Se convierte en semiconsonante.
                    # Se crea DIPTONGO DECRECIENTE y fundimos sílabas.
                    monografo_semiconsonante = [monografo for monografo in
                                                MONOGRAFOS[silaba_actual.get_fonema_vocal().get_fonema_ipa()[0]]
                                                if isinstance(monografo, GrafemaSemiconsonante)][0]
                    fonema_semiconsonante = FONEMAS[monografo_semiconsonante.get_fonemas_ipa()[0]]
                    silaba_actual.set_fonema_semiconsonante(fonema_semiconsonante)
                silaba_actual.set_fonema_vocal(silaba_siguiente.get_fonema_vocal())
            self.funde_silabas(calcula_alofonos)
            return True  # Cuando hay colapso devolvemos True
        else:
            # Dos vocales en hiato. Nada que hacer.
            pass

        # Las semivocales suelen abrir a las vocales. Recalculamos alófonos en cualquier caso
        # salvo que se haya requerido lo contrario
        if calcula_alofonos:
            self.calcula_alofonos()
        return False
