
"""
This script contains the Circuit class. It allows the user to save the 
parameters of the circuit, such as; elements and each nodes. Once the 
circuit is defined, the user can get tableau equations, voltage solution,
current solution....
"""


from .errors import InputError
from .graph import plotFunction
from . import elementos as Element
import numpy as np
import sympy as sy
import copy
import subprocess


s, t, h=sy.symbols("s t h")
print("hola")
p = subprocess.Popen('mkdir graphics & mkdir data', shell=True)

"==============================Circuit class=================================="


class Circuit(object):
    """
    A class used to represent a circuit.
     
    Parameters
    ----------
    circuit: list
        It is a list, with elements and lists, which represents a circuit.
        circuit parameter must have the following structure;
        [[r1, [0, 1]], [r2, [1, 2]], ..., [V, [n, 0]]]
        [r1, [0, 1]]-->r1 resistive element connected to 0 and 1 nodes.
        The current will pass from 0 node to 1.
        [r2, [1, 2]]-->r1 resistive element connected to 1 and 2 nodes.
        The current will pass from 1 node to 2.
        .
        .
        .

    Attributes
    ----------
    variables: list
        It is a list with circuit variables in a symbolic form.

    nl: boolean
        It determinates if the circuit is linear, or non-lineal, that it: if
        nl is True the circuit will be non-lineal, and if it False, lineal.

    Methods
    -------
    add(n):
        It adds a element/group of elements, defined by the input n,in the
        circuit attribute.

    reset(circuit):
        It erases the defined circuit attribute and introduces another one.

    get():
        when this method is called, the user will get the objectÂ´s circuit
        attribute value.

    getTableua():
        when this method is called, the user will get the matrix
        representation of the tableau equations.

    solution(position, port, variable, initcondition):
        It returns the solution of the circuit.

    dcAnalysis(position, ports, variable, dcelement, t0, t1, steps):
        It makes a graph which shows the change of a element variable, as
        a VoltageSource type element changes its value

    timeAnalysis(position, ports, variable, t0, t1, steps):
        It makes a graph which shows the change of a element variable, as
        the time change.

    theveninEquivalent(node1, node2):
        It returns the thevenin equivalent of the circuit.

    NortonEquivalent(node1, node2):
        It return the Norton equivalent of the circuit.


    Raises
    ------
    InputError:
        If the Circuit object initiate argument structure is not what supposed
        to be. The structure it must follow is described in the Parameters
        section.
        If the Circuit initiate argument does not meet the khirchoffs law
        criteria.

    Note
    ----
        Circuit 0 node represents ground.


    """

    "--------------------------__init__--------------------------------------"
     
    def __init__(self, circuit):
        self.__circuit = circuit
        self.__sol = None
        self.nl = False
        self.__tableaui = self.__tableauI()
        self.__tableauv = self.__tableauV()
        self.__tableaue = self.__tableauE()
        self.__tableaut = self.__tableauT()
        self.__variables = self.__Variables()
        self.__errorAnalysis()
        self.__vth = None
        self.__rth = None
        self.variables = self.__variables

    "--------------------------------add-------------------------------------"
     
    def add(self, n):
        """
        This method adds elements, with each respective node notation.
        The adding element must have the same structure as the
        initiate arguments; [[element1,[node1, node2], [node3, node4],... ],
        [element2, [node1Â´, node2Â´], [node3Â´, node4Â´],... ],...]

        Parameters
        ----------
        n: list

        """
        self.__circuit.extend(n)
        self.__errorAnalysis()

    "--------------------------------reset-----------------------------------"
      
    def reset(self, circuit=[]):
        """
        When reset method is called, the defined circuit attribute will be
        replaced by the input parameter. If there is no input parameter, then
        the circuit attribute will be defined by a default variable.

        Parameters
        ----------
        circuit: list
            It represents a circuit that will replaced the already defined
            circuit attribute.

        """
        self.__circuit = circuit
        self.nl = False
        self.__tableaui = self.__tableauI()
        self.__tableauv = self.__tableauV()
        self.__tableaue = self.__tableauE()
        self.__tableaut = self.__tableauT()
        self.__variables = self.__Variables()
        self.__errorAnalysis()
        self.__sol = self.solution()

    "---------------------------------get------------------------------------"
    
    def get(self):
        """
        It returns it's  circuit attribute.
        """
        return self.__circuit

    "--------------------------------copy------------------------------------"
     
    def copy(self):
        """
        It return a copy of this object.
        """
        return copy.deepcopy(self)

    "-----------------------------getTableau----------------------------------"
     
    def getTableau(self):
        """
        This method returns a tuple with two list. The first one holds tableu
        for currents, voltages, and tableau for elements. The second one has
        the values of the excited sources.

        Returns
        -------
        t, u: tuple
            t: list
            u: list
        """
        return self.__tableuat
                            
    "-----------------------------__tableauI1--------------------------------"
     
    def __tableauI1(self):

        # c sera una lista cuyos valores seran los nodos del circuito.
        c = []
        
        # En este caso ocurre un fenÃ³meno interesante; la notaciÃ³n es correcta
        # (aunque no lo parezca) porque, cuando se aplica c.extend(argumento)
        # este devolverÃ¡ la palabra reservada None, y por ende se crearÃ¡ una
        # lista con la siguiente forma [[None], [None],...,[None]]
        try:
            [[c.extend(puerta) for puerta in elemento[1::]] 
                for elemento in self.__circuit]
            
        except TypeError:
            raise InputError("wrong init argument.")
        
        # d es un diccionario cuyas claves se han creado mediante la lista c.
        # De ese modo se evita la repeticiÃ³n de nodos.
        d = dict.fromkeys(c)
        
        # variable c1: numero de puertas, y por ende numero de corrientes
        c1 = sum([len(elemento)-1 for elemento in self.__circuit])
        
        # con este for a cada clave se le estÃ¡ aÃ±adiendo una valor. El valor
        # sera una lista de dimension c1, completada con zeros.
        for nodo in d:
            d[nodo] = [0]*c1
            
        # variable c2: se usa para pasar de columna en columna de la matriz
        # tableauI, d.
        c2 = 0
        
        # Con las dos sentencias for, por un lado se irÃ¡n cogiendo los elementos
        # del circuito; la variable i da la posiciÃ³n del [elemento, puerta1,
        # puerta2...] dentro de self.__circuit. Por otro lado, con el segundo for
        # se irÃ¡n cogiendo las puertas del elementoi; la variable j da la
        # posiciÃ³n de las puerta que tiene el elementoi.

        for i in range(len(self.__circuit)):
            for j in range(1, len(self.__circuit[i])):
                try:
                    # con esta sentencia se selecciona el elemento.
                    elemento = self.__circuit[i][0]
                    
                    # con este if nos aseguramos de que la dimensiÃ³n de los
                    # puertos sea igual a dos
                    if len(self.__circuit[i][j]) != 2:
                        raise AttributeError
                        
                    # con estas dos sentencias se completa el diccionario d.
                    # teniendo en cuenta la forma en la que se ha completado, en el
                    # primer terminal de cualquier puerta entrarÃ¡ la corriente, y
                    # del del segundo saldrÃ¡.
                    d[self.__circuit[i][j][0]][c2] = elemento.current(0)
                    d[self.__circuit[i][j][1]][c2] = elemento.current(1)
                
                except (AttributeError, TypeError):
                    raise InputError("wrong init argument.")

                # sentencia necesaria para cambiar de columna en los valores del
                # diccionario d.
                c2 += 1
                
        if 0 in d.keys():
            self.__nonzero = False
        else:
            self.__nonzero = True
        return d

    "----------------------------__tableauI----------------------------------"
     
    def __tableauI(self):
        tableaui = self.__tableauI1()
        # coge el diccionario tableaui y sus valores los mete en la lista I.
        # se ha aplicado la funciÃ³n sorted() porque los keys de un diccionario
        # no tienen por que estar ordenados. Si no lo estuvieran, los resultados
        # finales estarian desordenados y por ende podria causar confusiones.
        return [tableaui[i] for i in sorted(tableaui.keys())]

    "-------------------------------tableauV---------------------------------"
     
    def __tableauV(self):
        d = self.__tableaui
        
        # mediante esta sentencia se crea la matriz transpuesta de tableauI.
        x = [[d[i][j] for i in range(len(d))] for j in range(len(d[0]))]
        
        return x

    "-------------------------------tableauE---------------------------------"
      
    def __tableauE(self):

        # e es una lista. Contiene las posiciones de los elementos no lineales
        # en el circuito.

        e = [i for i in range(len(self.__circuit)) if self.__circuit[i][0].getNL()]
        u = []
        j = 0
        for i in range(len(self.__circuit)):
            if self.__circuit[i][0].getNL():
                u.append(j)
                self.nl = True
            if self.__circuit[i][0].getDif() or self.__circuit[i][0].getTvariant():
                self.timedependent = True
            j += self.__circuit[i][0].nPorts()
            
        # se metera dentro del este bloque if, si hay algun elemento no lineal
        # en el circuito.
        if len(e) != 0:
            # dado que las ecuaciones no lineales de los elementos tienen una
            # dependencia de los voltajes (v0, v1,..., vn) y corrientes (i0, i1,
            # ..., in), donde vi e ii son los voltajes y corrientes del puerto i
            # del elemento, es necesario cambiar esos simbolos por el que les
            # corresponde en el circuito.
            q = 0
            for i in e:
                n = self.__circuit[i][0].nPorts()
                
                # i1 sera igual al conjunto de corrientes que aparecen en las
                # ecuaciones no lineales del elemento.
                i1 = sy.symbols("i0:%d" % n)

                # i2 sera igual al conjunto de corrientes que sustituiran los
                # valores i1 del elemento.
                i2 = sy.symbols("i%d:%d" % (u[q]+1, u[q]+n+1))

                # v1 sera igual al conjunto de corrientes que aparecen en las
                # ecuaciones no lineales del elemento.
                v1 = sy.symbols("v0:%d" % n)

                # v2 sera igual al conjunto de corrientes que sustituiran los
                # valores i1 del elemento.
                v2 = sy.symbols("v%d:%d" % (u[q]+1, u[q]+n+1))

                # t2 sera igual al conjunto de corrientes que sustituiran los
                # valores i1 del elemento. Estos simbolos se usarÃ¡n para que
                # no haya una perdida de informaciÃ³n.
                t2 = sy.symbols("t%d:%d" % (u[q]+1, u[q]+n+1))

                # u2 sera igual al conjunto de corrientes que sustituiran los
                # valores i1 del elemento.Estos simbolos se usarÃ¡n para que
                # no haya una perdida de informaciÃ³n.
                u2 = sy.symbols("u%d:%d" % (u[q]+1, u[q]+n+1))

                # estas listas serÃ¡n los argumentos de la funcion subs de sympy
                # para sustituir devidamente los simbolos.
                l1 = [(i1[l], t2[l]) for l in range(n)]
                l2 = [(v1[l], u2[l]) for l in range(n)]
                
                l3 = [(t2[l], i2[l]) for l in range(n)]
                l4 = [(u2[l], v2[l]) for l in range(n)]
                
                q += 1
                # mediante este conjunto de for se realizara la sustitucion.
                for j in range(n):
                    for m in range(3):
                        for k in range(n):
                            if m == 2 and k > 0:
                                continue
                            else:
                                f = self.__circuit[i][0].equation[j][m][k]
                                
                                if sy.sympify(f).is_real:
                                    continue
                                else:
                                    f = f.subs(l1).subs(l2).subs(l3).subs(l4)
                                    self.__circuit[i][0].equation[j][m][k] = f

        dim = sum([len(i)-1 for i in self.__circuit])
        
        # la lista u serÃ¡ una matriz con una unica fila con una dimensiÃ³n igual
        # a dim. Los casos no nulos  estarÃ¡n asociados a los valores de
        # excitaciÃ³n de las fuentes indep. En esta sentencia se instancia la
        # matriz u se instancia con valores nulos
        u = [0]*dim
        
        # la lista m sera una matriz de dimensiones dim x 2dim. Sus valores no
        # nulos se obtienen mediante las ecuaciones de los elementos. En esta
        # sentencia m se instanciara completamente con valores nulos. Las
        # columnas [0, dim-1] guardarÃ¡n la informaciÃ³n del voltaje, y las
        # [dim, 2dim-1] para las corrientes.
        m = [[0]*dim*2 for i in range(dim)]
        
        # apuntador1 y apuntador2 se encargargan de cambiar de fila y columna
        # respectivamente, en la matriz m. Estando con una ecuaciÃ³n especifica,
        # apuntador1 cambiara con el cambio de puerta, para asÃ­ coger los
        # voltajes y corrientes que aparecen en la ecuaciÃ³n. Una vez que se ha
        # cogido la informaciÃ³n puerta a puerta para cada ecuaciÃ³n, a apntador2
        # se le sumaran el numero de puertas del elemento, para que la
        # informaciÃ³n de dicho elemento no se solape con el del siguiente.
        apuntador1 = 0
        apuntador2 = 0
        
        # con este for se cogerÃ¡n, secuelcialmente y de forma ordenada, los
        # elementos del circuito. Con las caracteristicas de cada elemento,
        # como el numero de ecuaciones, el numero de puertas, y los valores
        # de corriente y voltaje se completara la matriz m.
        for i in range(len(self.__circuit)):
            elemento = self.__circuit[i][0]
            x = elemento.nEquations()
            for ecuacion in range(x):
                for puerta in range(0, len(self.__circuit[i])-1):
                    m[apuntador1][apuntador2+puerta] = elemento.voltageValue(ecuacion, puerta)
                    m[apuntador1][apuntador2+dim+puerta] = elemento.currentValue(ecuacion, puerta)
                    u[apuntador1] = elemento.uValue(ecuacion)[0]
                
                apuntador1 += 1
                
            apuntador2 += len(self.__circuit[i])-1
        return m, u 

    "-------------------------------__tableauT-------------------------------"
                       
    def __tableauT(self):
         
        if self.__nonzero:
            i = 0
        else:
            i = 1
             
        tI = self.__tableaui[i::]
        tV = [j[i::] for j in self.__tableauv]
        tE, tu = self.__tableaue
        dimtI = len(tI)
        dimtV = len(tV)
        dimt = 2*dimtV+dimtI
            
        # t contendra toda la informaciÃ³n del circuito, tableauI, tableauV, y
        # tableauE, con un orden especifico. En esta sentencia t se instanciara
        # como una lista de dimensiones dimt x dimt y, completamente compuesta
        # por valores nulos.
        t = [[0]*dimt for i in range(dimt)]
         
        # u contendra los valores de excitaciÃ³n de las fuentes. En esta
        # sentencia u se instanciara como una lista de dimension dimt y con
        # valores nulos.
        u = [0]*dimt
         
        # Mediante las dos sentencias for, y las condiciones if se le darÃ¡n los
        # correspondientes valores no nulos a m.
        for i in range(dimt):
            for j in range(dimt):
                if i < dimtI and j >= (dimtI+dimtV):
                    t[i][j] = tI[i][j-dimtI-dimtV]
                elif i >= dimtI and i < (dimtI+dimtV):
                    if j < dimtI:
                        t[i][j] = -1*tV[i-dimtI][j]
                    elif j >= dimtI and j < (dimtI+dimtV) and i == j:
                        t[i][j] = 1
                elif i >= (dimtI+dimtV) and j >= dimtI:
                    t[i][j] = tE[i-dimtI-dimtV][j-dimtI]
                    
            if i >= (dimtI+dimtV):
                u[i] = tu[i-dimtI-dimtV]
                
        return t, u

    "----------------------------__Variables---------------------------------"
    
    def __Variables(self):
         
        t1, t2 = self.__tableaut
         
        c = []
        
        # En este caso ocurre un fenÃ³meno interesante; la notaciÃ³n es correcta
        #(aunque no lo parezca) porque, cuando se aplica c.extend(argumento)
        # este devolverÃ¡ la palabra reservada None, y por ende se crearÃ¡ una
        # lista con la siguiente forma [[None], [None],...,[None]]
        [[c.extend(puerta) for puerta in elemento[1::]]
            for elemento in self.__circuit]
         
        dime = max(c)
        # con este valor se conseguira saber las dimensiones de las variables
        # e, v, i
        dim = int((len(t1)-dime)/2)
         
        # con estas sentencias se consigue una lista cuyo contenido es, las
        # variables e, v, i en forma simbolica. De este modo podremos indicar
        # a la funciÃ³n solve_linear_system_LU cuales son las variables
        # independientes del sistema.
        variables = [a for a in sy.symbols("e1:%d"%(dime+1))]
        for b in "vi":
            variables.extend([a for a in sy.symbols("%s1:%d"%(b, dim+1))])
             
        return variables

    "-----------------------------__solution---------------------------------"
 
    def __solution(self):
        t1, t2 = self.__tableaut
        # variables es una  lista cuyo contenido es, las variables e, v, i en
        # forma simbolica. De este modo podremos indicar a la funciÃ³n
        # solve_linear_system_LU cuales son las variables independientes del
        # sistema.
        variables = self.__variables

        # este bloque resuelve el sistema lineal de equaciones, haciendo
        # uso del modulo numpy.
        t1 = np.array(t1, dtype='float')
        t2 = np.array(t2, dtype='float')
        y = np.linalg.solve(t1, t2)
        x = {}
        for i in range(len(variables)):
            x[variables[i]] = y[i]
       
        return x
      
    "-------------------------__searchSymbol---------------------------------"
     
    def __searchSymbol(self, element, port, variable):
        if variable == "node1":
            i = element[port+1][0]
            a = sy.symbols("e%d" % i)
         
        elif variable == "node2":
            i = element[port+1][1]
            a = sy.symbols("e%d" % i)
             
        else:
            a = [i for i in range(len(self.__circuit)) if self.__circuit[i] == element]
            b = sum([len(self.__circuit[i])-1 for i in range(a[0])])
            i = b+port+1
            if variable == "current":
                a = sy.symbols("i%d" % i)
            elif variable == "voltage":
                a = sy.symbols("v%d" % i)
                 
        return a

    "-------------------------__systemE--------------------------------------"

    def __systemE(self):
        u, v = self.__tableaut
        variables = self.__variables
        f1 = []
        for i in range(len(u)):
            f = [u[i][j]*variables[j] for j in range(len(u[i]))]
            f = sum(f)
            f1.append(f-v[i])
        return f1

    "-------------------------solution---------------------------------------"
     
    def solution(self, position=None, port=None, variable=None, initcondition=None):
        """
        It returns a dictionary which keys are the circuit variables: $i_1$,
        $i_2$,..., $e_1$, $e_2$,... . The values of the keys are the solutions
        of the circuit.
         
        Parameters
        ----------
        position: list
            This parameter must contain integers which the position , from 0
            to the number of elements-1, of the wanted elements to be
            analysed.
             
        port: list
            Specify from which ports will bet get the variable information,
            respectively.
             
        variable: list
            The variable to be studied. There are four options; voltage,
            current, node1, node2. These variables are related to the Element
            type object.
             
        initcondition: dictionary
            A dictionary which keys are the circuit variables, and each values
            are the initial conditions.
        """
             
        variables = self.__variables
         
        # Cuando se instancia el objeto de la clase circuito, instantaneamente
        # ejecuta los la funciÃ³n solution() y asÃ­ se le da un calor a la
        # variable interna self.__sol. De ese modo se evita que cuando se
        # ejecute externamente la funciÃ³n solution() nuevamente se tenga que
        # resolver el los sistemas etc, pues se hace uso de la variable
         
        # Caso en el que la variable self.__sol ya tiene un valor, y unicamente
        # hay que devolverlo.
        if self.__sol is not None:
            x = self.__sol
        
        # Caso en el que la variable self.__sol no tiene un valor, y por ende
        # hay que calcularlo
        else:
             
            if self.nl:
                F = self.__systemE()
                 
                # diccionario con los elementos no lineales; los keys serán
                # las posiciones de los elementos no lineales en el circuito
                # y los values seran los propios elementos.
                n1 = {}
                for i in range(len(self.__circuit)):
                    e = self.__circuit[i][0]
                    if e.getNL():
                        n1[i] = copy.deepcopy(e)
                        
                try:
                    x = self.__NewtonRaphson1(F, variables, initcondition)
                    
                except np.linalg.LinAlgError:
                    x = None
                if x is None:
                    
                    for i in n1:
                        self.__circuit[i][0] = n1[i]
                        
                    circuito = copy.deepcopy(self.__circuit)

                    b, a, c = {}, {}, {}
                    for i in range(len(circuito)):
                        e = circuito[i][0]
                        te = type(e)
                        if te == Element.VoltageSource or te == Element.CurrentSource or te == Element.Capacitor:
                            b[i] = e.uValue(0)[0]
                            a[i] = 0
                            c[i] = b[i]/2
                            e.setuValue(0, c[i])
                    
                    condition = True
                    contador = 0
                     
                    while condition:
                        print(contador)
                        print(c)
                        n2 = {}
                        for i in n1:
                            e = copy.deepcopy(circuito[i][0])
                            n2[i] = e
                             
                        newcircuit = Circuit(circuito)
                        F = newcircuit.__systemE()
                        
                        try:
                            x = newcircuit.__NewtonRaphson1(F, variables, initcondition)
                            
                        except np.linalg.LinAlgError:
                            x = None

                        if x is not None:
                                 
                            n3 = {}
                            for i in n1:
                                 
                                e = copy.deepcopy(circuito[i][0])
                                n3[i] = e

                            for i in b:
                                circuito[i][0].setuValue(0, b[i])
                            newcircuit = Circuit(circuito)
                            F = newcircuit.__systemE()
                            
                            try:
                                x = newcircuit.__NewtonRaphson1(F, variables, initcondition)
                            except np.linalg.LinAlgError:
                                x = None
                            if x is not None:
                                condition = False
                                
                                for i in n1:
                                    self.__circuit[i][0] = circuito[i][0]
                            else:
                                for i in n1:
                                    circuito[i][0] = n3[i]
                                    
                                for i in c:
                                    a[i] = c[i]
                                    c[i] = (b[i]+c[i])/2

                        else:
                            for i in n1:
                                circuito[i][0] = n2[i]
                             
                            for i in c:
                                c[i] = (a[i]+c[i])/2
                                circuito[i][0].setuValue(0, c[i])
                              
                        contador += 1
                        if contador > 50:
                            if x is None:
                                print("No solution")
                            else:
                                print("last solution=", x[1])
                                print("precision=", x[0])
                                
                            raise RuntimeError("Number of iterations exceeded")

                if x[0] < 1e-3:
                    x0 = x[1]
                    x = x0
                else:
                    print("last solution=", x[1])
                    print("precision=", x[0])
                    raise RuntimeError()
                    
            # en el caso en el que el circuito sea lineal, se ejecuta la
            # funcion privada self.__solution(); funciÃ³n encargada de lograr
            # las soluciones de los sitemas de ecuaciones lineales.
            else:
                x = self.__solution()
        self.__sol = x
        # Esta if sirve para dar al usuario la solucion que desea. Hay dos
        # opciones.
        # Si el usuario quiere obtener todas las soluciones (todos los valores
        # e, v, y i del circuito).
        if position is None:
            return self.__sol
         
        # Si el usuario desea obtener los voltajes de los nodos del circuito
        # (e), las corrientes que atraves de un elemento (i), o las diferencias
        # de potencia que se crean atraves de las terminales de los elementos
        # (v).
        else:
            a = self.__searchSymbol(self.__circuit[position[0]], port[0], variable[0])
             
            return self.__sol[a]

    "---------------------NewtonRaphsonDiscrete------------------------------"
     
    def __NewtonRaphson1(self, F, variables, x0=None):
        
        # lista con las posiciones de los elementos no lineales en el cirucito.
        nol = []
        
        # lista con las posiciones de los elementos del tipo subcircuito.
        sub = []

        # diccionario cuyas keys seran los elementos no lineales del cirucito,
        # y los values seran una copia de la ecuacion REAL del elemento.
        # cuando el elemento no lineal se linealiza, pierde su ecuacion real,
        # por lo tanto cuando se consigue la solucion es necesario devolver
        # al elemento no lineal su ecuacion REAL. e sera un diccionario para
        # realizar dicha sustitucion.
        e = {}
        
        # instruccion para instanciar rellenar nol, sub, y e.
        for i in range(len(self.__circuit)):
            element = self.__circuit[i]
            
            if element[0].getNL():
                
                e[element[0]] = copy.deepcopy(element[0].getEquation())
                 
                element[0].setDiscrete(True)
                 
                nol.append(i)
                 
                if element[0].getCir() is not None:
                    sub.append(i)

        newcircuit = Circuit(self.__circuit)
        
        # s es una diccionario con las soluciones de newcircuit.
        s = newcircuit.solution()
        
        # f1 es una lista con los valores del sistema F(X), una vez
        # sustituidos los valores de X, esto es; f0=[f1(x1, x2, ..., xn),
        # f2(x1, x2, ..., xn), ..., fn(x1, x2, ..., xn)]. En este caso
        # xi=s[a].
        f1 = [f.subs([(a, s[a]) for a in variables]) for f in F]
         
        a = sy.sqrt(sum([f**2 for f in f1]))
        if a > 1e10:
            for i in nol:
                self.__circuit[i][0].setNL(True)
                self.__circuit[i][0].setEquation(e[self.__circuit[i][0]])
            return None
                 
        # Se comprueba si el valor de s es lo suficientemente exacto. Si lo es
        # el programa saldra del loop while y devolvera el valor de s. En caso
        # contrario, se volvera a instanciar un circuito con los nuevos valores
        # de linealizacion de los elementos no lineales. La variable contador 
        # determina el numero max de iteraciones.
        
        contador = 0
        while contador < 100:
            
            contador += 1
            print(a)
            if a < 1e-10 and len(sub) == 0:
                for i in nol:
                    self.__circuit[i][0].setNL(True)
                    self.__circuit[i][0].setEquation(e[self.__circuit[i][0]])
                return sy.sqrt(sum([f**2 for f in f1])), s

            for j in nol:
                element = self.__circuit[j]
                # se habilita la ecuacion equivalente discreta del elemento
                # no lineal. Dichas ecuaciones se instanciaran con unos
                # valores de defecto.

                # lista que se completara con los valores necesarios para
                # que las ecuciones equivalentes se creen correctamente.
                v = []
                i = []
                # con esta sentencia for se completa la lista v.
                for k in range(0, len(element)-1):

                    # NOTA: de momento en los elementos no lineales
                    # creados, unicamente es necesario el valor de los
                    # voltages para crear nuevamente las ecuaciones
                    # equivalentes.
                    v.append(newcircuit.solution([j], [k], ["voltage"]))
                    i.append(newcircuit.solution([j], [k], ["current"]))

                # se habilita la ecuacion discreta con los valores dados
                element[0].setParamValues(v, i)

            # se instancia un nuevo ciruicto, newcircuit, con la lista c.
            newcircuit = Circuit(self.__circuit)
             
            # s es una diccionario con las soluciones de newcircuit.
            s = newcircuit.solution()
            
            # comprobacion si el nuevo resultado es valido.
            f1 = [f.subs([(a, s[a]) for a in variables]) for f in F]
            b = sy.sqrt(sum([f**2 for f in f1]))
            print(b)
            if b > 1e10:
                for i in nol:
                    self.__circuit[i][0].setNL(True)
                    self.__circuit[i][0].setEquation(e[self.__circuit[i][0]])
                return None
                 
            # valor para el criterio de convergencia.
            c = abs(b-a)
            
            # En los casos de circuitos con subcircuitos, no se puede saber
            # usar el criterio de precision, y por lo tanto se opta por un
            # criterio de combergencia.
            if c < 1e-3 and len(sub) != 0:
                for j in nol:
                    self.__circuit[j][0].setNL(True)
                    self.__circuit[j][0].setEquation(e[self.__circuit[j][0]])
             
                return c, s
            
            # en los casos de circuitos sin subcircuitos, se puede dar el caso
            # en el que la precision deja de disminuir y la convergencia 
            # aumenta. Por lo tanto, se ha optado por devolver la precision
            # obtenida, y su valor se evaluara en la funcion solution
            elif c < 1e-11: 
                for j in nol:
                    self.__circuit[j][0].setNL(True)
                    self.__circuit[j][0].setEquation(e[self.__circuit[j][0]])
        
                return b, s

            a = b
            
        print("last solution=", s)
        print("precision=", a)
        raise RuntimeError("Number of iterations exceeded")

    "-------------------------timeAnalysis-----------------------------------"
     
    def timeAnalysis(self, position, ports, variable, t0, t1, steps):
        """
        This function allows the user to see a circuit variable change as the
        time changes.
         
        Parameters
        ----------
        position: list
            This parameter must contain integers which the position of the
            wanted elements to be analysed.
             
        ports: list
            Specify from which ports will bet get the variable information,
            respectively.
             
        variable: list
            the variable to be studied. There are four options; voltage,
            current, node1, node2. These variables are related to the Element
            type object.
             
        t0: float
            Time at which the analysis starts.
             
        t1: float
            Time at which the analysis finishes.
             
        steps: int
            number of steps from t0 to t1.
             
        Raises
        ------
        InputError
            If the element parameter is not in the circuit
             
        """

        elements = [self.__circuit[i] for i in position]
         
        v = self.__analysis(elements, ports, variable, t0, t1, steps)
         
        plotFunction(len(elements), "time", v)

    "-----------------------------dcAnalysis---------------------------------"
     
    def dcAnalysis(self, position, ports, variables, dcelement, v0, vi, steps):
        """
        This function allows the user to see a circuit variable change as the
        VoltageSource type element, defined with the input variavle dcelement
        value change from v0, to vi.
         
        Parameters
        ----------
        position: list
            This parameter must contain integers which the position of the
            wanted elements to be analysed.
             
        ports: list
            Specify from which ports will bet get the variable information,
            respectively.
             
        variables: list
            the variable to be studied. There are four options; voltage,
            current, node1, node2. These variables are related to the Element
            type object.
         
        dcelement: list
            It must be a VoltageSource Type element with each nodes
             
        v0: float
            Voltage at which the analysis starts.
             
        vi: float
            Voltage at which the analysis finishes.
             
        steps: int
            number of steps from v0 to vi.
        
        Notes
        -----
            It is possible to use this function in circuits with capacitors and
            inductor. The step size will be 1e-5. However, elements with t 
            dependency are not allowed.
        
        Raises
        ------
        InputError
            If the element parameter is not in the circuit
             
        """
        def substituteh(element, h):
             
            # mediante esta sentencia se obtiene la ecuacion del elemento.
            equation = element.getEquation()
            dim = len(equation)
            for j in range(dim):
                for k in range(dim):
                    for i in range(2):
                        try:
                            equation[j][i][k] = equation[j][i][k].subs(sy.symbols("h"), h)
                        except:
                            pass
                try:
                    equation[j][2] = equation[j][2].subs(sy.symbols("h"), h)
                except:
                    pass
           
        h = 1e-5
        m = (vi-v0)/steps
        newcircuit = []
        t = sy.symbols("t")
        for e in self.__circuit:
            if e[0].getTvariant():
                raise OSError
                 
            if e[0].getDif():
                if e[0].getSubcir():
                    for j in e[0].difElements():
                        substituteh(j[0], h)
                else:
                    substituteh(e[0], h)
            newcircuit.append(e)
            if e == dcelement:
                e[0].setTvariant()
                e[0].setEquation([[[1], [0], [m*t]]])
                 
        newc = Circuit(newcircuit)
        elements = [self.__circuit[i] for i in position]
        v = newc.__analysis(elements, ports, variables, v0, vi, steps)
         
        plotFunction(len(elements), "voltage", v)

    "---------------------------__analysis-----------------------------------"
     
    def __analysis(self, elements, ports, variable, t0, t1, steps):

        # con esta funcion se intenta sustituir el valor h de las ecuaciones
        # consitutivas del elemento en cuestion.
        def substituteh(element, h):
             
            # mediante esta sentencia se obtiene la ecuacion del elemento.
            equation = element.getEquation()
            dim = len(equation)
             
            # mediante este conjunto de sentencias for se analiza al completo
            #todas las componentes de las ecuaciones del elemento.
            # las sentencias try permiten usar el metodo subs, perteneciente al
            # modulo sympy, esto es; si la componente, en la que se quiere
            # sustituir h, no tiene ninguna h, el metodo subs darÃ¡ error. Dicho
            # erro serÃ¡ captura pÃ²r try-except.
            for j in range(dim):
                for k in range(dim):
                    for i in range(2):
                        try:
                            equation[j][i][k] = equation[j][i][k].subs(sy.symbols("h"), h)
                        except:
                            pass
                try:
                    equation[j][2] = equation[j][2].subs(sy.symbols("h"), h)
                except:
                    pass
                 
            # mediante la sentencia setEquation() se sustituye la ecuaciÃ³n de
            # defecto del elemento por la ecuaciÃ³n con los h ya sustituidos.
            print(equation)
            element.setEquation(equation)
         
        # con esta funcion se intenta sustituir el valor t de las ecuaciones
        # consitutivas del elemento en cuestion.
        # NOTA: el funcionamiento de este mÃ©todo es el mismo que en el caso de
        # substituteh(element, h)
        def substitutet(element, t):
            
            equation = element.getEquation()
            dim = len(equation)
            for j in range(dim):
                for k in range(dim):
                    for i in range(2):
                        try:
                            equation[j][i][k] = equation[j][i][k].subs(sy.symbols("t"), t)
                        except:
                            pass
                try:
                    equation[j][2][0] = equation[j][2][0].subs(sy.symbols("t"), t)
                except:
                    pass

            element.setEquation(equation)
             
        # con los inputs dados se define el valor de h.
        h = (t1-t0)/steps
        # setLinearEquations
        # se instancia la variable t. lista con todos los valores del tiempo
        # en los que se quiere calcular el voltage o corriente atraves del
        # elemento
        t = [t0+i*h for i in range(0, int(steps)+1)]
         
        # lista con las posiciones de los elementos, con alguna derivada en
        # sus ecuaciones, en el circuito.
        dif = []
         
        # lista con las posiciones de los elementos, con alguna dependencia
        # explicita del tiempo en sus ecuaciones, en el circuito.
        tv = []
         
        # lista de tuplas. El primer valor nos especificarÃ¡ la posiciÃ³n del
        # elemento en el input de entrada element. El segundo valor
        # especificarÃ¡ la posiciÃ³n del elemento en self.__circuit, del cual se
        # desea obtener la informaciÃ³n en funciÃ³n del tiempo.
        e = []
         
        # con este conjunto de sentencias for e if se se completa dif y tv.
        # Ademas el los casos en los que el elemento tenga alguna componente
        # diferencial, el elemento se someterÃ¡ a mÃ©todo substituteh() para
        # sustituir los valores de h de sus ecuaciones.
        for i in range(len(self.__circuit)):
            element1 = self.__circuit[i][0]
            if element1.getDif():
                dif.append(i)
                if not element1.getSubcir():
                    substituteh(element1, h)
                else:
                     
                    for j in element1.difElements():
                        substituteh(j[0], h)
                    element1.setLinearEquations()
            if element1.getTvariant():
                tv.append(self.__circuit[i][0])
             
            # e es un array de tuplas cuyos valores seran j (posicion del ele-
            # mento en el array del input) e i (posicion del elemento en el
            # circuito)
            for j in range(len(elements)):
                if self.__circuit[i] == elements[j]:
                    e.append((j, i))

        # lista que tendrÃ¡ las soluciones deseadas del elemento, a lo largo del
        # tiempo.
        s = dict.fromkeys(e)
        for i in e:
            s[i] = []
        newc = copy.deepcopy(self.__circuit)
        TV = []
         
        for i in range(len(self.__circuit)):
            if self.__circuit[i][0].getTvariant():
                TV.append(i)
                 
        for i in range(steps):
             
            print(i)
             
            for j in range(len(tv)):
                substitutet(newc[TV[j]][0], t[i])
                # substitutet(TV[j], t[i])
            # se instancia un objeto del tipo circuit con newc.
            c = Circuit(newc)
            # se obtiene la soluciÃ³n deseada.
            for j in range(len(e)):
                if i == 0:
                    m = "w"
                else:
                    m = "a"
                with open("data\\data%s.dat"%str(e[j][0]), m) as file:
                    try:
                        file.write(str(t[i+1])+" "+str(c.solution([e[j][1]], [ports[e[j][0]]], [variable[j]]))+"\n")
                    except OSError:
                        continue
                    
            newc = c.__circuit
            # con esta sentencia for se aplica el mÃtodo de euler.
            for j in dif:
                # En este conjunto de sentencias if, el caso en el que el
                #  elemento es no lineal, se descarta porque eso se realiza en
                # newtonraphson1.
                if newc[j][0].getCir() is None:
                    if newc[j][0].getDifValue() == "v":
                        newc[j][0].vk(c.solution([j], [0], ["voltage"]))
                    elif newc[j][0].getDifValue() == "i":
                        newc[j][0].ik(c.solution([j], [0], ["current"]))

                elif not newc[j][0].getNL():
                    v = []
                    c = []
                    for k in range(0, len(newc[j])-1):
                        v.append(c.solution([j], [k], ["voltage"]))
                        c.append(c.solution([j], [k], ["current"]))
                    newc[j][0].setIVk(v, c)
                    newc[j][0].setLinearEquations()
                 
                else:
                    newc[j][0].setIVk()
                    newc[j][0].setLinearEquations()

            for j in range(len(tv)):
                newc[TV[j]][0].setEquation(copy.deepcopy(tv[j].getEquation()))
            
        v = []
        for i in range(len(e)):
            v.append(str(self.__searchSymbol(elements[i], ports[e[i][0]], variable[i])))

        return v
         
    "---------------------------theveninEquivalent---------------------------"
     
    def theveninEquivalent(self, nodo1, nodo2):
        """
        It calculates the Thevenin equivalent of the circuit.
         
        Parameters
        ----------
        nodo1: int
            It is equivalent to the positive node, node+
             
        nodo2: int
            It is equivalent to the negative node, node-
             
             
        """
        # nodo1 == nodo+
        # nodo2 == nodo-
        m = [0, 0]
        for j in range(2):
            cs = Element.CurrentSource(j)
            c = []
            for i in self.__circuit:
                c.append(i)
            c.append([cs, [nodo1, nodo2]])
            newc = Circuit(c)
            m[j] = newc.solution([len(c)-1], [0], ["voltage"])
        rth = -(m[1]-m[0])
        vth = -m[0]
        self.__vth = vth
        self.__rth = rth
        return "vth=%s V, rth=%s ohm" % (str(vth), str(rth))

    "---------------------------nortonEquivalent-----------------------------"
    def nortonEquivalent(self, nodo1, nodo2):
        """
        It calculates the Norton equivalent of the circuit.
         
        Parameters
        ----------
        nodo1: int
            It is equivalent to the positive node, node+
             
        nodo2: int
            It is equivalent to the negative node, node-
             
        """
        self.theveninEquivalent(nodo1, nodo2)
        return "inor = %s A, rth = %s ohm" % (str(self.__vth/self.__rth), str(self.__rth))

    "----------------------------__errorAnalysis-----------------------------"
    
    def __errorAnalysis(self):
        """
        It uses tableauI and tableauV to check errors.
        """
        for i in self.__tableauv:
            if sum(i)!= 0:
                raise InputError("wrong circuit")
