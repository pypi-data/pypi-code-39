# -*- coding: utf-8 -*-

# Created on Fri Oct  5 09:45:49 2018

# Subject: TFG Ingenieria Electronica

# Topic: class wich represents a circuit

# @author: Carmen


from .circuito import Circuit
import sympy as sy
import math as m
import numpy as np
import copy

s, h, t = sy.symbols("s h t")
vc = sy.symbols("vc")
pi = m.acos(-1)
"================================Elements====================================="


class Elements(object):
    """
    A class used to represent a set of electric elements.
    
    Parameters
    ----------
    equation: list
        The representation of the constitutive equations of the element.
    
    
    Attributes
    ----------
    equation: list
        The representation of the constitutive equations of the element.
        
        
    Methods
    -------
    current(terminal):
        It returns the way in which goes the current in the terminal, input
        value.
        
    nEquations():
        It returns the number of constitutive equations of the element. 
        
    nPorts():
        It returns the number of ports of the element.
        
    VoltageValue(equation, port):
        It takes a equation, specified by the input parameter, of the 
        constitutive equations and it will return the value that is within the
        specified port voltage.
        
    CurrentValue(equation, port):
        It takes a equation, specified by the input parameter, of the 
        constitutive equations and it will return the value that is within the
        specified port current.
        
    UValue(equation):
        It takes a equation, specified by the input parameter, of the 
        constitutive equations and it will return the u value.
        
    setEquation(equation):
        It changes the element equation with the input argument.
        
    getEquation():
        It return the element equation.
    
    setuValue(equation, value):
        The u value of the equation is changed with the value input.
    
    getDif():
        It determinates if the equation has any differentiation.
    
    getDifValue():
        It specifies which variable, v or i, has been differentiate.
    
    getNL():
        It specifies whether the element is non-linear, or not.
    
    setNL(value):
        It allows the user to specify the element non-linearity.
    
    getTvariant():
        It determinates wheter the element has a time dependency.
    
    setTvariant(value=True):
        This method allows the user to determinate whether the elements is
        timer variant or not.
        
    getSubcir(value):
        It allows the user to determinate whether the element is a sub-circuit
        or not.
        
    getDiscret():
        It determinates whether the element equation has beenlinearized.
    
    getCir():
        It returns the solution of the inner circuit of a SubCircuit type 
        object.
    
    setCir(cir):
        It gets the solution of the inner circuit of a SubCircuit type object
    """
    
    def __init__(self, equation=[], differential=False, difValue=None,
                 nl=False, tvariant=False, subcir=False):
        
        self.nl = nl
        self.equation = equation
        self.__differential = differential
        self.__difValue = difValue
        self.__tvariant = tvariant
        self.__subcir = subcir
        self.__cir = None
        self.__discrete = True

    def setEquation(self, equation):
        """
        It changes the element equation with the input argument.
        
        Parameter
        ---------
        equation: list
            A representation of the constitutive equation with lists.
        """
        self.equation = equation
        
    def getEquation(self):
        """
        It return the element equation.
        """
        
        return self.equation
        
    def current(self, terminal):
        """
        It returns the way in which goes the current in the terminal, input
        value.
        
        Parameters
        ----------
        terminal: int
            The number of the terminal. It will take 0 or 1 value.
            
        Returns
        -------
        int
            1 if the terminal number is 0, -1 otherwise.
        
        """
        if terminal == 0:
            return 1
        return -1
    
    def nEquations(self):
        """
        It returns the number of constitutive equations of the element.
        
        Returns
        -------
        int
            number of constitutive equations of the element.
        """
        return len(self.equation)
    
    def nPorts(self):
        """
        It returns the number of ports of the element.
        
        Returns
        -------
        int
            number of ports of the element.
        """
        return len(self.equation[0][0])
    
    def voltageValue(self, equation, port):
        """
        It takes a equation, specified by the input parameter, of the 
        constitutive equations and it will return the value that is within the
        specified port voltage.
        
        Parameters
        ----------
        equation: int
            It is a number that specifies the equation that the user wants to 
            take from the set of constitutive equations.
        port: int
            It is a number that specifies the port from which the user wats to
            get voltage information.
            
        Returns
        -------
        float
            The parameter value multiplying with the voltage variable, 
            specified by equation and port input parameters.
        
        """
        return self.equation[equation][0][port]
    
    def currentValue(self, equation, port):
        """
        It takes a equation, specified by the input parameter, of the 
        constitutive equations and it will return the value that is within the
        specified port current.
        
        Parameters
        ----------
        equation: int
            It is a number that specifies the equation that the user wants to 
            take from the set of constitutive equations.
        port: int
            It is a number that specifies the port from which the user wats to
            get current information.
            
        Returns
        -------
        float
            The parameter value multiplying with the current variable, 
            specified by equation and port input parameters.
        """
        return self.equation[equation][1][port]
    
    def uValue(self, equation):
        """
        It takes a equation, specified by the input parameter, of the 
        constitutive equations and it will return the u value.
        
        Parameters
        ----------
        equation: int
        It is a number that specifies the equation that the user wants to 
        take from the set of constitutive equations.
            
        Returns
        -------
        float
            The u value of the equation.
        """
        return self.equation[equation][2]

    def setuValue(self, equation, value):
        """
        The u value of the equation is changed with the value input.
        
        Parameters
        ----------
        equation: int
            It is a number that specifies the equation that the user want to 
            take to change each u value
            
        value: float
            It is a float number, and it will replace the u value of the 
            specified equation
        """
        self.equation[equation][2][0] = value
    
    def getDif(self):
        """
        It determinates if the equation has any differentiation.
        
        Returns
        ------
        boolean
            True if the equation has any differentiation. False, otherwise
        """
        return self.__differential
    
    def getDifValue(self):
        """
        It specifies which variable, v or i, has been differentiate.
        """
        return self.__difValue
    
    def getNL(self):
        """
        It specifies whether the element is non-linear, or not.
        """
        return self.nl
    
    def setNL(self, value):
        """
        It allows the user to specify the element non-linearity.
        
        Parameters
        ----------
        value: boolean
            True to became non-linear. False, to linear.
        """
        self.nl = value
    
    def getTvariant(self):
        """
        It determinates whether the element has a time dependency.
        """
        return self.__tvariant
    
    def setTvariant(self, value=True):
        """
        This method allows the user to determinate wheter the elements is
        timer variant or not.
        
        Parameters
        ----------
        value: boolean
            True to time variant element. False, otherwise.
        """
        self.__tvariant = value
        
    def getSubcir(self):
        """
        This method determinates wheter the element is a SubCircuit type 
        objetc
        """
        return self.__subcir
    
    def setSubcir(self, value=True):
        """
        It allows the user to determinate whether the element is a sub-circuit
        or not.
        
        Parameters
        ----------
            value: boolean
                True to sub-circuits. False, otherwise
        """
        self.__subcir = value
    
    def getDiscrete(self):
        """
        It determinates whether the element equation has been linearized.
        """
        return self.__discrete
    
    def getCir(self):
        """
        It returns the solution of the inner circuit of a SubCircuit type 
        object.
        """
        return self.__cir
    
    def setCir(self, cir):
        """
        It gets the solution of the inner circuit of a SubCircuit type object
        
        Parameters
        ----------
            cir: dictionary
                the keys are equal to the circuit variables, and the dictionary 
                values are the solution of the circuit.
        """
        self.__cir = cir


