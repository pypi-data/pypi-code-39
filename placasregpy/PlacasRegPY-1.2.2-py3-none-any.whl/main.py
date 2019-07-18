import time                                                                         #Importamos el modulo "time" para pausar la ejecución del código unos segundos, para simular que se están procesando los datod introducidos
import re                                                                           #Importamos el modulo "re" para poder hacer uso del RegEx, que viene de Regular Expresions (Expresiones Regulares en español)
import Modulos as mod                                                               #Importamos el modulo llamado curiosamente "Modulos" y lo renombramos como mod, para no tener que escribir Modulos a cada rato, además de que noa ahorra un pocode tiempo al escribir

class Matricula:

    def TipoMatricula(self):
        placa = input("Introduzca un numero de matricula: ")                                #Introducción de datos por teclado

        n_placa = placa                                                                     #Aqui hacemos que la variable "n_placa" tenga el mismo valor de la variable "placa" para poder hacer un burn uso del numero de matricula mas adelante en el programa

        time.sleep(2.375)                                                                   #Aqui pausamos la ejecución del programa por 2.375 segundos

        if re.match('T[0-9]{5}$', placa):                                                   #A partir de esta línea(línea 11) empezamos a usar la variable "placa", para que el programa pueda hacer la comparación entre lo que introducimos por teclaado y las diferentes sentencias escritas en el programa
            print(mod.mensaje().format(n_placa), "Taxi.")                                   #Aqui usamos la variable "n_placa" para poder mostrarle en un mensaje al usuario mostrando los datos que introdujo el usuario(en este caso, el numero de matricula) por pantalla, además hacemos el uso de la función "mensaje()"
        elif re.match('B[0-9]{5}$', placa):
            print(mod.mensaje().format(n_placa), "Buses.")
        elif re.match('MB[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Metrobus.")
        elif re.match('PR[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Prensa")
        elif re.match('E[0-9]{5}$', placa):
            print(mod.mensaje().format(n_placa), "Jueces/Fiscales")
        elif re.match('CP[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Canal de Panama")
        elif re.match('HP[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Radioaficionado")
        elif re.match('CC[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Cuerpo Consular")
        elif re.match('6H[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Cuerpo Honorario")
        elif re.match('MI[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Mision Internacional")
        elif re.match('RI[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Ruta Interna")
        elif re.match('[A-C][A-Z][0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Vehiculos particulares")
        elif re.match('MA[0-9]{4}$', placa):
            print(mod.mensaje().format(n_placa), "Motos")
        elif re.match('[0-9]{6}$', placa):
            print(mod.mensaje().format(n_placa), "vehiculos normales(antes del 2013)")
        else:
            print(mod.error().format(n_placa))                                             #Aqui también usamos la variable "n_placa", esta vez usando la función "error()" que retorna un mensaje de error al introducir un número de matrícula no valido/incorrecto

mtr = Matricula()

if __name__ == "__main__":
    mtr.TipoMatricula()