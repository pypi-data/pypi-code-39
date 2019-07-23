#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Fonema y múltiples especializaciones de ella para representar los fonemas

La clase Fonema es la representación básica de un grafema. Los objetos de tipo Fonema tienen siempre
el atributo con el carácter IPA que lo representa. Otros atributos como la localización, la abertura,
modo y punto de articulación, sonoridad o duración, aparecen según la subclase de Fonema que se use.

También se incluyen otras 6 clases que son especializaciones de Fonema, que sirven de apoyo y facilitan
el procesado de los distintos tipos de fonema. La estructura de clases es la siguiente:
- Fonema:
    - FonemaConsonante
    - FonemaVocoide:
        - FonemaVocal
        - FonemaSemiconsonante
        - FonemaSemivocal
    - FonemaPausa
"""

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Fonema:
    u"""Esta clase representa la descripción básica de un fonema.

    Contiene la información sobre el símbolo IPA que define al fonema.

    Las especializaciones de esta clase añadirán más atributos.
    """
    def __init__(self, fonema_ipa=u''):
        u"""Constructor para la clase Fonema.

        :type fonema_ipa: unicode
        :param fonema_ipa: Un string con la representación IPA del fonema
        """
        self._fonema_ipa = fonema_ipa

    def get_fonema_ipa(self):
        u"""Devuelve el string con la representación en formato IPA del fonema.

        :rtype: unicode
        :return: La representación en formato IPA del fonema
        """
        return self._fonema_ipa

    def set_fonema_ipa(self, fonema_ipa):
        u"""Se establece el valor para la representación en formato IPA del fonema.

        :type fonema_ipa: unicode
        :param fonema_ipa: Un string con la representación IPA del fonema
        :return: None.
        """
        self._fonema_ipa = fonema_ipa


class FonemaVocoide(Fonema):
    u"""Clase que representa a los fonemas de vocoides (vocales y deslizantes)

    Hereda de la clase padre y añade el atributo sobre la localización del vocoide.
    """
    def __init__(self, fonema_ipa, localizacion):
        u"""Constructor para la clase FonemaVocoide.

        :type fonema_ipa: unicode
        :param fonema_ipa: Un string con la representación IPA del fonema
        :type localizacion: int
        :param localizacion: Un int con el código (ver graf_consts) que indica la localización.
        """
        Fonema.__init__(self, fonema_ipa)
        self._localizacion = localizacion

    def get_localizacion(self):
        u"""Devuelve el int con el código que indica la localización del vocoide (ver graf_consts).

        :rtype: int
        :return: El código (ver graf_consts) que indica la localización.
        """
        return self._localizacion


class FonemaVocal(FonemaVocoide):
    u"""Clase que representa a los fonemas de vocales

    Hereda de la clase padre y añade el atributo sobre la abertura de la vocal.
    """
    def __init__(self, fonema_ipa, localizacion, abertura):
        u"""Constructor para la clase FonemaVocal.

        :type fonema_ipa: unicode
        :param fonema_ipa: Un string con la representación IPA del fonema
        :type localizacion: int
        :param localizacion: Un int con el código (ver graf_consts) que indica la localización.
        :type abertura: int
        :param abertura: Un int con el código (ver graf_consts) que indica la abertura.
        """
        FonemaVocoide.__init__(self, fonema_ipa, localizacion)
        self._abertura = abertura

    def get_abertura(self):
        u"""Devuelve el int con el código que indica la abertura de la vocal (ver graf_consts).

        :rtype: int
        :return: El código (ver graf_consts) que indica la abertura.
        """
        return self._abertura


class FonemaSemivocal(FonemaVocoide):
    u"""Esta subclase de FonemaVocoide es la clase padre para fonemas semivocales.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de fonemas y su
    procesamiento. Está vacía.
    """
    pass


class FonemaSemiconsonante(FonemaVocoide):
    u"""Esta subclase de FonemaVocoide es la clase padre para fonemas semiconsonantes.

    Su existencia se debe a que la estructura de clases permite identificar fácilmente los tipos de fonemas y su
    procesamiento. Está vacía.
    """
    pass


class FonemaConsonante(Fonema):
    u"""Clase que representa a los fonemas de consonantes

    Hereda de la clase padre y añade los atributos sobre modo y punto de articulación, y sonoridad.
    """
    def __init__(self, fonema_ipa, mda, pda, sonoridad):
        u"""Constructor para la clase Fonema.

        :type fonema_ipa: unicode
        :param fonema_ipa: Un string con la representación IPA del fonema
        :type mda: int
        :param mda: Un int con el código (ver graf_consts) que indica el modo de articulación.
        :type pda: int
        :param pda: Un int con el código (ver graf_consts) que indica el punto de articulación.
        :type sonoridad: bool
        :param sonoridad: True para sonoras, False para sordas
        """
        Fonema.__init__(self, fonema_ipa)
        self._mda = mda
        self._pda = pda
        self._sonoridad = sonoridad

    def get_mda(self):
        u"""Devuelve el int con el código que indica el modo de articulación de la consonante (ver graf_consts).

        :rtype: int
        :return: El código (ver graf_consts) que indica el modo de articulación.
        """
        return self._mda

    def get_pda(self):
        u"""Devuelve el int con el código que indica el punto de articulación de la consonante (ver graf_consts).

        :rtype: int
        :return: El código (ver graf_consts) que indica el punto de articulación.
        """
        return self._pda

    def get_sonoridad(self):
        u"""Devuelve el bool con el valor de sonoridad de la consonante.

        :rtype: int
        :return: True si es sonora, False si es sorda
        """
        return self._sonoridad


class FonemaPausa(Fonema):
    u"""Clase que representa a los fonemas de pausa

    Hereda de la clase padre y añade el atributo de duración de la pausa.
    """
    def __init__(self, fonema_ipa, duracion):
        u"""Constructor para la clase Fonema.

        :type fonema_ipa: unicode
        :param fonema_ipa: Un string con la representación IPA del fonema
        :type duracion: int
        :param duracion: Un int con el código (ver graf_consts) que indica la duración.
        """
        Fonema.__init__(self, fonema_ipa)
        self._duracion = duracion

    def get_duracion(self):
        u"""Devuelve el int con el código que indica la duración de la pausa (ver graf_consts).

        :rtype: int
        :return: El código (ver graf_consts) que indica la duración.
        """
        return self._duracion