"-------------------------------Resistance------------------------------------"


class Resistance(Elements):
    """
    A class used to represent a resistance.
    
    Parameters
    ----------
    value: float
        The value of the resistance.
        
    Attributes
    ----------    
    equation: list
        The representation of the resistance constitutive equation.
        
    """
    
    def __init__(self, value):
        self.equation = [[[1], [-value], [0]]]
        super().__init__(self.equation)
        

"-----------------------------VoltageSource-----------------------------------"


class VoltageSource(Elements):
    """
    A class used to represent a voltage source.
    
    Parameters
    ----------
    value: float
        The excitation value of the source.
        
    Attributes
    ----------
    equation: list
        The representation of the voltage source constitutive equation.
    """
    def __init__(self, value):
        self.equation = [[[1], [0], [value]]]
        super().__init__(self.equation)


"-----------------------------ACVoltageSource---------------------------------"


class ACVoltageSource(Elements):
    """
    A class used to represent a AC voltage source.
    
    
    Parameters
    ----------
    value: float
        The amplitude of the AC voltage source..
        
    frequency: float
        The frequency of the AC voltage source.
        
    phase: float
        The phase of the AC voltage source
        
    Attributes
    ----------
    equation: list
        The representation of the voltage source constitutive equation.
    """
    def __init__(self, value, frequency, phase=0):
        
        self.equation = [[[1], [0], [value*sy.sin(frequency*2*pi*t + phase)]]]
        super().__init__(self.equation, tvariant=True)
        
        
