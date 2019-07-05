# -*- coding: utf-8 -*-
"""
Created on Mon May  6 10:30:44 2019

@author: Carmen
"""

import sympy as sy
import numpy as np
import random as ra
from . import elementos as Element 
from .circuito import Circuit
from copy import deepcopy

class SubCircuit(Element.Elements):
    """
    A class used to represent a set of subcircuits.
    
    Parameters
    ----------
    circuito: list
        It represents the inner circuit of the subcircuit
        
    v: list
        A list with initial values of the subcircuit.
        
    FT: list
        It determinates which are the input/output of the inner circuit.
        
    nl: boolean
        True if the inner circuit is non-linear. False, otherwise.
        
    differential: boolean
        True if the inner circuit has any capacitor/inductor.
        
    cir: dictionary
        The keys of the dictionary are the variables of the inner circuit,
        and the values are the solution of the circuit.
        
        
    Attributes
    ----------
    nl: boolean
        True if the inner circuit is non-linear. False, otherwise.
        
    circuito: list
        It represents the inner circuit of the subcircuit
        
        
    Methods
    -------
    setDiscrete():
        The input value determinates wheter the element equation is going to
        be linealized or not.
        
    getCir():
        It returns the solution of the inner circuit of a SubCircuit type 
        object.
    
    setCir(cir):
        It gets the solution of the inner circuit of a SubCircuit type object.
        
    setParamValues():
        This methods get values for linearization, and gets the equivalent 
        equation.
        
    setLinearEquations():
        It recalculates the equations.
        
    difElements():
        It reuturns a list of elements with differential values on its 
        equations.
        
    setIVk():
        It is a method for the application of the Euler method in capacitors, 
        and inductors.
    """
    
    def __init__(self, circuito, v, FT, nl=False, differential=False,  
                 cir=None):
        
        self.nl = nl
        self.circuito = circuito
        self.__differential = differential
        self.__v = v
        self.__FT = FT
        self.__cir = None
        self.__d1 = None
        self.__d2 = None
        self.__discrete = None
        
        a = len(self.__v)
        
        self.equation = [[[0 for i in range(a)],
                         [1 if i == j else 0 for i in range(a)],
                         [ra.randint(1, 11)]] for j in range(a)]
        
        if not nl:
            self.__d1 = [i[0] for i in self.__FT]
            d4 = [i for i in self.__FT]
            self.d3 = {}
            for i in range(len(self.__d1)):
                self.d3[self.__d1[i]] = self.circuito.index(d4[i])
        else:
            self.__d1 = [i for i in self.__v]
            
        self.__d2 = {}
        for i in range(len(self.__d1)):
            self.__d2[self.__d1[i]] = self.__FT[i]

        super().__init__(self.equation, nl=self.nl, subcir=True,
                         differential=self.__differential)

    def setDiscrete(self, dis):
        """
        The input value determinates wheter the element equation is going to
        be linealized or not.
        """
        self.__discrete = dis
        
        if dis:
            self.setParamValues()
        else:
            super().__init__(self.equation, nl=True)

    def getCir(self):
        """
        It returns the solution of the inner circuit of a SubCircuit type 
        object.
        """
        return self.__cir
    
    def setCir(self, cir):
        """
        It gets the solution of the inner circuit of a SubCircuit type object.
        
        Parameters
        ----------
        cir: dictionary
            The keys of the dictionary are the variables of the inner circuit
            and the values are the solutions of the circuit.
        """
        self.__cir = cir

    def setParamValues(self, v=None, i=None):
        """
        This methods get values for linearization, and gets the equivalent 
        equation.
        
        Parameters
        ----------
        v: list
            v is a list with the voltage values of the elements port.
            
        i: list
            i is a list with the current values of the elements port.
        """

        if v is None:
            v = self.__v
        else:
            self.__v = v

        self.__d1 = [i for i in self.__v]
            
        self.__d2 = {}
        for i in range(len(self.__d1)):
            self.__d2[self.__d1[i]] = self.__FT[i]

        self.d3 = {}
        for i in range(len(self.__d1)):
            self.d3[self.__d1[i]] = self.circuito.index(self.__d2[self.__d1[i]])

        circuito = self.circuito
        a = len(self.__d1)
        
        self.equation = [[[0 for i in range(a)],
                         [1 if i == j else 0 for i in range(a)],
                         [0]] for j in range(a)]
        
        for i in range(len(self.__d1)):
            self.__d2[self.__d1[i]][0].setEquation([[[1], [0], [self.__d1[i]]]])

        c = Circuit(circuito)
        c.solution()
        self.setCir(c)

        for i in range(len(self.__d1)):
            self.__d2[self.__d1[i]][0].setEquation([[[1], [0], [0]]])
            
        nol = []
        e = {}
        for i in range(len(circuito)):
            if circuito[i][0].getNL():
                nol.append(i)
                e[circuito[i][0]] = deepcopy(circuito[i][0].getEquation())
                circuito[i][0].setDiscrete(True)
                
        self.__lin0(self.__d1, self.__d2, self.d3, circuito)
        
        for i in nol:
            circuito[i][0].setEquation(e[circuito[i][0]])
            circuito[i][0].setDiscrete(False)

        if self.__discrete:
            self.circuito = circuito
            super().__init__(self.equation, nl=False)    
            
    def setLinearEquations(self):
        """
        This mehtod is only used for linear subcircuits. It is used to 
        when a inner circuit component has a capacitor/inductor type element, 
        that is: when those elements equations change, the equation must be
        recalculated.
        """
        # reservado para los elementos lineales. Esto se utilizara cuando
        # un subcircuito lineal tenga algun elemento dinamico. Si el elemento
        # dinamico cambia, es necesario recalcular la ecuacion del subcicuito.
        
        for i in range(len(self.circuito)):
            if self.circuito[i][0].getSubcir():
                self.circuito[i][0].setLinearEquations()
        if not self.nl:
            if type(self.__d1[0]) == Element.Resistance:
                self.equation = self.__lin2(self.circuito, self.__d1, self.__d2, self.d3)
            else:
                self.equation = self.__lin3(self.circuito, self.__d1, self.__d2, self.d3)
     
    # comprobado que esto funciona

    def __lin0(self, d1, d2, d3, circuito):
        self.equation = [[[0 for i in range(len(d1))],
                         [1 if i == j else 0 for i in range(len(d1))],
                         [0]] for j in range(len(d1))]
        
        c = Circuit(circuito)
        for i in range(len(d1)):
            self.equation[i][2][0] = -c.solution([d3[d1[i]]], [0], ["current"])

        for i in range(len(d1)):
            d2[d1[i]][0].setEquation([[[1], [0], [1]]])
            c = Circuit(circuito)
            for j in range(len(d1)):
                self.equation[j][0][i] = +self.equation[j][2][0]+c.solution([d3[d1[j]]], [0], ["current"])
            
            d2[d1[i]][0].setEquation([[[1], [0], [0]]])
        
        return self.equation

    # __lin2 he comprobado su funcionamiento y parece que esta bien (teoricamente)
    # tendria que comprobarlo en la practica. Se han hecho unas correcciones,
    # y se ha comprobado que su funcionamiento es correcto.

    def __lin2(self, circuito, d1, d2, d3):
        
        equation = [[[0 for i in range(len(d1))], [0 for i in range(len(d1))], [0]]
                    for i in range(len(d1))]
        
        R = []
        r = []
        for i in range(1, len(equation)+2):
            R.append(i)
            r.append(i)
        r.extend(r)
        m = []
        
        for i in range(len(R)):
            
            for j in range(len(d1)):
                d1[j].setEquation([[[1], [-R[j]], [0]]])
                c = Circuit(circuito)
                
            voltage = []
            current = []
            for j in d1:
                voltage.append(c.solution([d3[j]], [0], ["voltage"]))
                current.append(c.solution([d3[j]], [0], ["current"]))
            m.append([voltage, current])
            for j in range(len(R)):
                R[j] = r[j+i+1]

        for i in range(1, len(m)):
            for j in range(len(m[i][0])):
                m[i][0][j] = m[0][0][j]-m[i][0][j]
                m[i][1][j] = m[0][1][j]-m[i][1][j]
                
        a = [m[i][1] for i in range(1, len(m))]
        
        for i in range(0, len(m)-1):
            b = []
            for j in range(1, len(m)):
                b.append(m[j][0][i])
                
            A = np.array(a, dtype="float")
            B = np.array(b, dtype="float")
            y = np.linalg.solve(A, B)
            
            equation[i][2][0] = m[0][0][i]
            equation[i][0][i] = 1
            for j in range(len(y)):
                equation[i][1][j] = y[j]
                equation[i][2][0] -= y[j]*m[0][1][j]
            equation[i][2][0] = -equation[i][2][0]
        return equation

    def __lin3(self, circuito, d1, d2, d3):
        
        self.equation = [[[1 if i == j else 0 for i in range(len(d1))],
                        [0 for i in range(len(d1))],
                        [0]] for j in range(len(d1))]
        
        c = Circuit(circuito)
        for i in range(len(d1)):
            self.equation[i][2][0] = c.solution([d3[d1[i]]], [0], ["voltage"])
        for i in range(len(d1)):
            d1[i].setEquation([[[0], [1], [1]]])
            c = Circuit(circuito)
            for j in range(len(d1)):
                self.equation[j][1][i] = +self.equation[j][2][0]-c.solution([d3[d1[j]]], [0], ["voltage"])
            
            d1[i].setEquation([[[0], [1], [0]]])
        
        return self.equation

    def difElements(self):
        """
        It reuturns a list of elements with differential values on its 
        equations.
        """
        a = []
        for i in range(len(self.circuito)):
            e = self.circuito[i]
            if e[0].getDif() and e[0].getSubcir():
                a.extend(e[0].difElements())
            elif e[0].getDif():
                a.append(e)
        return a

    def setIVk(self, V=None, I=None):
        """
        It is a method for the application of the Euler method in capacitors, 
        and inductors.
        
        Parameters
        ----------
        V: list
            V contains the voltage solutions of the ports.
            
        I: list
            I contains the current solutions of the ports.
        """
        dim1 = []
        dim2 = []
        
        for i in range(len(self.circuito)):
            
            elemento = self.circuito[i]
            if elemento[0].getSubcir() and elemento[0].getDif() and  not elemento[0].getNL():
                
                dim1.append(i)
                
            elif elemento[0].getSubcir() and elemento[0].getDif() and elemento[0].getNL():
                elemento[0].setIVk()    
                
            elif elemento[0].getDif():
                dim2.append(i)
                
        for i in dim1:
            if not self.nl:
                for j in range(len(self.__d1)):
                    r = self.__d2[self.__d1[j]][0]
                    if type(self.__d1[0]) == Resistance:
                        r.setEquation([[[1], [-V[j]/I[j]], [0]]])
                        
                    else:
                        r.setEquation([[[0], [1], [I[j]]]])
                        
                self.setCir(Circuit(self.circuito))    
            # esta sentencia es tanto valida para los casos con circuito
            # principal lineal como no lineal.
            cir = self.getCir()
            
            I = [cir.solution([i], [j], ["current"]) for j in range(len(elemento)-1)]
            V = [cir.solution([i], [j], ["voltage"]) for j in range(len(elemento)-1)]
            elemento[0].setIVk(V, I)
            
            
        
        # caso de circuito principal lineal.
        if not self.nl:
            for i in range(len(self.__d1)):
                r = self.__d2[self.__d1[i]][0]
                if type(self.__d1[0]) == Resistance:
                    r.setEquation([[[1], [-V[i]/I[i]], [0]]])
                    
                else:
                    r.setEquation([[[0], [1], [I[i]]]])
                    
            self.setCir(Circuit(self.circuito))
            
            cir = self.getCir()
            
            for i in dim2:
                elemento = self.circuito[i]
                if elemento[0].getDifValue() == "v":
                    elemento[0].vk(cir.solution([i], [0], ["voltage"]))
                elif elemento[0].getDifValue() == "i":
                    elemento[0].ik(cir.solution([i], [0], ["current"]))
                    
            for i in range(len(self.__d1)):
                r = self.__d2[self.__d1[i]][0]
                if type(self.__d1[0]) == Resistance:
                    r.setEquation([[[1], [-V[i]/I[i]], [0]]])
                    
                else:
                    r.setEquation([[[0], [1], [0]]])
                    
        else:
            cir = self.getCir()
            for i in dim2:
                elemento = self.circuito[i]
                if elemento[0].getDifValue() == "v":
                    elemento[0].vk(cir.solution([i], [0], ["voltage"]))
                elif elemento[0].getDifValue() == "i":
                    elemento[0].ik(cir.solution([i], [0], ["current"]))
                    

