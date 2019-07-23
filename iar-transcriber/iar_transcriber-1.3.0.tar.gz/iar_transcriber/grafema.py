#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Grafema y múltiples especializaciones de ella para representar los grafemas

La clase Grafema es la representación básica de un grafema. Contiene un único grafema (el primario),
además de una lista de strings, donde cada uno es la representación IPA de un fonema (cada grafema
puede representar a varios fonemas o incluso a más de uno). También contiene el deletreo del grafema
para poder hacer deletreos.

También se incluyen otras 21 clases que son especializaciones de Grafema, que sirven de apoyo y facilitan
el procesado de los distintos tipos de grafemas. La estructura de clases es la siguiente:
- Grafema:
    - Digrafo
    - GrafemaConsonante:
        - MonografoConsonante
        - (+Digrafo) DigrafoConsonante
    - GrafemaVocoide:
        - GrafemaVocal:
            - MonografoVocal
        - GrafemaSemivocal:
            - MonografoSemivocal
        - GrafemaSemiconsonante:
            - MonografoSemiconsonante
    - GrafemaMudo:
        - MonografoMudo
    - GrafemaPausa:
        - MonografoPausa
    - GrafemaSimbolo:
        - MonografoSimbolo
    - GrafemaNumero:
        - MonografoNumero
    - GrafemaOrdinal:
        - MonografoOrdinal
