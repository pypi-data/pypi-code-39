from problema_del_viajero import *

from heurispy.problema import Problema
from heurispy.heuristicas.recocido_simulado import RecocidoSimulado
from heurispy.framework import genera_lista_ejecuciones_heuristicas
from heurispy.framework import inicia_exploracion_heuristica

if __name__ == '__main__':

    problema_optimizacion = Problema(generar_solucion_nueva, funcion_objetivo, vecindad)

    recSim = RecocidoSimulado(problema_optimizacion, alpha=0.9, max_iteraciones=1000000)

    parametros_recSim = dict(temperatura=[1.0, 2.0], iteraciones_inyeccion_temperatura=[100, 1000],
                             maximo_inyecciones_temperatura=[5, 10])

    lista_bloque_parametros_simul = genera_lista_ejecuciones_heuristicas(parametros_recSim, 10)

    inicia_exploracion_heuristica(recSim, lista_bloque_parametros_simul)