"-----------------------------CurrentSource-----------------------------------"


class CurrentSource(Elements):
    """
    A class used to represent a current source.
    
    Parameters
    ----------
    value: float
        The impedance value of the resistance.
        
    Attributes
    ----------   
    equation: list
        The representation of the current source constitutive equation.
        
    """
    def __init__(self, value):
        self.value = value
        self.equation = [[[0], [1], [self.value]]]
        super().__init__(self.equation)
 

"-----------------------------ACCurrentSource---------------------------------"


class ACCurrentSource(Elements):
    """
    A class used to represent a AC voltage source.
    
    Parameters
    ----------
    value: float
        The amplitude of the AC current source..
        
    frequency: float
        The frequency of the AC current source.
        
    phase: float
        The phase of the AC current source
        
    Attributes
    ----------
    equation: list
        The representation of the voltage source constitutive equation.
    """
    def __init__(self, value, frequency, phase=0):
        self.value = value
        self.equation = [[[0], [1], [value*sy.sin(frequency*2*pi*t + phase)]]]
        super().__init__(self.equation, tvariant=True)
        

"--------------------------------Capacitor------------------------------------"


class Capacitor(Elements):
    """
    A class used to represent a capacitor.
    
    Parameters
    ----------
    value: float
        The capacitance value of the capacitor.

    v0: float
        Determinates the voltage value across the capacitor  when t=0.
        
    Attributes
    ----------   
    equation: list
        The representation of the capacitor constitutive equation.
        
    """
    def __init__(self, value, v0=0.0):
        self.equation = [[[1], [-h/value], [v0]]]
        super().__init__(self.equation, differential=True, difValue="v")
        
    def vk(self, value):
        self.equation[0][2][0] = value
        super().setEquation(self.equation)


"--------------------------------Inductor------------------------------------"


class Inductor(Elements):
    """
    A class used to represent a inductor.
    
    Parameters
    ----------
    value: float
        The inductance value of the inductor.

    i0: float
        Determinates the current value across the inductor  when t=0.
        
    Attributes
    ----------   
    equation: list
        The representation of the capacitor constitutive equation.       
    """
    def __init__(self, value, i0=0):
        self.equation = [[[-h/value], [1], [i0]]]
        super().__init__(self.equation, differential=True, difValue="i")
        
    def ik(self, value):
        self.equation[0][2][0] = value
        super().setEquation(self.equation)
        

"---------------------------------Diode---------------------------------------"


class D1N4002(Elements):
    """
    A class used to represent a diode.
    
    Parameters
    ----------
    
    Attributes
    ----------
    equation: list
        The representation of a diode constitutive equation.
    
    v: list
        It is a list with the initial values.
    """
    def __init__(self, i0=14.11e-9, v=[0.4], i=[1e-3]):
        self.__v = v
        self.v = self.__v
        self.__i0 = i0
        self.__vt = 8.6173324e-5*298
        vt = self.__vt
        v0 = sy.symbols("v0")
        self.__discrete = False
        self.equation = [[[-i0*(sy.exp(v0/vt)-1)/v0], [1], [0]]]
        super().__init__(self.equation, nl=True)

    def setDiscrete(self, dis):
        """
        The input value determinates wheter the element equation is going to
        be linealized or not.
        
        Parameters
        ----------
            dis: boolean
                True to make the equation linear. False, otherwise.
        """
        self.__discrete = dis
        
        if self.__discrete:
            self.setParamValues(self.__v)
        else:
            super().__init__(self.equation, nl=True)
            
    def getDiscrete(self):
        """
        This method return True when the equation has been linealized.
        """
        return self.__discrete
        
    def setParamValues(self, v=None, i=None):
        """
        To linearization a set of values are needed. So, this method takes 
        each input arguments, and it uses to make the linealization and change 
        the equation.
        
        Parameters
        ----------
            v: list
                v is a list with the voltage values of the elements port.
            
            i: list
                i is a list with the current values of the elements port
        """
        
        if v is None:
            v = self.__v
        else:
            self.__v = v
            
        self.v = v
        v0 = v[0]
        print(v)
        
        g = self.__i0*sy.exp(v0/self.__vt)/self.__vt
        i = self.__i0*(sy.exp(v0/self.__vt)-1)-self.__i0*sy.exp(v0/self.__vt)*v0/self.__vt
        
        if self.__discrete:
            super().__init__([[[-g], [1], [i]]], nl=False)
                

