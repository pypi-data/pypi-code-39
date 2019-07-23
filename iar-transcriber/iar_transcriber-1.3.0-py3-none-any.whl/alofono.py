#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Alófono y múltiples especializaciones de ella para representar los alófonos

La clase Alofono es la representación básica de un alófono. Contiene la información de los símbolos
IPA del alófono y del fonema del que es alófono. Además, incluye un listado con restricciones acerca
de los fonemas que deben aparecer en el entorno del alófono para que éste sea un alófono válido.

También se incluyen otras 6 clases que son especializaciones de Alofono, que sirven de apoyo y facilitan
el procesado de los distintos tipos de alófonos. La estructura de clases es la siguiente:
- Alofono:
    - AlofonoConsonante
    - AlofonoVocoide:
        - AlofonoVocal
        - AlofonoSemivocal
        - AlofonoSemiconsonante
    - AlofonoPausa
"""

from iar_transcriber.fon_consts import FONEMAS, FONEMA_VACIO

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Alofono:
    u"""Esta clase representa la descripción básica de un alófono.

    Contiene la información sobre el símbolo IPA que define al alófono y cuál es el fonema del que deriva.
    Además, contiene una serie de restricciones acerca de qué fonemas deben aparecer en el entorno
    (desde el fonema previo hasta tres fonemas después).
    """
    def __init__(self,
                 alofono_ipa=u'',
                 fonema_padre_ipa=u'',
                 fonemas_siguientes_ipa=None,
                 fonemas_postsiguientes_ipa=None,
                 fonemas_postpostsiguientes_ipa=None,
                 fonemas_previos_ipa=None):
        """Constructor para la clase Alofono

        :type alofono_ipa: unicode
        :param alofono_ipa: El símbolo IPA para este alófono
        :type fonema_padre_ipa: unicode
        :param fonema_padre_ipa: El símbolo IPA para el fonema que expresa este alófono
        :type fonemas_siguientes_ipa: [unicode]
        :param fonemas_siguientes_ipa: La lista de los fonemas que deben aparecer inmediatamente después
            para que aparezca este alófono. Si la lista está vacía (o es None), indica que no hay restricción.
        :type fonemas_postsiguientes_ipa: [unicode]
        :param fonemas_postsiguientes_ipa: La lista de los fonemas que deben aparecer 2 posiciones después
            para que aparezca este alófono. Si la lista está vacía (o es None), indica que no hay restricción.
        :type fonemas_postpostsiguientes_ipa: [unicode]
        :param fonemas_postpostsiguientes_ipa: La lista de los fonemas que deben aparecer 3 posiciones después
            para que aparezca este alófono. Si la lista está vacía (o es None), indica que no hay restricción.
        :type fonemas_previos_ipa: [unicode]
        :param fonemas_previos_ipa: La lista de los fonemas que deben aparecer inmediatamente antes
            para que aparezca este alófono. Si la lista está vacía (o es None), indica que no hay restricción.
        """
        self._alofono_ipa = alofono_ipa
        self._fonema_padre_ipa = fonema_padre_ipa
        # Esto siguiente está hecho como una lista porque facilita el procesado posterior, ya que
        # condiciones_fonema[posición relativa] (de -1 -posición previa- hasta +3, estando el 0 vacío,
        # pues es la posición del fonema en sí, y el alófono no se condiciona a sí mismo)
        # es la lista de fonemas que deben aparecer en esa posición relativa.
        self._condiciones_fonema = [[], fonemas_siguientes_ipa if fonemas_siguientes_ipa else [],
                                    fonemas_postsiguientes_ipa if fonemas_postsiguientes_ipa else [],
                                    fonemas_postpostsiguientes_ipa if fonemas_postpostsiguientes_ipa else [],
                                    fonemas_previos_ipa if fonemas_previos_ipa else []]

    def es_alofono_compatible(self, entorno, posicion_en_entorno):
        u"""Dado un entorno fonético y la posición que en dicho entorno ocupa el alófono, se determina si es compatible

        Cada alófono contiene una serie de restricciones en cuanto a qué fonemas deben aparecer previa y
        posteriormente para que el alófono aparezca. Por ejemplo, el fonema /n/ tiene múltiples realizaciones
        alofónicas (tantas como puntos de articulación consonántica), y entre ellos, el alófono [m] sólo aparece
        cuando está seguido de los fonemas /b/ o /p/. Igualmente, el alófono [ã] sólo puede aparecer si está
        seguido o precedido de nasal (pudiendo haber deslizantes entre la vocal y las nasales).

        Dado un fonema y su entorno, solo hay un único alófono que es compatible.

        :type entorno: [Fonema]
        :param entorno: Una lista de fonemas, entre los cuales está ubicado el fonema de quien queremos
            verificar si somos alófono válido o no.
        :type posicion_en_entorno: int
        :param posicion_en_entorno: La posición en el entorno del fonema cuyo alófono queremos calcular.
        :rtype: bool
        :return: True o False según sea compatible o no.
        """
        # Cada alófono tiene 4 grupo de restricciones que indican los fonemas que deben aparecer una posición
        # antes y hasta tres después. Verificamos aquí que estas 4 restricciones se cumplan para este entorno.
        for orden_condicion in [-1, 1, 2, 3]:
            # No hay restricciones para todas las posiciones. Si la lista de fonemas que deben aparecer en esa
            # posición está vacía, se interpreta como que no hay restricciones para esa posición
            if not self._condiciones_fonema[orden_condicion]:
                # No hay condición para esta posición. Pasamos a la siguiente condición.
                continue
            # Hay condición para esta posicion
            if 0 <= posicion_en_entorno + orden_condicion < len(entorno):
                # El entorno incluye un fonema para esta posición. Hay que comprobar la condición
                # OJO: quitamos el símbolo de segmento largo antes de la comparación.
                if entorno[posicion_en_entorno + orden_condicion].get_fonema_ipa().replace(u'ː', u'')\
                        in self._condiciones_fonema[orden_condicion]:
                    # Hay condición, un fonema para esta posición en el entorno, y cumple la condición.
                    continue
                else:
                    # Hay condición y fonema y no se cumple.
                    """
                    # OJO: No termino de ver el sentido de que se pase de <un> -> [ˈu̞n] a <un no> -> [ˈu.nːo] (cambio
                    # en la abertura de la vocal). El caso es que haciendo esto estamos considerando de alguna manera
                    # que las dos /n/ pasan al ataque y ninguna queda en coda, con lo que no se abre la vocal.
                    # Me parece que tiene más sentido ejecutar el código a continuación que no hacerlo.
                    # Sin embargo, todos los ejemplos del manual indican que no, que se trata a la vocal como si no
                    # tuviera coda.
                    # En el código siguiente vemos, para los fonemas posteriores al este alófono, que si el fonema
                    # precedente al que hace referencia la condición es geminado, es como si también estuviera ocupando
                    # la posición que estamos verificando, y por lo tanto tambien se cumpliría la condición si el fonema
                    # previo (la versión corta, quitando el símbolo de duración larga) está en la lista de fonemas
                    # necesarios para esta posición.
                    if 1 < orden_condicion <= 3 and\
                            isinstance(entorno[posicion_en_entorno + orden_condicion - 1], FonemaConsonante) and\
                            u'ː' in entorno[posicion_en_entorno + orden_condicion - 1].get_fonema_ipa() and\
                            entorno[posicion_en_entorno + orden_condicion - 1].get_fonema_ipa().replace(u'ː', u'') in\
                            self._condiciones_fonema[orden_condicion]:
                        # Las consonantes geminadas son en el fondo dos consonantes seguidas e influyen en esto.
                        continue
                    """
                    return False
            else:
                # El entorno no incluye fonemas para esta posición
                if u'|' in self._condiciones_fonema[orden_condicion]:
                    # Si se admite una pausa en esta posición, también se acepta que no haya fonema
                    continue
                else:
                    # Se fuerza que haya un fonema en concreto, pero no tenemos ninguno en el entorno dado
                    return False
        # Si hemos llegado hasta aquí es que no hemos tenido problemas con ninguna condición. El alófono es compatible
        return True

    def get_fonema_aparente(self):
        u"""Se devuelve el "fonema aparente" de este alófono: aquel fonema que coincide en carácter IPA con el alófono

        En ocasiones un fonema se expresa con un alófono que resulta coincidir con otro fonema distinto (es decir,
        dicho alófono es habitualmente el alófono con el que se expresa un fonema distinto al que ha originado
        este alófono). Cuando se da esta circunstancia, el fonema aparente resulta ser el fonema con el que
        coincide el alófono

        :rtype: Fonema
        :return: El objeto Fonema que representa al fonema que "parece ser" origen de este alófono
        """
        # Este método se puede utilizar para "refonemizar" un texto, obteniendo fonemas que no son los que
        # realmente indica la ortografía, pero que por pronunciación, aparentan ser los fonemas válidos.
        if self._alofono_ipa == u'':
            return FONEMA_VACIO
        # Para empezar tomamos como fonema aparente el propio fonema padre
        if self._alofono_ipa[-1] == u'ː':
            # Si es largo nos quedamos con la versión corta, para poder compararlo bien
            fonema_tipico_ipa = self._fonema_padre_ipa.replace(u'ː', u'')
            alofono_ipa = self._alofono_ipa[:-1]
        else:
            fonema_tipico_ipa = self._fonema_padre_ipa  # Por defecto
            alofono_ipa = self._alofono_ipa

        # Si el alófono es uno de los "conflictivos" (que pueden surgir por la aparición de más de un fonema),
        # cambiamos el fonema típico.
        if alofono_ipa in [u'n̟', u'n̪', u'n', u'ⁿ', u'ⁿ̠', u'n̠', u'ŋ', u'ɴ']:
            fonema_tipico_ipa = u'n'
        elif alofono_ipa in [u'm', u'ɱ']:
            fonema_tipico_ipa = u'm'
        elif alofono_ipa in [u'β̞']:
            fonema_tipico_ipa = u'b'
        elif alofono_ipa in [u'ð̞']:
            fonema_tipico_ipa = u'd'
        elif alofono_ipa in [u'ɣ̞']:
            # OJO: el carácter del grafema g es distinto del del fonema ɡ
            fonema_tipico_ipa = u'ɡ'

        # Tras haber calculado el fonema aparente, le ponemos la duración adecuada
        if self._alofono_ipa[-1] == u'ː':
            fonema_tipico_ipa += u'ː'
        return FONEMAS[fonema_tipico_ipa]

    def get_fonema_aparente_ipa(self):
        u"""Devuelve el caracter IPA del fonema aparente de este alófono

        :rtype: unicode
        :return: El carácter IPA del fonema aparente de este alófono
        """
        return self.get_fonema_aparente().get_fonema_ipa() if self._alofono_ipa else u''

    def get_alofono_ipa(self):
        u"""Devuelve el símbolo IPA para este alófono

        :rtype: unicode
        :return: El símbolo IPA que representa este alófono
        """
        return self._alofono_ipa

    def set_alofono_ipa(self, alofono_ipa):
        u"""Se fija el valor del símbolo IPA que representa a este alófono

        :type alofono_ipa: unicode
        :param alofono_ipa: El símbolo IPA para este alófono
        """
        self._alofono_ipa = alofono_ipa

    def get_fonema_padre_ipa(self):
        u"""Devuelve el símbolo IPA del fonema del que deriva este alófono (el fonema padre)

        :rtype: unicode
        :return: El símbolo IPA del fonema del que deriva este alófono
        """
        return self._fonema_padre_ipa

    def set_fonema_padre_ipa(self, fonema_padre_ipa):
        u"""Se fija el valor del símbolo IPA que representa al fonema que se expresa con este alófono

        :type fonema_padre_ipa: unicode
        :param fonema_padre_ipa: El símbolo IPA del alófono padre
        """
        self._fonema_padre_ipa = fonema_padre_ipa

    def get_condiciones_fonema(self):
        u"""Devuelve la lista de las condiciones de aparición de este alófono.

        :rtype: [[unicode]]
        :return: La lista de listas de símbolos IPA que representan las restricciones de aparición del alófono
        """
        return self._condiciones_fonema


class AlofonoVocoide(Alofono):
    u"""Esta subclase de Alofono es la clase padre para alófonos de vocoides.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de alófono y su
    procesamiento. Está vacía.
    """
    pass


class AlofonoVocal(AlofonoVocoide):
    u"""Esta subclase de AlofonoVocoide es la clase padre para alófonos de vocales.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de alófono y su
    procesamiento. Está vacía.
    """
    pass


class AlofonoSemivocal(AlofonoVocoide):
    u"""Esta subclase de AlofonoVocoide es la clase padre para alófonos de semivocales.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de alófono y su
    procesamiento. Está vacía.
    """
    pass


class AlofonoSemiconsonante(AlofonoVocoide):
    u"""Esta subclase de AlofonoVocoide es la clase padre para alófonos de semiconsonantes.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de alófono y su
    procesamiento. Está vacía.
    """
    pass


class AlofonoConsonante(Alofono):
    u"""Esta subclase de Alofono es la clase padre para alófonos de consonantes.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de alófono y su
    procesamiento. Está vacía.
    """
    pass


class AlofonoPausa(Alofono):
    u"""Esta subclase de Alofono es la clase padre para alófonos de pausas.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de alófono y su
    procesamiento. Está vacía.
    """
    pass
