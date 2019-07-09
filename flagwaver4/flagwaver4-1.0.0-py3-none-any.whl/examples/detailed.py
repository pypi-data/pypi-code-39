import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import flagwaver4

def run():
    serials = flagwaver4.arduino.serial_ports()
    #print(serials)
    if len(serials) > 0:
        flagwaver4.interface.initiate()
    else:
        print("Please connect your arduino and try again")

if __name__ == '__main__':
    run()