"------------------------------TransistorQ2N2222------------------------------"


class Q2N2222(Elements):
    """
    A class used to represent a NPN transistor.
    
    Parameters
    ----------
    
    Attributes
    ----------
    equation: list
        The representation of the NPN transistor constitutive equation.
        
    """
    def __init__(self, ics=3.307157571149511e-15, ies=1.1403e-15, 
                 ar=0.8602961925565159, af=0.9943, v=[-0.7, -0.7], i=[1e-3, 1e-3]):
        
        v0, v1 = sy.symbols("v0 v1")
        
        # las siguientes constantes son constantes para definir las ecuaciones
        # constitutivas del diodo Q2N222.

        self.__vt = 8.6173324e-5*298
        self.__v = v
        self.v = self.__v
        self.__ics = ics
        self.__ies = ies
        self.__ar = ar
        self.__af = af
        
        vt = self.__vt
        ics = self.__ics
        ies = self.__ies
        ar = self.__ar
        af = self.__af

        # v1=vbe=vb-ve, v0=vbc=vb-vc
        # ic=af*ies*(sy.exp((v1)/vt)-1)-ics*(sy.exp((v0)/vt)-1)
        # ie=-ies*(sy.exp((v1)/vt)-1)+ar*ics*(sy.exp((v0)/vt)-1)
        
        self.equation = [[[-ics*sy.exp(v0/vt)/v0, af*ies*sy.exp(v1/vt)/v1], [1, 0], [af*ies-ics]],
                         [[ar*ics*sy.exp(v0/vt)/v0, -ies*sy.exp(v1/vt)/v1], [0, 1], [-ies+ar*ics]]]
        
        self.__discrete = False
        super().__init__(self.equation, nl=True)

    def setDiscrete(self, dis):
        """
        The input value determinates wheter the element equation is going to
        be linealized or not.
        
        Parameters
        ----------
            dis: boolean
                True to make the equation linear. False, otherwise.
        """
        self.__discrete = dis
        
        if self.__discrete:
            self.setParamValues(self.__v)
        else:
            super().__init__(self.equation, nl=True) 
            
    def getDiscrete(self):
        """
        This method return True when the equation has been linealized.
        """
        return self.__discrete
        
    def setParamValues(self, v=None, i=None):
        """
        To linearization a set of values are needed. So, this method takes 
        each input arguments, and it uses to make the linealization and change 
        the equation.
        
        Parameters
        ----------
            v: list
                v is a list with the voltage values of the elements port.
            
            i: list
                i is a list with the current values of the elements port
        """
        if v is None:
            v = self.__v
        else:
            self.__v = v
            
        v0 = v[0]
        v1 = v[1]
        
        g1 = self.__ies*sy.exp(v1/self.__vt)/self.__vt
        i1 = self.__ies*(sy.exp(v1/self.__vt)-1)-self.__ies*sy.exp(v1/self.__vt)*v1/self.__vt
        g2 = self.__ics*sy.exp(v0/self.__vt)/self.__vt
        i2 = self.__ics*(sy.exp(v0/self.__vt)-1)-self.__ics*sy.exp(v0/self.__vt)*v0/self.__vt

        if self.__discrete:
            super().__init__([[[g2, -g1*self.__af], [-1, 0], [self.__af*i1-i2]],
                              [[-self.__ar*g2, +g1], [0, -1], [self.__ar*i2-i1]]], nl=False)


"------------------------------TransistorQ2N3904------------------------------"


