from heurispy import framework
import Problema
from Heuristicas.BusquedaTabu import BusquedaTabu

from problema_kilometros_vacios import *


if __name__ == '__main__':

    problema_kilometros = Problema.Problema(dominio=generar_solucion_nueva,
                                            funcion_objetivo=funcion_objetivo,
                                            funcion_variacion_soluciones=variar_solucion)

    tabuBus = BusquedaTabu(problema_kilometros, max_iteraciones=10000)

    parametros_tabuBus = dict(espacio_memoria=[50, 100, 150], max_busquedas_sin_mejora=[50, 100])

    lista_bloque_parametros_taboo = framework.genera_lista_ejecuciones_heuristicas(parametros_tabuBus, repeticiones=10)

    framework.inicia_exploracion_heuristica(tabuBus, lista_bloque_parametros_taboo)


