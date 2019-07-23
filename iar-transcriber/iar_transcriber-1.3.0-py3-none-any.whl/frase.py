#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Frase, que representa la estructura (en objetos Palabra) de una frase.

La clase Frase toma un texto de entrada y lo divide en palabras, para crear posteriormente un objeto
Palabra con cada una de ellas. Si dichas palabras no son "legibles" (números, símbolos, acrónimos...)
procede a su conversión en palabras.

También es el encargado de producir el resilabeo de las palabras a nivel de frase, valiéndose para ello
de la clase Juntura, que es una especialización de la clase Palabra.
"""

from iar_tokenizer import Tokenizer
from iar_transcriber.palabra import Palabra, Juntura
from iar_transcriber.silaba import Silaba
from iar_transcriber.grafema import GrafemaSimbolo
from iar_transcriber.graf_consts import MONOGRAFOS
from iar_transcriber.fon_consts import FONEMAS, CERR
from iar_transcriber.alof_consts import ALOFONOS_PAUSA

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Frase:
    u"""La clase Frase es una representación estructurada (en objetos Palabra) de una frase.

    En esta clase se divide una frase (representada por un string) en palabras, creándose un objeto Palabra
    para cada una de ellas. Se expanden los símbolos, números y algunos caracteres no ortográficos.

    También, según los parámetros, se realiza el resilabeo de las palabras de la frase, se calculan los alófonos y
    se organizan los grafemas dentro de la sílaba (en vistas a realizar una transcripción ortográfica)

    Además, se inserta una epéntesis ([e] frente a grupos de /s/ + oclusiva en ataque)
    """

    def __init__(self, frase_texto, resilabea=True, calcula_alofonos=True,
                 inserta_epentesis=False, organiza_grafemas=False):
        u"""Constructor de la clase Frase

        :type frase_texto: unicode
        :param frase_texto: El texto (string) con la frase
        :type resilabea: bool
        :param resilabea: Si está a True (por defecto) se realiza el resilabeo. Si está a False, no.
        :type calcula_alofonos: bool
        :param calcula_alofonos: Si está a True, se calculan los alófonos (para hacer transcripciones fonéticas).
            Si está a False, no se calculan los alófonos (para transcripciones fonológicas u ortográficas).
        :type inserta_epentesis: bool
        :param inserta_epentesis: Si está a True, se inserta una [e] epentética ante grupo /s/ + oclusiva (solamente
            a inicio de palabra, puesto que todo grupo inválido en español aparece en coda o a inicio de palabra).
        :type organiza_grafemas: bool
        :param organiza_grafemas: Si está a True, se crea la estructura de grafemas (con vistas a hacer una
            transcripción ortográfica). Si está a False, no (para transcripciones fonéticas/fonológicas).
        """
        self._frase_texto = frase_texto
        self._palabras_texto = Tokenizer.segmenta_por_palabras([frase_texto], elimina_separadores=False,
                                                               segmenta_por_guiones_internos=False,
                                                               segmenta_por_guiones_externos=True,
                                                               adjunta_separadores=True,
                                                               agrupa_separadores=False)
        self._palabras = []  # Crearemos una lista de objetos Palabra con todas las palabras (legibles) del texto.
        # Nos aseguramos de que las palabras sean vocalizables. Tenemos que expandir todo aquello que no sea legible
        # tal y como está, sino que necesite algún tipo de expansión en (otros) caracteres alfabéticos.
        # Para empezar, cambiamos los símbolos por sus vocalizaciones.
        palabras_texto_sin_simbolos = []  # Variable auxiliar para las palabras texto tras expandir símbolos
        for palabra_texto in self._palabras_texto:
            if Palabra.contiene_simbolos(palabra_texto):
                # Si hay símbolos en la "palabra", los vocalizamos (y dejamos los no símbolos)
                inicio_subpalabra = 0  # Si los símbolos están mezclados con caracteres, sólo vocalizamos los símbolos
                for orden_caracter, caracter in enumerate(palabra_texto):
                    if caracter in MONOGRAFOS and isinstance(MONOGRAFOS[caracter][0], GrafemaSimbolo):
                        if orden_caracter > inicio_subpalabra:
                            # Había algo antes del símbolo, y lo consideramos palabra aparte.
                            palabras_texto_sin_simbolos += [palabra_texto[inicio_subpalabra:orden_caracter]]
                        # Vocalizamos el símbolo
                        palabras_texto_sin_simbolos += MONOGRAFOS[caracter][0].get_deletreo().split()
                        # Marcamos el nuevo posible inicio de subpalabra
                        inicio_subpalabra = orden_caracter + 1  # Hay un nuevo inicio de subpalabra tras el símbolo
                    elif orden_caracter == len(palabra_texto) - 1:
                        # Si el último no es símbolo, cogemos todos los caracteres desde el símbolo anterior
                        # y añadimos la palabra
                        palabras_texto_sin_simbolos += [palabra_texto[inicio_subpalabra:orden_caracter + 1]]
            else:
                # Si no hay símbolos, la dejamos como está
                palabras_texto_sin_simbolos += [palabra_texto]
        # Al haber troceado las palabras, pueden quedar signos de puntuación colgando. Por ejemplo, si la entrada era
        # <2%,>, quedará [u'2', u'por', u'ciento', u',']. Tenemos que volver a adjuntar la u',' con el u'ciento'.
        self._palabras_texto = Tokenizer.adjunta_separadores(palabras_texto_sin_simbolos,
                                                             separadores_agrupados=False,
                                                             segmentado_por_palabras=True)

        # Hemos eliminado símbolos, pero aún quedan los dígitos (que no deben deletrearse de uno en uno sino que
        # se deben agrupar varios dígitos en un número) y algunas otras cosas como números romanos, acrónimos y
        # demás que deben todavía expandirse en palabras legibles.
        for orden_palabra_texto, palabra_texto in enumerate(self._palabras_texto):
            palabras_legibles = Palabra.\
                convierte_a_palabras_legibles(palabra_texto,
                                              self._palabras_texto[orden_palabra_texto - 1]
                                              if orden_palabra_texto > 0 else u'',
                                              self._palabras_texto[orden_palabra_texto + 1]
                                              if orden_palabra_texto < len(self._palabras_texto) - 1 else u'')
            for palabra_legible in palabras_legibles.split(u' '):
                if palabra_legible:  # Podría estar vacía, por ejemplo el u'-' no tiene deletreo.
                    # Creamos un objeto Palabra por cada palabra legible y la añadimos a la lista
                    palabra = Palabra(palabra_texto=palabra_legible, calcula_alofonos=calcula_alofonos,
                                      inserta_epentesis=inserta_epentesis, organiza_grafemas=organiza_grafemas)
                    self._palabras.append(palabra)
        if self._palabras:  # Si hay una frase con un guion o solo signos de puntuación, puede no tener palabras
            # Metemos las pausas a inicio y final de frase.
            self._palabras[0].get_silabas()[0].set_fonema_pausa_previa(FONEMAS[u'‖'])
            self._palabras[0].get_silabas()[0].set_alofono_pausa_previa(ALOFONOS_PAUSA[u'‖'][0])
            self._palabras[-1].get_silabas()[-1].set_fonema_pausa_posterior(FONEMAS[u'‖'])
            self._palabras[-1].get_silabas()[-1].set_alofono_pausa_posterior(ALOFONOS_PAUSA[u'‖'][0])

        # Mantenemos una lista de todas las sílabas de la frase. Es necesaria únicamente para hacer el resilabeo,
        # pero como no estamos creando nada, sino que es simplemente una lista de referencias a sílaba, se hace
        # en cualquier caso porque puede resultar práctico y no ocupa demasiada memoria.
        self._silabas = [silaba for palabra in self._palabras for silaba in palabra.get_silabas()]
        # Para terminar, resilabeamos las palabras de la frase y recalculamos los alófonos si es necesario.
        # Si no hay que resilabear, cada palabra tendrá ya sus alófonos calculados (si hacen falta).
        if resilabea and self._silabas:
            self.resilabea(calcula_alofonos)

    def get_silabas(self):
        """Devuelve un listado con todas las sílabas de la frase.

        Si se ha resilabeado, puede no coincidir con las sílabas de las palabras por separado: además de cambios se
        pueden perder sílabas o incluso palabras completas.

        :rtype: [Silaba]
        :return: La lista de objetos Silaba que hay en esta frase (tras resilabear o no, según se haya especificado)
        """
        return self._silabas

    def get_palabras(self):
        """Devuelve un listado con todas los objetos Palabra de la frase.

        Si se ha resilabeado, puede no coincidir con el número de palabras por separado.

        :rtype: [Palabra]
        :return: La lista de objetos Palabra que hay en esta frase (tras resilabear o no, según se haya especificado)
        """
        return self._palabras

    def get_frase_texto(self):
        """Devuelve la cadena de texto original que se usó al crear la frase.

        :rtype: unicode
        :return: El texto con la frase.
        """
        return self._frase_texto

    def resilabea(self, calcula_alofonos):
        """Realiza el resilabeo de las sílabas de la frase y calcula los alófonos tras hacer los cambios.

        Se recrean los efectos del resilabeo, que produce cambios alofónicos en los contactos entre sílabas, así como
        la creación/destrucción/traslación de fonemas de unas sílabas a otras, lo que puede producir la pérdida de
        sílabas e incluso la desaparicion de alguna palabra completa.

        Además, y esto es un punto muy importante, puede realizar resilabeos dentro de una única palabra. Esto ocurre
        porque por defecto cada vocal crea una sílaba. Sin embargo, al resilabear es posible que dos vocales
        consecutivas se fundan en una única vocal larga, colapsando una sílaba. Así, de zoología, [θo.o.lɔ.ˈxi.a],
        se pasa a [θoː.lɔ.ˈxi.a].

        :type calcula_alofonos: bool
        :param calcula_alofonos: Si está a True se calculan los alófonos (si vamos a hacer una transcripción fonética)
            y si está a False no se realiza (para una transcripción fonológica/ortográfica).
        :return: None
        """
        # Hasta llegar a este punto, las palabras están silabeadas y transcritas de forma independiente, como
        # rodeadas de pausas. En este método vamos a fusionar cada sílaba final de palabra con la inicial de la
        # siguiente y produciremos cambios fonéticos en los cortes de palabra.
        # Estos cambios consisten en:
        # - Cambios alofónicos (principalmente cambio de punto de articulación en coda/ataque y de apertura vocálica).
        # - Cambio de tipo de fonema: cambios entre (semi)consonante y (semi)vocal.
        # - Traslación de fonemas de una sílaba a la siguiente (de coda a ataque). En estos casos se
        #   mantiene el alófono que se hubiera obtenido inicialmente cuando el fonema ocupaba posición de coda
        # - Cambios en la estructura del núcleo: una vocal cerrada átona en ataque/coda absoluto, puede pasar a ser
        #   (semi)consonante/semivocal de la siguiente/anterior sílaba. Esto produce que se colapsen dos sílabas en una
        # - Nasalización de núcleos vocálicos al quedar entre nasales.
        # - Colapso de sílabas y alargamiento de vocal cuando hay dos sílabas que contienen la misma vocal de núcleo
        #   y no existen más fonemas entre los dos.
        if not self._silabas:
            # No hay nada aún. Nada que hacer.
            return

        # Es posible crear un objeto Frase sin resilabear y/o sin calcular alófonos y posteriormente llamar a este
        # método para resilabear esas palabras no resilabeadas, y además, si se quiere, calcular los alófonos.
        # El problema es que si queremos resilabear y además calcular alófonos, y previamente no habíamos hecho
        # ninguna de las dos cosas, no tendremos la estructura de alófonos creada. Al resilabear, cuenta con que
        # algunos alófonos no se modifican y se dejan "como estaban" (como las codas ensordecidas a final de palabra)
        # Resumiendo: antes de resilabear y recalcular los alófonos hace falta calcularlos en la palabra aislada.
        if calcula_alofonos and not self._silabas[0].get_alofonos(incluye_pausas=False):
            self._silabas = []
            for palabra in self._palabras:
                palabra.calcula_alofonos()
                self._silabas += palabra.get_silabas()

        orden_silaba = 0  # Llevamos un contador aparte porque vamos a modificar la propia lista mientras la procesamos
        while orden_silaba < len(self._silabas):
            # Vamos a ir prestando atención a una sílaba cada vez. Sin embargo, para calcular los efectos del resilabeo
            # necesitamos la sílaba previa y siguiente a aquella que estamos procesando (si existen)
            # Nos fijamos principalmente en las sílabas que tienen un corte de palabra a su izquierda o derecha, o
            # en aquellas que acaben en vocal y dicha vocal sea la que comience la sílaba siguiente (para unirlas en
            # un fonema largo). En realidad, como las palabras raramente superan las dos sílabas, se procesan casi todas
            # las sílabas.
            # Al unir dos palabras, esto afecta a la última sílaba de la primera palabra y a la primera sílaba de
            # la segunda palabra. De ahí que necesitemos la sílaba anterior y la siguiente, puesto que la sílaba que
            # estemos procesando puede estar tanto al inicio de una palabra como al final (o incluso entre medias, en
            # caso de combinación de dos vocales en una vocal larga).

            # Comenzamos calculando el entorno de la sílaba: sílaba previa y siguiente, si existen (si no, vacías)
            silaba_anterior = self._silabas[orden_silaba - 1]\
                if orden_silaba > 0 and not self._silabas[orden_silaba - 1].get_fonema_pausa_posterior()\
                else Silaba()
            silaba_actual = self._silabas[orden_silaba]
            silaba_siguiente = self._silabas[orden_silaba + 1]\
                if orden_silaba < len(self._silabas) and not self._silabas[orden_silaba].get_fonema_pausa_posterior()\
                else Silaba()
            silabas_de_interes = [silaba_anterior, silaba_actual, silaba_siguiente]
            # La juntura es simplemente una palabra hecha con los extremos de otras. Se usa para resilabear,
            # ya que al ser una especialización de Palabra, hereda sus métodos y puede recalcular los alófonos
            # una vez hayamos hecho los cambios en las sílabas debida al resilabeo.
            juntura = Juntura(silabas=silabas_de_interes, calcula_alofonos=False)  # De momento no calculamos alófonos

            # Calculamos si la sílaba tiene uno de sus extremos en contacto con fonemas de otras palabras, sin que
            # existan pausas entre ellas.
            # Vamos, que calculamos si la sílaba resulta estar en contacto directo con una sílaba de otra palabra
            necesita_resilabeo =\
                (silaba_actual.get_final_palabra() and not silaba_actual.get_fonema_pausa_posterior() and
                 orden_silaba < len(self._silabas) - 1 and silaba_siguiente.get_fonemas() and
                 not silaba_siguiente.get_fonema_pausa_previa()) or\
                (silaba_actual.get_inicio_palabra() and not silaba_actual.get_fonema_pausa_previa() and
                 orden_silaba > 0 and silaba_anterior.get_fonemas() and
                 not silaba_anterior.get_fonema_pausa_posterior())

            if necesita_resilabeo:
                # Hay un problema cuando no tenemos semivocal ni coda, ya que en el caso de que la sílaba siguiente
                # contenga únicamente la vocal /i/ o /u/, en principio la podríamos tomar como semivocal de la
                # sílaba actual. Pero cabe la posibilidad de que no sea eso lo que tenemos que hacer, sino que dicha
                # vocal siguiente se consonantice y pase a formar parte de la sílaba postsiguiente.
                # Estas excepciones ocurren cuando la sílaba siguiente es simplemente /i/ o /u/ y dicha
                # sílaba es la única de la palabra, y además la sílaba postsiguiente no tiene ataque ni semiconsonante
                # (y dicha vocal no es la misma que la /i/ o /u/ previa). En estos casos, la vocal /i/ o /u/ de la
                # sílaba siguiente no se convierte en semivocal sino que se consonantiza y se asocia con la
                # sílaba postsiguiente.
                # Lo comprobamos, y si es el caso no resilabeamos pero sí que recalculamos los alófonos (por posibles
                # cambios alofónicos al tener
                if not silaba_actual.get_fonemas_coda() and not silaba_actual.get_fonema_semivocal():
                    if orden_silaba + 2 < len(self._silabas):
                        silaba_postsiguiente = self._silabas[orden_silaba + 2]
                        if len(silaba_siguiente.get_fonemas(incluye_pausas=False)) == 1 and \
                                silaba_siguiente.get_fonema_vocal().get_abertura() == CERR and \
                                silaba_siguiente.get_final_palabra() and \
                                not silaba_siguiente.get_fonema_pausa_posterior() and \
                                not silaba_postsiguiente.get_fonemas_ataque() and \
                                not silaba_postsiguiente.get_fonema_semiconsonante() and \
                                (silaba_postsiguiente.get_fonema_vocal().get_abertura() != CERR or
                                 silaba_postsiguiente.get_fonema_vocal().get_localizacion() !=
                                 silaba_siguiente.get_fonema_vocal().get_localizacion()):
                            # La sílaba siguiente se asocia con la postsiguiente y no con la actual. No obstante, quizá
                            # haya cambios alofónicos en el ataque, si estamos a inicio de palabra.
                            if silaba_actual.get_inicio_palabra():
                                juntura.calcula_alofonos()
                            orden_silaba += 1
                            continue
            else:
                # Si no se necesita el resilabeo por ser sílabas en contacto de palabras distintas, miramos si nos
                # hace falta resilabear porque tengamos una vocal que se alargue (incluso dentro de una palabra).
                necesita_resilabeo =\
                    orden_silaba < len(self._silabas) - 1 and silaba_siguiente.get_fonemas() and\
                    not silaba_siguiente.get_tonica() and\
                    not silaba_actual.get_fonemas_coda(incluye_pausas=True) and\
                    not silaba_siguiente.get_fonema_semiconsonante() and\
                    not silaba_siguiente.get_fonemas_ataque() and\
                    not silaba_actual.get_fonema_semivocal() and\
                    silaba_actual.get_fonema_vocal().get_fonema_ipa() ==\
                    silaba_siguiente.get_fonema_vocal().get_fonema_ipa()
                # Al exigir que el fonema sea el mismo, uniremos las vocales como mucho de dos en dos. Estaría la
                # opción de sólo comparar el primer carácter y así podríamos unir todos las vocales que haya seguidas
                # como una única vocal larga.

            if necesita_resilabeo:
                # Hemos llegado a un corte de palabra por izquierda o derecha que no está separada por pausa,
                # o a dos sílabas que se van a fusionar por alargamiento vocálico. Resilabeamos.
                colapso = juntura.resilabea(calcula_alofonos)
                if colapso:  # Si hay colapso, la sílaba que se está procesando y la siguiente se han fundido
                    del self._silabas[orden_silaba + 1]
                    # Volvemos a reanalizar la sílaba, por si la nueva siguiente sílaba influyera. Por ejemplo, al
                    # resilabear <no unís>, partimos de [no] + [u.ˈni̞s], y al analizar [no] la unimos con la siguiente
                    # sílaba [u], dando [ˈnou̯] + [ˈni̞s]. Si pasáramos a la siguiente sílaba ahora, [ˈni̞s], nos
                    # perderíamos el hecho de que ahora el núcleo vocálico queda en entorno nasal, con lo que no
                    # podríamos generar la forma correcta [nõũ̯.ˈni̞s].
                    # Resumiendo: que no aumentamos el contador del orden de sílaba
                    continue
            orden_silaba += 1

        # Al resilabear puede haber monosílabos que se hayan quedado vacíos (principalmente una "y" que se semivocaliza)
        # Las borramos
        orden_palabra = 0
        while orden_palabra < len(self._palabras):
            if not self._palabras[orden_palabra].get_silabas():
                del self._palabras[orden_palabra]
            else:
                orden_palabra += 1

    def transcribe_ortograficamente_frase(self, marca_tonica=False, incluye_pausas=True,
                                          separador=u'-', apertura=u'<', cierre=u'>'):
        u"""Se devuelve la transcripción ortográfica de la frase, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type incluye_pausas: bool
        :param incluye_pausas: Si está a True, se incluye en la transcripción las pausas que toda frase tiene
            (al inicio y) al final.
        :type separador: unicode
        :param separador: Un string que se coloca entre sílabas
        :type apertura: unicode
        :param apertura: Un string que se coloca al inicio
        :type cierre: unicode
        :param cierre: Un string que se coloca al final
        :rtype: unicode
        :return: La transcripción ortográfica de la frase, según los parámetros
        """
        transcripcion_frase = u''
        for palabra in self._palabras:
            transcripcion_palabra = u''
            for orden_silaba, silaba in enumerate(palabra.get_silabas()):
                transcripcion_silaba = silaba.transcribe_ortograficamente_silaba(marca_tonica, incluye_pausas)
                if transcripcion_silaba:
                    if transcripcion_palabra:
                        transcripcion_palabra += separador  # Toca meter el separador
                    transcripcion_palabra += transcripcion_silaba
            transcripcion_frase += (u' ' if transcripcion_frase else u'') + transcripcion_palabra
        return apertura + transcripcion_frase + cierre

    def transcribe_fonologicamente_frase(self, marca_tonica=True, incluye_pausa_previa=False,
                                         incluye_pausa_posterior=False, transcribe_fonemas_aparentes=False,
                                         separador=u'.', apertura=u'/', cierre=u'/'):
        u"""Se devuelve la transcripción fonológica de la frase, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type incluye_pausa_previa: bool
        :param incluye_pausa_previa: Si está a True, se incluye en la transcripción las pausas que toda frase tiene
            al inicio.
        :type incluye_pausa_posterior: bool
        :param incluye_pausa_posterior: Si está a True, se incluye en la transcripción las pausas que toda frase tiene
            al final.
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
        transcripcion_frase = u''
        for orden_silaba, silaba in enumerate(self._silabas):
            transcripcion_silaba = silaba.transcribe_fonologicamente_silaba(
                marca_tonica=marca_tonica,
                incluye_pausa_previa=transcripcion_frase != u'' or incluye_pausa_previa,
                incluye_pausa_posterior=orden_silaba < len(self._silabas) - 1 or incluye_pausa_posterior,
                transcribe_fonemas_aparentes=transcribe_fonemas_aparentes)
            if transcripcion_silaba:
                if transcripcion_frase:
                    if transcripcion_frase[-1] not in [u'|', u'‖']:
                        if not transcripcion_silaba[0] in [u'|', u'‖']:
                            transcripcion_frase += separador  # Toca meter el separador
                    elif transcripcion_silaba[0] in [u'|', u'‖']:
                        if transcripcion_silaba[0] == u'‖':
                            transcripcion_frase = transcripcion_frase[-1] + u'‖'
                        transcripcion_silaba = transcripcion_silaba[1:]
                transcripcion_frase += transcripcion_silaba
        # Cabe la posibilidad de tener textos raros como "Sí, ()", que se transcribe como /ˈsi|/, con una pausa,
        # porque el "()" final se convierte en una sílaba fonéticamente vacía (no conviene que la borremos, porque
        # quizá hagamos la transcripción ortográfica).
        if not incluye_pausa_posterior and transcripcion_frase and transcripcion_frase[-1] in [u'|', u'‖']:
            transcripcion_frase = transcripcion_frase[:-1]

        return apertura + transcripcion_frase + cierre

    def transcribe_foneticamente_frase(self, marca_tonica=True, incluye_pausa_previa=False,
                                       incluye_pausa_posterior=False, ancha=False,
                                       separador=u'.', apertura=u'[', cierre=u']'):
        u"""Se devuelve la transcripción fonética de la frase, generando un string que depende de los parámetros.

        :type marca_tonica: bool
        :param marca_tonica: Si está a True se incluyen en la transcripción los símbolos de acento, y si está a False
            no se incluyen
        :type incluye_pausa_previa: bool
        :param incluye_pausa_previa: Si está a True, se incluye en la transcripción la pausa que toda frase tiene
            al inicio.
        :type incluye_pausa_posterior: bool
        :param incluye_pausa_posterior: Si está a True, se incluye en la transcripción la pausa que toda frase tiene
            al final.
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
        :return: el string con la transcripción fonética (alófonos) de la frase, según los parámetros
        """
        transcripcion_frase = u''
        for orden_silaba, silaba in enumerate(self._silabas):
            transcripcion_silaba = silaba.transcribe_foneticamente_silaba(
                marca_tonica=marca_tonica,
                incluye_pausa_previa=transcripcion_frase != u'' or incluye_pausa_previa,
                incluye_pausa_posterior=orden_silaba < len(self._silabas) - 1 or incluye_pausa_posterior,
                ancha=ancha)
            if transcripcion_silaba:
                if transcripcion_frase:
                    if transcripcion_frase[-1] not in [u'|', u'‖']:
                        if not transcripcion_silaba[0] in [u'|', u'‖']:
                            transcripcion_frase += separador  # Toca meter el separador
                    elif transcripcion_silaba[0] in [u'|', u'‖']:
                        if transcripcion_silaba[0] == u'‖':
                            transcripcion_frase = transcripcion_frase[-1] + u'‖'
                        transcripcion_silaba = transcripcion_silaba[1:]
                transcripcion_frase += transcripcion_silaba
        # Cabe la posibilidad de tener textos raros como "Sí, ()", que se transcribe como [ˈsi|], con una pausa,
        # porque el "()" final se convierte en una sílaba fonéticamente vacía (no conviene que la borremos, porque
        # quizá hagamos la transcripción ortográfica).
        if not incluye_pausa_posterior and transcripcion_frase and transcripcion_frase[-1] in [u'|', u'‖']:
            transcripcion_frase = transcripcion_frase[:-1]
        return apertura + transcripcion_frase + cierre