class Q2N3904(Elements):
    """
    A class used to represent a NPN transistor.
    
    Parameters
    ----------
    
    Attributes
    ----------
    equation: list
        The representation of the NPN transistor constitutive equation.
    """
    def __init__(self, ics=5.135668043523316e-15, ies=6.734423e-15, 
                 ar=0.42749, af=0.9976, v=[-0.7, -0.7], i=[1e-3, 1e-3]):
        
        v0, v1 = sy.symbols("v0 v1")
        
        # las siguientes constantes son constantes para definir las ecuaciones
        # constitutivas del diodo Q2N222.

        self.__v = v
        self.v = self.__v
        self.__vt = 8.6173324e-5*298
        self.__ics = ics
        self.__ies = ies
        self.__ar = ar
        self.__af = af
        
        vt = self.__vt
        ics = self.__ics
        ies = self.__ies
        ar = self.__ar
        af = self.__af
        
        # v1=vbe=vb-ve, v0=vbc=vb-vc
        # ic=af*ies*(sy.exp((v1)/vt)-1)-ics*(sy.exp((v0)/vt)-1)
        # ie=-ies*(sy.exp((v1)/vt)-1)+ar*ics*(sy.exp((v0)/vt)-1)
        
        self.equation = [[[-ics*sy.exp(v0/vt)/v0, af*ies*sy.exp(v1/vt)/v1], [1, 0], [af*ies-ics]],
                         [[ar*ics*sy.exp(v0/vt)/v0, -ies*sy.exp(v1/vt)/v1], [0, 1], [-ies+ar*ics]]]
        
        self.__discrete = False
        super().__init__(self.equation, nl=True)

    def setDiscrete(self, dis):
        """
        The input value determinates wheter the element equation is going to
        be linealized or not.
        
        Parameters
        ----------
            dis: boolean
                True to make the equation linear. False, otherwise.
        """
        self.__discrete = dis
        
        if self.__discrete:
            self.setParamValues(self.__v)
            
        else:
            super().__init__(self.equation, nl=True) 
            
    def getDiscrete(self):
        """
        This method return True when the equation has been linealized.
        """
        return self.__discrete
        
    def setParamValues(self, v=None, i=None):
        """
        To linearization a set of values are needed. So, this method takes 
        each input arguments, and it uses to make the linealization and change 
        the equation.
        
        Parameters
        ----------
            v: list
                v is a list with the voltage values of the elements port.
            
            i: list
                i is a list with the current values of the elements port
        """
        if v is None:
            v = self.__v
        else:
            self.__v = v
            
        self.v = v
        v0 = v[0]
        v1 = v[1]
        
        g1 = self.__ies*sy.exp(v1/self.__vt)/self.__vt
        i1 = self.__ies*(sy.exp(v1/self.__vt)-1)-self.__ies*sy.exp(v1/self.__vt)*v1/self.__vt
        g2 = self.__ics*sy.exp(v0/self.__vt)/self.__vt
        i2 = self.__ics*(sy.exp(v0/self.__vt)-1)-self.__ics*sy.exp(v0/self.__vt)*v0/self.__vt

        if self.__discrete:
            super().__init__([[[g2, -g1*self.__af], [-1, 0], [self.__af*i1-i2]],
                              [[-self.__ar*g2, +g1], [0, -1], [self.__ar*i2-i1]]], nl=False)
            

"------------------------------TransistorQ2N3906------------------------------"


class Q2N3906(Elements):
    """
    A class used to represent a NPN transistor.
    
    Parameters
    ----------
    
    Attributes
    ----------
    equation: list
        The representation of the NPN transistor constitutive equation.
    """
    def __init__(self, ies=1.1537553902975205e-15, ics=1.3908311155608809e-15, 
                 ar=0.8278688524590164, af=0.994, v=[-0.7, -0.7], i=[-1e-4, -1e-4]):
        
        v0, v1 = sy.symbols("v0 v1")
        self.__v = v
        self.v = self.__v
        self.__vt = 8.6173324e-5*298
        self.__ics = ics
        self.__ies = ies
        self.__ar = ar
        self.__af = af
        
        vt = self.__vt
        ics = self.__ics
        ies = self.__ies
        ar = self.__ar
        af = self.__af
        
        # v1=vbe=vb-ve, v0=vbc=vb-vc
        # ic=af*ies*(sy.exp((v1)/vt)-1)-ics*(sy.exp((v0)/vt)-1)
        # ie=-ies*(sy.exp((v1)/vt)-1)+ar*ics*(sy.exp((v0)/vt)-1)
        
        self.equation=[[[ics*sy.exp(-v0/vt)/v0, -af*ies*sy.exp(-v1/vt)/v1], [1, 0], [-af*ies+ics]],
                       [[-ar*ics*sy.exp(-v0/vt)/v0, ies*sy.exp(-v1/vt)/v1], [0, 1], [+ies-ar*ics]]]

        self.__discrete = False
        super().__init__(self.equation, nl=True)

    def setDiscrete(self, dis):
        """
        The input value determinates wheter the element equation is going to
        be linealized or not.
        
        Parameters
        ----------
            dis: boolean
                True to make the equation linear. False, otherwise.
        """
        self.__discrete = dis
        
        if dis:
            self.setParamValues(self.__v)
            
        else:
            super().__init__(self.equation, nl=True)
            
    def getDiscrete(self):
        """
        This method return True when the equation has been linealized.
        """
        return self.__discrete
        
    def setParamValues(self, v=None, i=None):
        """
        To linearization a set of values are needed. So, this method takes 
        each input arguments, and it uses to make the linealization and change 
        the equation.
        
        Parameters
        ----------
            v: list
                v is a list with the voltage values of the elements port.
            
            i: list
                i is a list with the current values of the elements port
        """
        if v is None:
            v = self.__v
        else:
            self.__v = v
            self.v = v

        v0 = v[0]
        v1 = v[1]
        g1 = self.__ies*sy.exp(-v1/self.__vt)/self.__vt
        i1 = self.__ies*(sy.exp(-v1/self.__vt)-1)+self.__ies*sy.exp(-v1/self.__vt)*v1/self.__vt
        g2 = self.__ics*sy.exp(-v0/self.__vt)/self.__vt
        i2 = self.__ics*(sy.exp(-v0/self.__vt)-1)+self.__ics*sy.exp(-v0/self.__vt)*v0/self.__vt

        if self.__discrete:
            super().__init__([[[-g2, g1*self.__af], [1, 0], [self.__af*i1-i2]],
                              [[self.__ar*g2, -g1], [0, 1], [self.__ar*i2-i1]]], nl=False)


