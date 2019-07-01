#todo: Verificar que dominio, vecindad y funcion_objetivo reciban un método.
class Problema:

    """
    Esta clase se encarga del manejo de las funciones que el usuiaro defina para plantear su
    problema de optimización discreta.
    """

    def __init__(self, dominio, funcion_objetivo, funcion_variacion_soluciones):
        self.solucion_inicial = None
        self.dominio = dominio
        self.cambia_solucion = funcion_variacion_soluciones
        self.funcion_objetivo = funcion_objetivo

    def __getstate__(self):
        return self.__dict__

    def genera_solucion(self):
        self.solucion_inicial = self.dominio()

"""
def solucion():
    import numpy

    # Se crea una matriz de tamaño 5x5 con valores entradas 0 y 1, elegidas de forma aletoria.

    nueva_solucion = numpy.random.choice([0, 1], size=(5, 5))
    return nueva_solucion


def vecindad(solucion):
    import numpy

    nueva_solucion = numpy.copy(solucion)
    # Se eligen los índices de las entradas a cambiar de forma aleatoria

    x_1 = numpy.random.randint(5)
    y_1 = numpy.random.randint(5)
    x_2 = numpy.random.randint(5)
    y_2 = numpy.random.randint(5)
    valor_matriz_1 = solucion[x_1][y_1]
    valor_matriz_2 = solucion[x_2][y_2]

    # Si las dos entradas tienen el mismo valor, se vuelve a elegir aleatoriamente la segunda entrada

    while valor_matriz_1 == valor_matriz_2:
        x_2 = numpy.random.randint(5)
        y_2 = numpy.random.randint(5)
        valor_matriz_2 = solucion[x_2][y_2]

    # Se cambian las entradas correspondientes

    solucion[x_1][y_1] = valor_matriz_2
    solucion[x_2][y_2] = valor_matriz_1

    # Se regresa la solución con entradas cambiadas.

    return nueva_solucion


def funcion_objetivo(solucion):
    import numpy

    # Se multiplica la matriz de rutas con la solución y se regresa la suma del resultado.

    matriz_rutas = numpy.array([[1000, 1, 5, 8, 1000],
                                [2, 1000, 4, 1000, 1],
                                [1, 4, 1000, 3, 1],
                                [8, 1000, 1, 1000, 4],
                                [1000, 9, 2, 1, 1000]])
    return numpy.sum(numpy.multiply(matriz_rutas, solucion))

problema_prueba = Problema(solucion, funcion_objetivo, vecindad)

problema_prueba.genera_solucion()

x = problema_prueba.get_solucion()

print(x)

print("----------------------------------------------------------------------")

y = problema_prueba.vecindad(x)

print(y)

f = problema_prueba.funcion_objetivo(y)
"""