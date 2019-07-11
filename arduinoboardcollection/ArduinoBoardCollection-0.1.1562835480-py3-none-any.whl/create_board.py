import os
import time


def create_board(path,name,superboard="ArduinoBasicBoard"):
    camelcase = ''.join(x for x in name.title() if not x.isspace())
    snakename= name.lower().replace(' ', '_')
    os.makedirs(os.path.join(path,snakename),exist_ok=True)
    if os.path.exists(os.path.join(path,snakename,"board.py")):
        raise ValueError(name + "already exists as board: " + str(os.path.join(path,snakename)))

    with open(os.path.join(path,snakename,"board.py"),"w+") as f:
        code=""
        if superboard == "ArduinoBasicBoard":
            code+="from arduino_controller.basicboard.board import ArduinoBasicBoard\n"

        code+="from arduino_controller.basicboard.arduino_data import ArduinoData\n"
        code+="from arduino_controller.arduino_variable import arduio_variable\n"

        #boardclass
        code+="\n\nclass "+camelcase+"("+superboard+"):\n"
        code+="\tFIRMWARE = "+str(time.time()).replace(".","")+"\n"


        code+="\n\tdef __init__(self):\n"
        code+="\t\tsuper().__init__()\n"
        code+="\t\tself.inocreator.add_creator("+camelcase+"ArduinoData)\n"

        #arduino_data
        code+="\n\nclass "+camelcase+"ArduinoData(ArduinoData):\n"
        code+="\n\tdef definitions(self):  # name:value\n\t\treturn {}\n"
        code+="\n\tdef global_vars(self):  # name:[type,defaultvalue]  array possible: \"array[ARRAYSIZE]\": [\"uint8_t\", None]\n\t\treturn {}\n"
        code+="\n\tdef includes(self):  # [\"<Package.h\"]\n\t\treturn []\n"
        code+="\n\tdef functions(self):  # name:[returntype,[(argtype,argname),...], stringcode] \n\t\treturn {}\n"
        code+="\n\tdef setup(self):  # stringcode\n\t\treturn \"\"\n"
        code+="\n\tdef loop(self):  # stringcode\n\t\treturn \"\"\n"
        code+="\n\tdef dataloop(self):  # stringcode\n\t\treturn \"\"\n"

    # end
        code += "\n\nif __name__ == '__main__':\n"
        code += "\tins = "+camelcase+"()\n"
        code += "\tins.create_ino()\n"
        f.write(code.replace("\t","    "))


if __name__ == "__main__":
    create_board(path=os.path.join(os.path.dirname(__file__),"boards","test"),name="Testboard "+str(int(time.time())))