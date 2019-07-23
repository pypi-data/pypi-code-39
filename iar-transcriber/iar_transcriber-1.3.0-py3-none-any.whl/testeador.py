#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""Proporciona la clase Testeador, que hace un test alofónico y ortográfico usando una serie de textos pretranscritos.

Tan solo contiene un único método, que realiza el testeo.
"""

from __future__ import print_function
from iar_transcriber.testeador_consts import TESTS_TRANSCRIPCION
from iar_transcriber.texto import Texto

__author__ = "Iván Arias Rodríguez"
__copyright__ = "Copyright 2017, Iván Arias Rodríguez"
__credits__ = [""]
__license__ = "GPL"  # No estoy seguro
__version__ = "1.0.1"
__maintainer__ = "Iván Arias Rodríguez"
__email__ = "ivan.arias.rodriguez@gmail.com"
__status__ = "Development"  # "Prototype", "Production"


class Testeador:
    u"""La clase Testeador hace un testeo a nivel de alófonos y grafemas, para asegurarse de que ciertos cambios en el
    código no introduzca errores en alguna otra parte.
    """

    def __init__(self):
        u"""Constructor para la clase Testeador.
        """
        pass

    @staticmethod
    def test():
        """Realiza un test de transcripción fonética y ortográfica e imprime los resultados

        Los textos se incluyen en testeador_consts.py y contienen unos fragmentos literarios (y algunos de prueba para
        combinaciones poco comunes) y sus transcripciones fonéticas. Para cada uno se hace un doble test:
        primero se comprueba que la transcripción fonética obtenida corresponda con la transcripción ya
        verificada que debería corresponder a ese texto, y además se comprueba que la transcripción ortográfica
        (hecha a partir de las estructuras de grafemas creadas) se corresponda con el texto de entrada.
        Como hay textos en los que se debe hacer una expansión ortográfica de algún símbolo o número, no es
        posible que la transcripción ortográfica coincida. En estos casos se marca el texto de test con un
        signo u'-' al inicio del texto.

        :return: None
        """
        # Realizamos un recuento de los fonemas y sílabas testeados
        estadisticas_segmentos = None
        estadisticas_silabas = None
        # Hay una serie de textos que nos sirven de test. Probamos todos
        for orden_test, test_transcripcion_fonologica in enumerate(TESTS_TRANSCRIPCION):
            txt = test_transcripcion_fonologica[0]
            print(u'Texto ' + str(orden_test) + u': (' + txt[:min(len(txt), 40)] + u'...).', end=' ')
            # Para hacer el test de transcripción ortográfica, no debemos resilabear ni nos hacen falta los alófonos
            texto = Texto(txt, resilabea=False, calcula_alofonos=False,
                          inserta_epentesis=True, organiza_grafemas=True)
            if txt[0] != u'-':  # Nuestra marca para saber que no hay que testear la transcripción ortográfica.
                transcripcion_ortografica_calculada = texto.\
                    transcribe_ortograficamente_texto(marca_tonica=False, separador=u'', apertura=u'', cierre=u'')
                if txt == transcripcion_ortografica_calculada:
                    print(u'Test ortográfico pasado.', end=' ')
                else:
                    print(u'TEST ORTOGRÁFICO FALLADO')
                    for orden, caracter in enumerate(txt):
                        if orden < len(transcripcion_ortografica_calculada) and\
                                transcripcion_ortografica_calculada[orden] != caracter:
                            print(u'\tError en posicion', orden,
                                u'(', caracter, u'->', transcripcion_ortografica_calculada[orden], u')')
                            print(u'\t\tANTES', txt[max(0, orden - 10):min(len(txt), orden + 10)])
                            print(u'\t\tAHORA',
                                transcripcion_ortografica_calculada[max(0, orden - 10):min(len(txt), orden + 10)])
                            break
                    else:
                        print(u'La nueva transcripción añade algo al final')
            else:
                print(u'Test ortográfico omitido.', end=' ')

            # Testeamos los alófonos: resilabeamos y calculamos alófonos
            texto.resilabea(calcula_alofonos=True)
            transcripcion_fonetica_calculada = texto.transcribe_foneticamente_texto()
            transcripcion_fonetica_modelo = test_transcripcion_fonologica[1]
            if transcripcion_fonetica_modelo == transcripcion_fonetica_calculada:
                print(u'Test de alófonos pasado.')
                estadisticas_segmentos, estadisticas_silabas = texto.\
                    get_estadisticas_segmentos_y_silabas(estadisticas_segmentos, estadisticas_silabas)
            else:
                print(u'TEST DE ALÓFONOS FALLADO.')
                # Indicamos dónde está el error, imprimiendo su entorno
                for orden, caracter in enumerate(transcripcion_fonetica_modelo):
                    if orden < len(transcripcion_fonetica_calculada) and\
                            transcripcion_fonetica_calculada[orden] != caracter:
                        print(u'\tError en posicion', orden, u'(', caracter, u'->',
                            transcripcion_fonetica_calculada[orden], u')')
                        print(u'\t\tANTES',
                            transcripcion_fonetica_modelo[max(0, orden - 15):
                                                          min(len(transcripcion_fonetica_modelo), orden + 15)])
                        print(u'\t\tAHORA',
                            transcripcion_fonetica_calculada[max(0, orden - 15):
                                                             min(len(transcripcion_fonetica_modelo), orden + 15)])
                        break
                else:
                    print(u'La nueva transcripción añade algo al final')

        print(estadisticas_segmentos["+len"], estadisticas_silabas["+len"])

if __name__ == "__main__":
    Testeador.test()