"===============================OPAMP2========================================"
"""
No funciona
"""      
        
# class Opamp2(SubCircuit):
#    """
#    A class to represent a real Operational Amplifier.
#    """
#    def __init__(self):
#        Q1=Element.Q2N3904(v=[0, 0])
#        Q2=Element.Q2N3904(v=[0, 0])
#        Q3=Element.Q2N3904(v=[0, 0])
#        Q7=Element.Q2N3904(v=[0, 0])
#        Q8=Element.Q2N3904(v=[0, 0])
#        Q13=Element.Q2N3904(v=[0, 0])
#        Q12=Element.Q2N3904(v=[0, 0])
#        Q14=Element.Q2N3904(v=[0, 0])
#        Q17=Element.Q2N3904(v=[0, 0])
#        Q15=Element.Q2N3904(v=[0, 0])
#        Q16=Element.Q2N3904(v=[0, 0])
#        Q18=Element.Q2N3904(v=[0, 0])
#        Q20=Element.Q2N3904(v=[0, 0])
#        
#        Q6=Element.Q2N3906(v=[0, 0])
#        Q5=Element.Q2N3906(v=[0, 0])
#        Q4=Element.Q2N3906(v=[0, 0])
#        Q9=Element.Q2N3906(v=[0, 0])
#        Q10=Element.Q2N3906(v=[0, 0])
#        Q11=Element.Q2N3906(v=[0, 0])
#        Q19=Element.Q2N3906(v=[0, 0])
#        
#        R1=Element.Resistance(1e3)
#        R2=Element.Resistance(50e3)
#        R3=R1
#        R4=Element.Resistance(5e3)
#        R5=R2
#        R6=Element.Resistance(50)
#        R7=Element.Resistance(7.5e3)
#        R8=Element.Resistance(4.5e3)
#        R9=Element.Resistance(25)
#        R10=R6
#        
#        c=Element.Capacitor(60e-12)
#        
#        
#        
#        FT1=Element.VoltageSource(10)#Vcc+
#        FT2=Element.VoltageSource(-10)#Vcc-
#        FT3=Element.VoltageSource(1)#Vin+
#        FT4=Element.VoltageSource(-1)#Vin-
#        FT5=Element.VoltageSource(5)#Vout
#        
#        FT=[[FT1, [1, 0]], [FT2, [26, 0]], [FT3, [3, 0]], [FT4, [4, 0]],
#            [FT5, [5, 0]]]
#        
#        circuito=[[FT1, [1, 0]], [FT2, [26, 0]], [FT3, [3, 0]], [FT4, [4, 0]],
#                  [Q1, [2, 5], [2, 6]], [Q2, [3, 5], [3, 7]], 
#                  [Q3, [9, 1], [9, 11]], [Q4, [5, 5], [5, 1]], 
#                  [Q5, [8, 10], [8, 7]],
#                  [Q6, [8, 9], [8, 6]], [Q7, [11, 9], [11, 12]], 
#                  [Q8, [11, 10], [11, 14]], [Q9, [5, 15], [5, 1]], 
#                  [Q10, [18, 18], [18, 1]],
#                  [Q11, [18, 19], [18, 1]], [Q12, [17, 17], [17, 26]], 
#                  [Q13, [17, 15], [17, 16]], [Q14, [20, 19], [20, 21]],
#                  [Q15, [22, 21], [22, 23]], 
#                  [Q16, [7, 21], [7, 22]], [Q17, [23, 7], [23, 26]], 
#                  [Q18, [19, 1], [19, 24]], [Q19, [21, 26], [21, 25]], 
#                  [Q20, [24, 19], [24, 4]],
#                  [R1, [12, 26]], [R2, [13, 26]], [R3, [14, 26]], 
#                  [R4, [16, 26]], [R5, [22, 26]], [R6, [23, 26]], 
#                  [R7, [20, 21]],
#                  [R8, [20, 19]], [R9, [24, 4]], [R10, [4, 25]], 
#                  [c, [19, 7]], [FT5, [5, 0]]]
#        v=[10, -10, 0, 0, 0]
#        
#        super().__init__(circuito, v, FT, nl=True, differential=True)
        