"""

from iar_transcriber.fon_consts import CERR, ANTE, POST, LADE, ALVE, POAL, PALA, NASA, OCLU, AFRI, FRIC, APRO, LATE, VIBM, VIBS, \
    FONEMAS, FonemaConsonante

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Grafema:
    u"""Esta clase representa la descripción básica de un grafema.

    Tiene información sobre el grafema (carácter) en sí, la representación IPA del fonema que representa y un string
    que indica cómo deletrear el grafema.
    También se definen algunas constantes, incluyendo una estructura auxiliar para quitar/poner tildes a las vocales.
    """
    def __init__(self, grafema_primario, fonemas_ipa, deletreo):
        u"""Constructor para la clase Grafema.

        :type grafema_primario: unicode
        :param grafema_primario: Un carácter que representa (es) el único grafema de un monógrafo, o el primero de
            los dos grafemas de un dígrafo: <ch>, <ll>, <rr>, <qu>, <gu>, <tx> y <tz>
        :type fonemas_ipa: [unicode]
        :param fonemas_ipa: los fonemas (caracter más diacríticos API) que expresa el grafema
        :type deletreo: unicode
        :param deletreo: indica con qué palabra(s) se lee el carácter aislado, para poder hacer deletreos.
        """
        self._grafema_primario = grafema_primario
        self._fonemas_ipa = fonemas_ipa
        self._deletreo = deletreo

    def get_grafema_primario(self):
        u"""Devuelve el string con el grafema primario del grafema.

        Devuelve el string (un único carácter) que representa el único grafema de un monógrafo, o el primero de los
        dos grafemas de un dígrafo.

        :rtype: unicode
        :return: El grafema primario (un string con un único carácter)
        """
        return self._grafema_primario

    def set_grafema_primario(self, grafema_primario):
        u"""Se establece el valor para el grafema primario (único carácter en monógrafos, o el primero en dígrafos.

        :type grafema_primario: unicode
        :param grafema_primario: El grafema primario que se debe asignar
        :return: None
        """
        self._grafema_primario = grafema_primario

    def get_fonemas_ipa(self):
        u"""Devuelve una lista con los fonemas para este grafema, expresados como caracteres con formato IPA.

        :rtype: [unicode]
        :return: La lista con los strings que representan con qué caracter IPA se expresa este grafema
        """
        return self._fonemas_ipa

    def set_fonemas_ipa(self, fonemas_ipa):
        u"""Se establece el valor para el listado de fonemas que se expresan con este grafema

        :type fonemas_ipa: [unicode]
        :param fonemas_ipa: La lista de fonemas en formato IPA con los que se expresa este grafema
        :return: None
        """
        self._fonemas_ipa = fonemas_ipa

    def get_deletreo(self):
        u"""Devuelve el string que indica, ortográficamente, cómo pronunciar este carácter cuando va en solitario.

        :rtype: unicode
        :return: El string con la representación ortográfica del símbolo, según tenga que pronunciarse
        """
        return self._deletreo

    def get_grafema_txt(self):
        u"""Devuelve la representación como string del grafema completo (en monógrafos, únicamente el grafema primario).

        Para grafemas que no sean monógrafos, este método se debe sobreescribir

        :rtype: unicode
        :return: La cadena de caracteres que conforman el grafema (en monógrafos, un único carácter)
        """
        return self._grafema_primario

    def es_grafema_compatible(self, graf_pre, graf_multi_post, graf_multi_post_post=None,
                              graf_multi_post_post_post=None, distancia_a_previo=1):
        u"""Determina si el grafema es compatible en el entorno fonético dado por los parámetros

        Como se procesan los grafemas de las palabras de izquierda a derecha, el entorno consiste en el grafema
        anterior (ya desambiguado) y los tres grafemas siguientes (cada uno de ellos como una lista aún no desambiguada
        de grafemas (con sus valores fonéticos) que pueden expresarse con ese mismo carácter.

        En el entorno se descartan los grafemas mudos (que no tienen relevancia para calcular la expresión fonética
        de un grafema). No obstante, se debe incluir el parámetro que indica a qué distancia (cuántos grafemas) está
        el grafema previo (que se nos da como parámetro). Esto es importante porque hay ocasiones en las que un
        grafema es compatible o no dependiendo de si hay o no mudos previos: por ejemplo, para diferenciar
        <deshielo> de <desierto>, donde la <i> es consonante en el primer caso (y <s> es coda) y semiconsonante en el
        segundo (donde la <s> es ataque).

        La necesidad de un entorno fonético tan amplio (tres grafemas a la derecha) está motivado principalmente por
        la capacidad de algunos grafemas, como <i>, de expresarse como (semi)consonante o (semi)vocal, y puede
        configurar la sílaba de muy diversas formas dependiendo de qué tipo de fonema exprese y a qué silaba pertenezca.

        Esta es una implementación base que devuelve siempre True y que tendrá que ser sobreescrita en las
        clases hijas cuando sea necesario.

        :type graf_pre: Grafema
        :param graf_pre: El grafema previo al actual
        :type graf_multi_post: [Grafema]
        :param graf_multi_post: la lista de grafemas posibles para el carácter 1 posición después del actual
        :type graf_multi_post_post: [Grafema]
        :param graf_multi_post_post: la lista de grafemas posibles para el carácter 2 posiciones después del actual
        :type graf_multi_post_post_post: [Grafema]
        :param graf_multi_post_post_post: la lista de grafemas posibles para el carácter 3 posiciones después del actual
        :type distancia_a_previo: int
        :param distancia_a_previo: Cuántos grafemas atrás se encuentra el grafema previo (saltando mudos)
        :rtype: bool
        :return: True si el grafema es compatible en el entorno dado, o False si no.
        """
        return True

    def transcribe_foneticamente_grafema(self):
        u"""Devuelve la transcripción fonética del grafema. Usualmente un único carácter IPA, a veces (como <x>) más

        :rtype: unicode
        :return: La transcripción fonética del grafema.
        """
        transcripcion_fonetica = u''
        for fonema in self._fonemas_ipa:
            transcripcion_fonetica += fonema
        return transcripcion_fonetica


class GrafemaVocoide(Grafema):
    u"""Esta subclase de Grafema es la clase padre para semiconsonantes, vocales y semivocales.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaVocal(GrafemaVocoide):
    u"""Clase que representa a los grafemas que actúan como vocal.

    Hereda de la clase padre y añade el atributo sobre la existencia o no de tilde ortográfica.
    """
    def __init__(self, grafema_primario, fonemas_ipa, deletreo, tilde):
        u"""Constructor para la clase GrafemaVocal.

        :type grafema_primario: unicode
        :param grafema_primario: Un carácter que representa (es) el único grafema de un monógrafo vocálico.
        :type fonemas_ipa: [unicode]
        :param fonemas_ipa: los fonemas (caracter más diacríticos API) que expresa el grafema
        :type deletreo: unicode
        :param deletreo: indica con qué palabra(s) se lee el carácter aislado, para poder hacer deletreos.
        :type tilde: bool
        :param tilde: True si el grafema tiene tilde ortográfica.
        """
        GrafemaVocoide.__init__(self, grafema_primario, fonemas_ipa, deletreo)
        self._tilde = tilde

    def get_tilde(self):
        u"""Devuelve un booleano indicando si el grafema tiene o no tilde ortográfica

        :rtype: bool
        :return: True si el grafema tiene tilde, False si no
        """
        return self._tilde


class GrafemaSemivocal(GrafemaVocoide):
    u"""Esta subclase de GrafemaVocoide es la clase padre para los monógrafos de semivocales.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaSemiconsonante(GrafemaVocoide):
    u"""Esta subclase de GrafemaVocoide es la clase padre para los monógrafos de semiconsonantes.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaConsonante(Grafema):
    u"""Esta subclase de Grafema es la clase padre para los grafemas consonánticos (monógrafos y dígrafos).

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaMudo(Grafema):
    u"""Esta subclase de Grafema es la clase padre para los grafemas mudos.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaPausa(Grafema):
    u"""Esta subclase de Grafema es la clase padre para los grafemas de pausa, como: ¿, ?, ., :, ...

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaSimbolo(Grafema):
    u"""Esta subclase de Grafema es la clase padre para los grafemas de símbolo, como: $, @, %...

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaNumero(Grafema):
    u"""Esta subclase de Grafema es la clase padre para los grafemas de números (0-9)

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class GrafemaOrdinal(Grafema):
    u"""Esta subclase de Grafema es la clase padre para los grafemas que indican un ordinal, como: ª, º, ...

    Añade el atributo de género, que indica si el ordinal es masculino o femenino, lo que repercute en la transcripción.
    """
    def __init__(self, grafema_primario, fonemas_ipa, deletreo, genero):
        u"""Constructor para la clase GrafemaOrdinal

        :type grafema_primario: unicode
        :param grafema_primario: Un carácter que representa el grafema primario de este grafema
        :type fonemas_ipa: [unicode]
        :param fonemas_ipa: los fonemas (caracter más diacríticos API) que expresa el grafema
        :type deletreo: unicode
        :param deletreo: indica con qué palabra(s) se lee el carácter aislado, para poder hacer deletreos.
        :type genero: bool
        :param genero: True si es femenino, False si es masculino
        """
        Grafema.__init__(self, grafema_primario, fonemas_ipa, deletreo)
        self._genero = genero

    def get_genero(self):
        u""" Devuelve el valor de género del grafema

        :rtype: bool
        :return: True si es femenino, False si es masculino
        """
        return self._genero


class Digrafo(Grafema):
    u"""Esta subclase de Grafema es la clase padre para los dígrafos, como: <ch>, <ll>, <rr>, <gu>, <qu>, <tx>, <tz>...

    Añade el atributo de grafema secundarios, que da el segundo carácter del dígrafo.
    """
    def __init__(self, grafema_primario, grafema_secundario, fonemas_ipa, deletreo):
        u"""Constructor para la clase Digrafo

        :type grafema_primario: unicode
        :param grafema_primario: Un carácter que representa el grafema primario de este grafema
        :type grafema_secundario: unicode
        :param grafema_secundario: Un carácter que representa el grafema secundario (el 2º) de este grafema
        :type fonemas_ipa: [unicode]
        :param fonemas_ipa: los fonemas (caracter más diacríticos API) que expresa el grafema
        :type deletreo: unicode
        :param deletreo: indica con qué palabra(s) se lee el carácter aislado, para poder hacer deletreos.
        """
        Grafema.__init__(self, grafema_primario, fonemas_ipa, deletreo)
        self._grafema_secundario = grafema_secundario

    def get_grafema_secundario(self):
        u""" Devuelve el valor del grafema_secundario del grafema

        :rtype: unicode
        :return: El carácter en segunda posición del dígrafo
        """
        return self._grafema_secundario

    def set_grafema_secundario(self, grafema_secundario):
        u"""Se establece el valor para el grafema secundario.

        :type grafema_secundario: unicode
        :param grafema_secundario: El grafema primario que se debe asignar
        :return: None
        """
        self._grafema_secundario = grafema_secundario

    def get_grafema_txt(self):
        u"""Devuelve la representación como string del grafema completo.

        :rtype: unicode
        :return: La cadena de caracteres que conforman el dígrafo
        """
        return self._grafema_primario + self._grafema_secundario

    def es_grafema_compatible(self, graf_pre, graf_multi_post, graf_multi_post_post=None,
                              graf_multi_post_post_post=None, distancia_a_previo=1):
        u"""Determina si el grafema es compatible en el entorno fonético dado por los parámetros

        (Véase el docstring para la clase base Grafema)

        :type graf_pre: Grafema
        :param graf_pre: El grafema previo al actual
        :type graf_multi_post: [Grafema]
        :param graf_multi_post: la lista de grafemas posibles para el carácter 1 posición después del actual
        :type graf_multi_post_post: [Grafema]
        :param graf_multi_post_post: la lista de grafemas posibles para el carácter 2 posiciones después del actual
        :type graf_multi_post_post_post: [Grafema]
        :param graf_multi_post_post_post: la lista de grafemas posibles para el carácter 3 posiciones después del actual
        :type distancia_a_previo: int
        :param distancia_a_previo: Cuántos grafemas atrás se encuentra el grafema previo (saltando mudos)
        :rtype: bool
        :return: True si el grafema es compatible en el entorno dado, o False si no.
        """
        fonema = FONEMAS[self._fonemas_ipa[-1]]  # No hay dígrafos multifonémicos, pero siempre manda el último fonema
        mda = fonema.get_mda()
        if self._grafema_secundario == u'u':
            # Somos <qu>/<gu> y queremos ver si es válido.
            if graf_multi_post and isinstance(graf_multi_post[0], GrafemaVocoide) and\
                    FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() == ANTE and\
                    graf_multi_post[0].get_grafema_txt().lower() != u'y':
                # Sigue un vocoide anterior que no es el grafema <y>. Es válido.
                return True
            return False
        elif self._grafema_secundario == u'r':
            # Somos <rr>. Lo consideramos válido siempre, tanto en coda (enfática, joderrrr), como en ataque
            # (rrato, trrato, arre).
            return True
        elif self._grafema_secundario == u'l':
            # Entra <ll>, que puede representar /ʎ/, /ʝ̞/, /ʒ/, /ʃ/ pero sólo si sigue vocal u otra <l>. Si no, es /l/
            if mda == LATE and fonema.get_pda() == ALVE:
                # La variante del dígrafo <ll> como una /l/
                if not graf_multi_post or (not isinstance(graf_multi_post[0], GrafemaVocoide) and
                                           graf_multi_post[0].get_grafema_primario().lower() != u'l'):
                    return True
                # Como la l-ll es un tanto especial, quizá al acabar de extraer todos los grafemas, lo cambiemos.
                # De momento rechazamos el dígrafo.
                return False
            else:
                # Pues es la representación fonética habitual para <ll>: /ʎ/, /ʝ̞/, /ʒ/, /ʃ/.
                if graf_multi_post and (isinstance(graf_multi_post[0], GrafemaVocoide) or
                                        graf_multi_post[0].get_grafema_primario().lower() == u'l'):
                    # Como la l-ll es un tanto especial, quizá al acabar de extraer todos los grafemas, lo cambiemos.
                    return True
                return False
        # Somos alguna de las variantes de la /ʧ/: <ch>, <tx>, <tz>. Siempre se acepta
        return True


class MonografoVocal(GrafemaVocal):
    u"""Esta subclase de GrafemaVocal es la clase padre para los monógrafos vocálicos.
    """
    def es_grafema_compatible(self, graf_pre, graf_multi_post, graf_multi_post_post=None,
                              graf_multi_post_post_post=None, distancia_a_previo=1):
        u"""Determina si el grafema es compatible en el entorno fonético dado por los parámetros

        La lógica es bastante compleja, principalmente debido a que las vocales cerradas, cuando se combinan entre sí,
        pueden dar resultados que dependen de varios grafemas posteriores. Por ejemplo, en la secuencia: pu, pui, puiu,
        puiui, la primera <u> es, respectivamente, vocal, semivocal, vocal y semivocal, dependiendo de qué caracteres
        se añadan: /ˈpu|ˈpwi|ˈpu.ʝ̞u|ˈpwi.ɡwi/

        (Véase el docstring para la clase base Grafema)

        :type graf_pre: Grafema
        :param graf_pre: El grafema previo al actual
        :type graf_multi_post: [Grafema]
        :param graf_multi_post: la lista de grafemas posibles para el carácter 1 posición después del actual
        :type graf_multi_post_post: [Grafema]
        :param graf_multi_post_post: la lista de grafemas posibles para el carácter 2 posiciones después del actual
        :type graf_multi_post_post_post: [Grafema]
        :param graf_multi_post_post_post: la lista de grafemas posibles para el carácter 3 posiciones después del actual
        :type distancia_a_previo: int
        :param distancia_a_previo: Cuántos grafemas atrás se encuentra el grafema previo (saltando mudos)
        :rtype: bool
        :return: True si el grafema es compatible en el entorno dado, o False si no.
        """
        # Tenemos un carácter <i>, <u>, <y> (y sus variantes con tilde/diéresis, mayúscula o minúscula, o incluso <&>)
        # y queremos ver si esta, su variante vocálica, es compatible. Los factores a tener en cuenta son muchísimoa y
        # se van desgranando en el código a continuación.
        if graf_pre and (isinstance(graf_pre, GrafemaSemiconsonante) or
                         (isinstance(graf_pre, GrafemaConsonante) and graf_pre.get_fonemas_ipa()[-1] == u'w')):
            # Si el grafema previo es una semiconsonante, a la fuerza somos vocal.
            return True
        if graf_pre and isinstance(graf_pre, GrafemaVocal) and \
                FONEMAS[graf_pre.get_fonemas_ipa()[0]].get_abertura() != CERR:
            # Está precedida de vocal fuerte. Seremos semivocal (hay, aunque), o consonante (alcahuete)
            # de la siguiente sílaba. No somos vocal.
            return False
        if not graf_multi_post:
            # A final de palabra, y además precedidos de consonante, de semivocal (i/y/u) o nada (inicio de palabra)
            # Somos vocal: tú, Hawaii, y
            return True
        if not isinstance(graf_multi_post[0], GrafemaVocoide):
            # Precedidos de consonante, semivocal (i/y/u) o nada;
            # y seguidos de consonante. Somos vocal.
            return True
        if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
            # Precedidos de consonante, semivocal (i/y/u) o nada;
            # y seguidos de vocal fuerte. Somos (semi)consonante: cueva, güerto.
            return False
        # Precedidos de consonante, i/y/u o nada;
        # y seguidos de i/y/u...
        if self._grafema_primario.lower() == u'y':
            # Somos la <y>. Si estamos precedidos de consonante haremos como que somos la <i>.
            if isinstance(graf_pre, GrafemaConsonante) and graf_pre.get_fonemas_ipa()[-1] != u'w':
                # Es raro. Si sigue u seremos semivocal, y si no, seremos vocal.
                if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                        FONEMAS[self._fonemas_ipa[-1]].get_localizacion():
                    # Seguido de i/y. Cosas raras como chyi, chyy -> chi-i. Somos vocal.
                    return True
                # seguidos de <u>. Somos semivocal: pyuda -> pjuda.
                return False
            # Somos la <y> Precedido de i/y/u o nada, y seguido de i/y/u.
            # Somos consonante: yy, yu, iyu, puyita.
            return False
        # Precedidos de consonante, i/y/u o nada;
        # y seguidos de i/u, y no somos la "y"...
        if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                FONEMAS[self._fonemas_ipa[-1]].get_localizacion():
            # Seguidos de vocoide de igual localización y no somos "y". No nos asociamos al siguiente. Vocal: chii.
            return True
        # Precedidos de consonante, i/y/u o nada;
        # y seguidos de vocoide i/y/u de distinta localización y no somos la "y".
        # Seremos (semi)consonante de ese vocoide (salvo que ese vocoide sea (semi)consonante de una vocal siguiente).
        if not graf_multi_post_post:
            # No postsigue nada. Somos (semi)consonante. Uy, fui.
            return False
        if not isinstance(graf_multi_post_post[0], GrafemaVocoide):
            # Postsigue consonante. Somos (semi)consonante: ruin, iul.
            return False
        # Precedidos de consonante, i/y/u o nada;
        # y seguidos de vocoide i/y/u de distinta localización y no somos la "y";
        # postseguidos de i/y/u...
        if graf_multi_post[0].get_grafema_primario().lower() == u'y':
            # Nos sigue una "y". Como le postsigue i/y/u será consonántica y nosotros seremos vocal: muyo.
            return True
        if FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
            # Al vocoide siguiente de distinta localización le postsigue vocal fuerte, luego el vocoide es consonante
            # de la vocal fuerte que le postsigue. Somos vocal: cuyo, vihuela.
            return True
        # Precedidos de consonante, i/y/u o nada;
        # seguidos de i/u de distinta localización, al que postsigue i/y/u.
        if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() == \
                FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_localizacion():
            # Si la siguiente y postsiguiente son iguales, ambas serán vocales y nosotros (semi)consonante.
            return False
        if not graf_multi_post_post_post:
            # No postpostsigue nada. Somos vocal: muiu, iui.
            return True
        if not isinstance(graf_multi_post_post_post[0], GrafemaVocoide):
            # Postpostsigue consonante. Somos vocal: muiun, iuil
            return True
        # Precedidos de consonante, i/y/u o nada;
        # seguidos de i/u de distinta localización, al que postsigue i/y/u, y postpostsigue vocoide.
        if graf_multi_post_post[0].get_grafema_primario().lower() == u'y':
            # Nos postsigue una "y". Como le postpostsigue vocoide será consonántica
            # y nosotros seremos (semi)consonante: iuyu, muiyi, viuyo.
            return False
        if FONEMAS[graf_multi_post_post_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
            # Al i/u postsiguiente le postpostsigue vocal fuerte, luego el i/u postsiguiente es consonante
            # de la vocal fuerte que nos postpostsigue. El vocoide de distinta localización que nos sigue es la
            # vocal y nosotros somos (semi)consonante: muiuo -> muiguo
            return False
        # Precedidos de consonante, i/y/u o nada;
        # seguidos de i/u de distinta localización, al que postsigue i/u, y postpostsigue i/y/u.
        # Si el que postsigue puede ser consonante del siguiente (si hay distinta localización), seremos semivocal.
        if FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_localizacion() != \
                FONEMAS[graf_multi_post_post_post[0].get_fonemas_ipa()[0]].get_localizacion():
            # El postsiguiente es consonante del postpostsiguiente, y nosotros (semi)consonante del siguiente.
            return False
        # La postsiguiente y la postpostsiguiente van en sílabas distintas. La siguiente es consonante de la
        # postsiguiente y nosotros vocal.
        return True


class MonografoSemivocal(GrafemaSemivocal):
    u"""Esta subclase de GrafemaSemivocal es la clase padre para los monógrafos semivocálicos.
    """
    def es_grafema_compatible(self, graf_pre, graf_multi_post, graf_multi_post_post=None,
                              graf_multi_post_post_post=None, distancia_a_previo=1):
        u"""Determina si el grafema es compatible en el entorno fonético dado por los parámetros

        (Véase el docstring para la clase base Grafema)

        :type graf_pre: Grafema
        :param graf_pre: El grafema previo al actual
        :type graf_multi_post: [Grafema]
        :param graf_multi_post: la lista de grafemas posibles para el carácter 1 posición después del actual
        :type graf_multi_post_post: [Grafema]
        :param graf_multi_post_post: la lista de grafemas posibles para el carácter 2 posiciones después del actual
        :type graf_multi_post_post_post: [Grafema]
        :param graf_multi_post_post_post: la lista de grafemas posibles para el carácter 3 posiciones después del actual
        :type distancia_a_previo: int
        :param distancia_a_previo: Cuántos grafemas atrás se encuentra el grafema previo (saltando mudos)
        :rtype: bool
        :return: True si el grafema es compatible en el entorno dado, o False si no.
        """
        # Tenemos una vocal cerrada no acentuada (<u>, <i>, <y>) que tenemos que comprobar que es semivocálica.
        if not graf_pre or not isinstance(graf_pre, GrafemaVocal)\
                or FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_abertura() == CERR:
            # No está precedida de vocal fuerte. Imposible ser semivocal.
            return False
        if not graf_multi_post:
            # Precedidos de vocal fuerte a final de palabra. Semivocal.
            return True
        if not isinstance(graf_multi_post[0], GrafemaVocoide):
            # Precedidos de vocal fuerte y seguidos de consonante. Semivocal.
            return True
        if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
            # Precedidos de vocal fuerte pero seguidos de vocal fuerte. Nos asociamos con la siguiente vocal.
            # Somos (semi)consonante y no semivocal.
            return False
        if self._grafema_primario.lower() == u'y':
            # Somos una "y" seguidos de i/y/u. Consonante en cualquier caso.
            return False
        if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                FONEMAS[self._fonemas_ipa[-1]].get_localizacion():
            # Precedidos de vocal fuerte, seguidos de vocoide de igual localización y no somos "y" (au-u, ai-i, ai-y).
            # Somos semivocal
            return True
        # Precedidos de vocal fuerte y seguidos de vocoide de distinta localización.
        # Puede ser (semi)consonante o semivocal. Hay dos opciones:
        # - Somos una <i> en posición a-I-u.
        # - Somos una <u> en posición a-U-i/y.
        # En ambos casos somos semivocal si estamos seguidos de <y> (aI-yi, aI-yu, aU-yi, aU-yu) o de
        # vocoide abierto (aI-au), o cerrado pero de distinta localización a la previa (aI-ui, aI-uy, aU-iu, aU-yu).
        # Seremos semiconsonante en el resto de casos (a-Iu-u, a-Ui-i, a-Ui-y y consonantes y tal)
        if graf_multi_post[0].get_grafema_primario().lower() == u'y' or\
                (graf_multi_post_post and isinstance(graf_multi_post_post[0], GrafemaVocoide) and
                 (FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR or
                  FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() !=
                  FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_localizacion())):
            # Semivocal.
            return True
        # Semiconsonante.
        return False


class MonografoSemiconsonante(GrafemaSemiconsonante):
    u"""Esta subclase de GrafemaSemiconsonante es la clase padre para los monógrafos semiconsonánticos.
    """
    def es_grafema_compatible(self, graf_pre, graf_multi_post, graf_multi_post_post=None,
                              graf_multi_post_post_post=None, distancia_a_previo=1):
        u"""Determina si el grafema es compatible en el entorno fonético dado por los parámetros

        (Véase el docstring para la clase base Grafema)

        :type graf_pre: Grafema
        :param graf_pre: El grafema previo al actual
        :type graf_multi_post: [Grafema]
        :param graf_multi_post: la lista de grafemas posibles para el carácter 1 posición después del actual
        :type graf_multi_post_post: [Grafema]
        :param graf_multi_post_post: la lista de grafemas posibles para el carácter 2 posiciones después del actual
        :type graf_multi_post_post_post: [Grafema]
        :param graf_multi_post_post_post: la lista de grafemas posibles para el carácter 3 posiciones después del actual
        :type distancia_a_previo: int
        :param distancia_a_previo: Cuántos grafemas atrás se encuentra el grafema previo (saltando mudos)
        :rtype: bool
        :return: True si el grafema es compatible en el entorno dado, o False si no.
        """
        # Tenemos una vocal cerrada no acentuada (<u>, <i>, <y>) y tenemos que comprobar que es semiconsonántica.
        if not graf_pre or not isinstance(graf_pre, GrafemaConsonante) or distancia_a_previo > 1:
            # Si no hay consonante previa (o hay un mudo entre medias) seremos consonante: huerto, hielo -> güerto, yelo
            return False
        if not graf_multi_post or not isinstance(graf_multi_post[0], GrafemaVocoide):
            # Si no hay fonema siguiente o no es vocoide no se puede ser semiconsonante.
            return False
        if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
            # Sigue vocal fuerte, seremos su semiconsonante
            return True
        if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                FONEMAS[self._fonemas_ipa[-1]].get_localizacion():
            # Sigue vocal cerrada de igual localización, somos vocal.
            return False  # chii, chiyi
        if not graf_multi_post_post or not isinstance(graf_multi_post_post[0], GrafemaVocoide):
            # Sigue vocal cerrada de distinta localización y después nada. Somos semiconsonante.
            return True  # chiu, chuy, chiul, chuyl
        if graf_multi_post[0].get_grafema_primario().lower() == u'y':
            # Sigue <y> al que sigue un vocoide. Somos vocal.
            return False  # chiyi
        if FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
            # Lo que sigue no es <y> y le postsigue una vocal fuerte. Lo siguiente es consonante y nosotros vocal.
            return False  # chiuo, chuie
        if FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion():
            # Después de la vocal cerrada hay otra igual, así que seremos la semiconsonante del siguiente grafema.
            return True  # chiuu, chuiy
        if not graf_multi_post_post_post or not isinstance(graf_multi_post_post_post[0], GrafemaVocoide):
            return False  # chiuy, chuiu, chiuil, chuius
        if graf_multi_post_post[0].get_grafema_primario().lower() == u'y':
            return True   # chiuyi
        if FONEMAS[graf_multi_post_post_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
            return True  # chiuio
        if FONEMAS[graf_multi_post_post_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_localizacion():
            return False  # chiuii, chuiuu
        return True  # chiuiu, chuiui


class MonografoConsonante(GrafemaConsonante):
    u"""Esta subclase de GrafemaConsonante es la clase padre para los monógrafos consonánticos.
    """
    def es_grafema_compatible(self, graf_pre, graf_multi_post, graf_multi_post_post=None,
                              graf_multi_post_post_post=None, distancia_a_previo=1):
        u"""Determina si el grafema es compatible en el entorno fonético dado por los parámetros

        (Véase el docstring para la clase base Grafema)

        :type graf_pre: Grafema
        :param graf_pre: El grafema previo al actual
        :type graf_multi_post: [Grafema]
        :param graf_multi_post: la lista de grafemas posibles para el carácter 1 posición después del actual
        :type graf_multi_post_post: [Grafema]
        :param graf_multi_post_post: la lista de grafemas posibles para el carácter 2 posiciones después del actual
        :type graf_multi_post_post_post: [Grafema]
        :param graf_multi_post_post_post: la lista de grafemas posibles para el carácter 3 posiciones después del actual
        :type distancia_a_previo: int
        :param distancia_a_previo: Cuántos grafemas atrás se encuentra el grafema previo (saltando mudos)
        :rtype: bool
        :return: True si el grafema es compatible en el entorno dado, o False si no.
        """
        # Tenemos problemas con varios grafemas que pueden expresar una consonante u otra cosa, pero no de forma
        # unívoca: <c>, <g>, <r>, que pueden expresar más de un fonema, <y>, <i>, <u> que pueden ser múltiples cosas
        # incluyendo consonante, y la <x> que expresa 1-2 fonemas según toque.
        # Decidiremos si este grafema se expresa con este fonema, o si no es compatible dado el entorno
        fonema = FONEMAS[self._fonemas_ipa[-1]]  # Nos fijamos en el último fonema con que se expresa este grafema.
        if isinstance(fonema, FonemaConsonante):
            # No somos la variante consonántica de la <u>. Nos fijamos en el modo de articulación
            mda = fonema.get_mda()
            if mda == OCLU:
                # Somos la <c>/<g> oclusivas, la <w> o la <x> que pierde la /s/ final y queda en /k/
                if self._grafema_primario.lower() == u'w':
                    if not graf_multi_post or not isinstance(graf_multi_post[0], GrafemaVocoide) or \
                            (FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_abertura() == CERR and
                             FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() == POST):
                        # Tenemos el valor de /b/ y no de /gw/
                        return True
                    return False
                elif self._grafema_primario.lower() == u'x':
                    # Somos la versión /k/ de la <x>. Solo es válido si sigue <r> o <s>
                    if graf_multi_post and isinstance(graf_multi_post[0], GrafemaConsonante) and\
                            FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_pda() == ALVE and\
                            FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_mda() in [VIBM, FRIC]:
                        return True
                    return False
                # Somos la <c>/<g> con valor oclusivo. Somos válidos salvo que siga vocoide anterior.
                elif graf_multi_post and isinstance(graf_multi_post[0], GrafemaVocoide) and\
                        (FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() == ANTE):
                    # Somos <c>/<g> con valor oclusivo y sigue vocal anterior. Es inválido.
                    return False
                # Somos la <c>/<g> con valor oclusivo y sigue vocoide no anterior, o nada. Es la opción válida.
                return True
            elif mda == FRIC and fonema.get_pda() != POAL:
                # Somos la <x> con valor /s/ o /ks/ o la <c>/<g> con valor fricativo.
                if self._grafema_primario.lower() == u'x':
                    # Somos la <x>
                    if len(self._fonemas_ipa) > 1:
                        # Somos la versión /ks/ de <x>. Solo es compatible si es intervocálica.
                        if graf_pre and isinstance(graf_pre, GrafemaVocoide) and graf_multi_post and\
                                isinstance(graf_multi_post[0], GrafemaVocoide):
                            # Una <x> intervocálica se expresa como /ks/. Es compatible.
                            return True
                        return False
                    # Somos la versión /s/ de la <x>. Es compatible si no es intervocálica o si no sigue
                    # un grafema <s>, <r>, <x>
                    if graf_multi_post and graf_multi_post[0].get_grafema_primario() in u'srx':
                        # Seguida de <s>, <r>, <x>
                        return False
                    if graf_pre and isinstance(graf_pre, GrafemaVocoide) and\
                            graf_multi_post and isinstance(graf_multi_post[0], GrafemaVocoide):
                        # Intervocálica.
                        return False
                    # Ni es intervocálica ni sigue <s>, <r>, <x>. Es compatible
                    return True
                else:
                    # Somos la <c>/<g> con valor fricativo. Solo es válido si sigue un vocoide anterior.
                    if graf_multi_post and isinstance(graf_multi_post[0], GrafemaVocoide) and\
                            (FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() == ANTE):
                        # Sigue vocal anterior
                        return True
                    return False
            elif fonema.get_pda() in [POAL, PALA] and\
                    (mda in [LATE, APRO, FRIC] or (mda == AFRI and fonema.get_sonoridad())):
                # Somos /ʎ/, /ʝ̞/, /ʒ/, /ʃ/.
                if self._grafema_primario.lower() == u'l'\
                        and graf_pre and graf_pre.get_grafema_primario().lower() == u'l' and distancia_a_previo == 1:
                    # La <l> se considera /ʎ/ si está inmediatamente precedida de /ʎ/. Es para que acepte cosas
                    # como polllllo (con impar número de <l>), y lo identifique con la palatal, y en colll sea alveolar.
                    return True
                elif graf_multi_post and isinstance(graf_multi_post[0], GrafemaVocoide):
                    # Sigue un vocoide.
                    if self._grafema_primario.lower() in [u'l', u'y']:
                        # Somos <l>, <y> (con valor palatal) seguido de vocoide. Somos compatibles.
                        return True
                    # Somos la <i> con valor aproximante palatal. Es compatible si sigue un vocoide no anterior, y si
                    # está a inicio de palabra o está precedido de vocoide (dejan una <i> intervocálica) o de mudo
                    # (normalmente <h> o <->)
                    elif (not graf_pre or not isinstance(graf_pre, GrafemaConsonante) or distancia_a_previo > 1) and\
                            (FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR or
                             (FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() != ANTE)):
                        # Somos consonante: ie, ia, io, iu -> ye, ya, yo, yu
                        return True
                # Estamos a final de palabra o no sigue vocoide. Ni la <l>, ni la <y>, <i> pueden tener valor
                # consonántico palatal.
                return False
            elif mda == VIBS:
                # Somos la variante de vibrante simple para la <r>. No es compatible a inicio de palabra o si va
                # precedida de <x> (que se habrá expresado como /k/), o si precede una alveolar o nasal o fricativa
                # que no sea labiodental (/f/).
                if not graf_pre or graf_pre.get_grafema_primario().lower() == u'x' or\
                        (isinstance(graf_pre, GrafemaConsonante) and
                         ((FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_pda() == ALVE) or
                          (FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_mda() == NASA) or
                          (FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_mda() == FRIC and
                           FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_pda() != LADE))):
                    # Estamos a inicio de palabra o precedidos de <x>, nasal, de alveolar o de fricativa no labiodental,
                    # es decir, precedida de <x>, <n>, <m>, <ñ>, <r>, /l/, /s/, /θ/, /x/, /ʒ/, /ʃ/
                    return False
                # Es válida como vibrante simple, ya sea en ataque simple o complejo, o coda.
                return True
            elif mda == VIBM:
                # Somos la variante vibrante múltiple de <r>. Es compatible en los casos inversos que la vibrante simple
                if not graf_pre or graf_pre.get_grafema_primario().lower() == u'x' or\
                        (isinstance(graf_pre, GrafemaConsonante) and
                         ((FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_pda() == ALVE) or
                          (FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_mda() == NASA) or
                          (FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_mda() == FRIC and
                           FONEMAS[graf_pre.get_fonemas_ipa()[-1]].get_pda() != LADE))):
                    # Estamos a inicio de palabra o precedidos de nasal, de alveolar o de fricativa no labiodental.
                    return True
                return False
            elif mda == LATE and fonema.get_pda() == ALVE:
                # Somos la <l> con su valor lateral alveolar habitual. Compatible salvo que estemos precedido de otra
                # consonante igual (es un caso un tanto anómalo debido a que las repeticiones de <l> son un tanto
                # especial, en cuanto a que pueden tomarse como <ll> pero en coda no)
                if not graf_pre or graf_pre.get_grafema_primario().lower() != u'l' or distancia_a_previo > 1:
                    # Somos una /l/ válida (lo habitual salvo cosas como polllo)
                    return True
                return False
        else:
            # Somos la variante consonántica (+ semiconsonante) de <u> (o la <ü> <w>, pero es casi lo mismo).
            if self._grafema_primario.lower() == u'w':
                if not graf_multi_post or not isinstance(graf_multi_post[0], GrafemaVocoide) or \
                        (FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_abertura() == CERR and
                         FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() == POST):
                    # Tenemos el valor de /b/ y no de /gw/
                    return False
                return True
            if graf_pre and isinstance(graf_pre, GrafemaConsonante) and distancia_a_previo == 1:
                # Tenemos una consonante previa que no está separada por una <h>, <->, así que seremos semiconsonante
                # o vocal, pero no consonante.
                return False
            if not graf_multi_post or not isinstance(graf_multi_post[0], GrafemaVocoide):
                # No sigue nada o no es un vocoide, así que no podemos ser consonante
                return False
            if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
                # Sigue una vocal fuerte, así que somos compatibles
                return True
            if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                    FONEMAS[self._fonemas_ipa[-1]].get_localizacion():
                # Sigue otra <u>, así que seremos vocal
                return False
            # Sigue una <i>/<y>
            if not graf_multi_post_post or not isinstance(graf_multi_post_post[0], GrafemaVocoide):
                # Tras la <i>/<y> que precede hay una consonante. Somos compatibles: uil
                return True
            if FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
                # Tras la <i>/<y> que precede hay una vocal fuerte, así que la <i>/<y> es consonante y nosotros somos
                # vocal: uio.
                return False
            if graf_multi_post[0].get_grafema_primario().lower() == u'y':
                # Somos <u> seguido de <y> y seguido de vocoide cerrado. La <y> es consonante y nosotros una vocal
                # previa: uyi, uyu
                return False
            if FONEMAS[graf_multi_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                    FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_localizacion():
                # Somos <uii>, y como hay dos <i> seguidas, son vocales, y nosotros consonante. Compatible.
                return True
            if not graf_multi_post_post_post or not isinstance(graf_multi_post_post_post[0], GrafemaVocoide):
                # Somos <uiu> en posición final, o seguida de consonante <uiul>. Seremos vocal puesto que la <i> se
                # consonantiza. No compatible.
                return False  # uiu, uiul
            if FONEMAS[graf_multi_post_post_post[0].get_fonemas_ipa()[0]].get_abertura() != CERR:
                # Tras el <uiu> sigue una vocal fuerte: <uiuo>. La segunda <u> se consonantiza y nosotros también.
                return True
            if FONEMAS[graf_multi_post_post[0].get_fonemas_ipa()[0]].get_localizacion() ==\
                    FONEMAS[graf_multi_post_post_post[0].get_fonemas_ipa()[0]].get_localizacion():
                # Somos <uiuu>, con lo que las dos últimas <u> vocalizan, la <i> consonantiza y somos vocal.
                # No compatible
                return False
            return True  # ui-uy


class MonografoMudo(GrafemaMudo):
    u"""Esta subclase de GrafemaMudo es la clase padre para los grafemas mudos: <h>, <->, <">...

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class MonografoPausa(GrafemaPausa):
    u"""Esta subclase de GrafemaPausa es la clase padre para los grafemas de pausa: <.>, <¿>, <!>...

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class MonografoSimbolo(GrafemaSimbolo):
    u"""Esta subclase de GrafemaSimbolo es la clase padre para los grafemas de símbolo: <±>, <@>, <$>...

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class MonografoNumero(GrafemaNumero):
    u"""Esta subclase de GrafemaSimbolo es la clase padre para los grafemas numéricos: <0>, <2>, <7>...

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class MonografoOrdinal(GrafemaOrdinal):
    u"""Esta subclase de GrafemaOrdinal es la clase padre para los grafemas que indican ordinal: <º>, <ª>...

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de grafemas y su
    procesamiento. Está vacía.
    """
    pass


class DigrafoConsonante(Digrafo, GrafemaConsonante):
    def __init__(self, grafema_primario, grafema_secundario, fonemas_ipa, deletreo):
        u"""Constructor para la clase DigrafoConsonante

        :type grafema_primario: unicode
        :param grafema_primario: Un carácter que representa el grafema primario de este grafema
        :type grafema_secundario: unicode
        :param grafema_secundario: Un carácter que representa el grafema secundario (el 2º) de este grafema
        :type fonemas_ipa: [unicode]
        :param fonemas_ipa: los fonemas (caracter más diacríticos API) que expresa el grafema
        :type deletreo: unicode
        :param deletreo: indica con qué palabra(s) se lee el carácter aislado, para poder hacer deletreos.
        """
        Digrafo.__init__(self, grafema_primario, grafema_secundario, fonemas_ipa, deletreo)
