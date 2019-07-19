import Framework
import Problema
from Heuristicas.BusquedaLocalterada import BusquedaLocalIterada
from problema_kilometros_vacios import *


if __name__ == '__main__':

    problema_kilometros = Problema.Problema(dominio=generar_solucion_nueva,
                                            funcion_objetivo=funcion_objetivo,
                                            funcion_variacion_soluciones=variar_solucion)

    localGuiadaIter = BusquedaLocalIterada(problema_kilometros, max_iteraciones=10000)

    parametros_locGui = dict(busqueda_local_sin_minimo_global=[10], rango_perturbacion=[4],
                             busqueda_iterada_sin_mejora=[100])

    lista_bloque_parametros_guiada = Framework.genera_lista_ejecuciones_heuristicas(parametros_locGui, repeticiones=1)

    Framework.inicia_exploracion_heuristica(localGuiadaIter, lista_bloque_parametros_guiada, nucleos_cpu=1)