"===============================OPAMP5========================================"
"""
Funciona.
"""


class Opamp5(SubCircuit):
    """
    This class represents a simplified Operational Amplifier.
    """
    def __init__(self):

        q1 = Element.Q2N3906(v=[-0.7, -0.7])
        q2 = Element.Q2N3906(v=[-0.7, -0.7])
        q8 = Element.Q2N3906(v=[-0.7, -0.7])
        
        q3 = Element.Q2N3904(v=[-0.7, -0.7])
        q4 = Element.Q2N3904(v=[-0.7, -0.7])
        q5 = Element.Q2N3904(v=[-0.7, -0.7])
        q6 = Element.Q2N3904(v=[-0.7, -0.7])
        q7 = Element.Q2N3904(v=[-0.7, -0.7])
        
        d1 = Element.D1N4002(2.68e-9)
        d2 = Element.D1N4002(2.68e-9)
        
        c = Element.Capacitor(60e-12)
        r = Element.Resistance(50e3)
        
        ia = Element.CurrentSource(19.51e-6)
        ic = Element.CurrentSource(3e-9)
        
        ft1 = Element.VoltageSource(0)
        ft2 = Element.VoltageSource(0)
        ft3 = Element.VoltageSource(10)
        ft4 = Element.VoltageSource(-10)
        ft5 = Element.VoltageSource(0)
        ft = Element.VoltageSource(0)
        
        self.circuito = [[q1, [2, 8], [2, 7]], [q2, [1, 6], [1, 7]],
                         [q3, [13, 8], [13, 4]], [q4, [13, 6], [13, 4]],
                         [ia, [3, 7]], [c, [6, 10]], [q5, [6, 3], [6, 9]],
                         [r, [9, 4]], [q6, [9, 10], [9, 4]], [d1, [11, 10]],
                         [d2, [12, 11]], [ic, [3, 12]], [q7, [12, 3], [12, 5]],
                         [q8, [10, 4], [10, 5]], [ft1, [1, 0]], [ft2, [2, 0]],
                         [ft3, [3, 0]], [ft4, [4, 0]], [ft, [8, 13]],
                         [ft5, [5, 0]]]

        ft = [[ft1, [1, 0]], [ft2, [2, 0]],
              [ft5, [5, 0]]]
        
        v = [0, -2, -2]
     
        super().__init__(self.circuito, v, ft, nl=True, differential=True)
