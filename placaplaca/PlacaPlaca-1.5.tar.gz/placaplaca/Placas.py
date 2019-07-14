import re
import os

os.system("cls")

def ShowPlaca(type):
    if (type!=""):
        print("\nLa placa pertenece a", type)
    else:
        print("\nPlaca irreconocida")

class Placa:

    def TypePlaca(self):
        placa=input("\nIngrese una placa: ")
        if re.match("^([A-Z]|[0-9]){6}$", placa):
            print("\nIngresaste una placa")
        
            if re.match("^MA([A-Z]|[0-9])+$", placa):
                type="una motocicleta"
            
            elif re.match("^MB[0-9]+", placa):
                type=("un MetroBus")
            
            elif re.match("^T([A-Z]|[0-9])+", placa):
                type=("un taxi")
            
            elif re.match("^E([A-Z]|[0-9])+", placa):
                type=("un vehiculo fiscal o judicial")
                
            elif re.match("^CP([A-Z]|[0-9])+", placa):
                type=("un vehiculo del canal")
            
            elif re.match("^B([A-Z]|[0-9])+$", placa):
                type=("un Bus")
            
            elif re.match("^HP([A-Z]|[0-9])+", placa):
                type=("un radioaficionado")
            
            elif re.match("^A[A-G]([A-Z]|[0-9])+$", placa):
                type=("un auto regular")
            
            elif re.match("^CC([A-Z]|[0-9])+$", placa):
                type=("un cuerpo consular")
            
            elif re.match("[0-9]+$", placa):
                type=("una serie antigua...")
            
            elif re.match("^PR([A-Z]|[0-9])+", placa):
                type=("un auto de prensa")
                
            else:
                type=("")
            ShowPlaca(type)
        else:
            print("Eso no es una placa")

placa=Placa()

if __name__=="__main__":
    placa.TypePlaca()