"----------------------------CurrentControlled--------------------------------"


class CurrentControlled(Elements):
    """
    A class used to represent a current controlled element.
            
    Parameters
    ----------
    r11: float
        The impedance value of the first port when the second port 
        current is 0 A, open port.
        
    r12: float
        The impedance value of the first port when the first port 
        current is 0 A.
        
    r21: float
        The impedance value of the second port when the second port 
        current is 0 A.
        
    r22: float
        The impedance value of the second port when the first port 
        current is 0 A.
    
    Attributes
    ----------    
    equation: list
        The representation of the current controlled constitutive equation.
    """
    def __init__(self, r11, r12, r21, r22):
        self.equation = [[[1, 0], [-r11, -r12], [0]], [[0, 1], [-r21, -r22], [0]]]
        super().__init__(self.equation)
        

"----------------------------VoltageControlled--------------------------------" 


class VoltageControlled(Elements):
    """
    A class used to represent a voltage controlled element.
    
    Parameters
    ----------
    g11: float
        The admittance of the first port when the second portÂ´s voltage is
        0 V.
        
    g12: float
        The admittance of the first port when the first portÂ´s voltage is
        0 V.
        
    g21: float
        The admittance of the second port when the second portÂ´s voltage is
        0 V.
        
    g22: float
        The admittance of the second port when the first portÂ´s voltage is
        0 V.
     
    Attributes
    ----------
    equation: list
        The representation of the voltage controlled constitutive equation.
        
    """
    def __init__(self, g11, g12, g21, g22):
        self.equation = [[[-g11, -g12], [1, 0], [0]], [[-g21, -g22], [0, 1], [0]]]
        super().__init__(self.equation)
        

"--------------------------------Hybrid1--------------------------------------" 


class Hybrid1(Elements):
    """
    A class used to represent Hybrid circuit.
    
    Parameters
    ----------
    h11: float
        The impedance value of the first port when the second port voltage
        is 0 V.
        
    h12: float
        The relation between the first and second port voltages when the 
        first portÂ´s current is 0 A.
        
    h21: float
        The relation between the first and second por currents when the 
        second portÂ´s voltage is 0 V.
        
    h22: float
        The admittance value of the second port when the first port current
        is 0 A.
     
    Attributes
    ----------    
    equation: list
        The representation of the Hybrid1 constitutive equation.
        
    """
    def __init__(self, h11, h12, h21, h22):
        self.equation = [[[1, -h12], [-h11, 0], [0]], [[0, -h22], [-h21, 1], [0]]]
        super().__init__(self.equation)  
        

"--------------------------------Hybrid2--------------------------------------"


