from problema_del_viajero import *

from heurispy.problema import Problema
from heurispy.heuristicas.busqueda_tabu import BusquedaTabu
from heurispy.framework import genera_lista_ejecuciones_heuristicas, inicia_exploracion_heuristica

if __name__ == '__main__':

    problema_optimizacion = Problema(generar_solucion_nueva, funcion_objetivo, vecindad)

    tabuBus = BusquedaTabu(problema_optimizacion, max_iteraciones=1000000)

    parametros_tabuBus = dict(espacio_memoria=[5000, 10000], max_busquedas_sin_mejora=[1000])

    lista_bloque_parametros_taboo = Framework.genera_lista_ejecuciones_heuristicas(parametros_tabuBus, 10)

	inicia_exploracion_heuristica(tabuBus, lista_bloque_parametros_taboo)