class Hybrid2(Elements):
    """
    A class used to represent a inverse Hybrid circuit.
    
    Parameters
    ----------
    h11: float
        The admittance value of the first port when the second port current
        is 0 A.
        
    h12: float
        The relation between the first and second port current when 
        the first portÂ´s voltage is 0 V.
        
    h21: float
        The relation between the second and first port voltage when the
        second port current is 0 A.
        
    h22: float
        The admittance value of the second port when the second port current
        is 0 A.
    
    Attributes
    ----------    
    equation: list
        The representation of the inverse Hybrid constitutive equation.
    """
    def __init__(self, h11, h12, h21, h22):
        self.equation = [[[-h11, 0], [1, -h12], [0]], [[-h21, 1], [0, -h22], [0]]]
        super().__init__(self.equation)
        

"-----------------------------Transmission1-----------------------------------"


class Transmission1(Elements):
    """
    A class used to represent a two port network.
    
    Parameters
    ----------
    t11: float
        The relation between the first and the second port voltages values
        when the second port current value is 0 A.
        
    t12: float
        The impedance of the first port when the second port current flows
        in the opposite direction and its portÂ´s voltage is 0 V.
        
    t21: float
        The admitance of the first port when the second port current is 
        0 A.
        
    t22: float
        The relation between the firs and second port currents when the 
        second portÂ´s currents flows in the opposite way and the itÂ´s 
        voltage value is 0 V.
     
    Attributes
    ----------
    equation: list
        The representation of the transmission constitutive equation.
    """
    def __init__(self, t11, t12, t21, t22):
        self.equation = [[[1, -t12], [t11, 0], [0]], [[0, -t21], [1, -t22], [0]]]
        super().__init__(self.equation) 
        

"-----------------------------Transmission2-----------------------------------" 


class Transmission2(Elements):
    """
    A class used to represent a two port network with inverse transmission 
    parameters.
    
    Parameters
    ----------
    t11: float
        The relation between the second and first port voltages when the first
        port current value is 0 A.
        
    t12: float
        The second port impedance value when the first port voltage is 0 V.
        
    t21: float
        The second port admittance value when the first port current is 0 A.
        
    t22: float
        The relation between the second and first port currents when first
        port voltage is 0 V.
     
    Attributes
    ----------
    equation: list
        The representation of the inverse transmission constitutive 
        equation.
    """
    def __init__(self, t11, t12, t21, t22):
        self.equation = [[[-t12, 1], [-t11, 0], [0]], [[-t21, 0], [-t22, 1], [0]]]
        super().__init__(self.equation)


"-----------------------------------CCVS--------------------------------------"


class CCVS(CurrentControlled):
    """
    A class used to represent a current controlled voltage source element.
    
    Parameters
    ----------
    r: float
        The impedance value of the voltage source controlled by a current.
    """
    def __init__(self, r):
        self.r = r
        super().__init__(0, r, 0, 0)

        
"-----------------------------------VCCS--------------------------------------"


class VCCS(VoltageControlled):
    """
    A class used to represent a voltage controlled current source element.
    
    Parameters
    ----------
    g: float
        The admittance value of the current source controlled by a voltage.
    """
    def __init__(self, g):
        self.g = g
        super().__init__(0, g, 0, 0)
        

"--------------------------------Gyrator--------------------------------------"


class Gyrator(VoltageControlled):
    """
    A class used to represent a gyrator.
    
    Parameters
    ----------
    g: float
        The admittance value of the gyrator
    """
    def __init__(self, g):
        self.g = g
        super().__init__(0, g, -g, 0)


"-----------------------------------VCVS--------------------------------------"


class VCVS(Hybrid1):
    """
    A class used to represent a voltage controlled voltafe souce.
    
    Parameters
    ----------
    u: float
        The relation between the first and second port voltages when the 
        first portÂ´s current is 0 A.
    """
    def __init__(self, u):
        self.u = u
        super().__init__(0, u, 0, 0) 
        

"----------------------------Transformer--------------------------------------"


class Transformer(Hybrid1):
    """
    A class used to represent a transformer.
    
    Parameters
    ----------
        n: float
            The numbers of turns in a winding.
    """
    def __init__(self, n):
        self.n = n
        super().__init__(0, n, -n, 0) 
        

"-----------------------------------CCCS--------------------------------------"


class CCCS(Hybrid2):
    """
    A class used to represent a current controlled current source.
    
    Parameters
    ----------
        u: float
            The relation between the first and second port current when 
            the first portÂ´s voltage is 0 V. 
    """
    def __init__(self, u):
        self.u = u
        super().__init__(0, u, 0, 0)
