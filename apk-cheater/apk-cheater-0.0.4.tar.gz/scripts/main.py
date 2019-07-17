import os
import re
import sys
import frida
import struct

def find_device(type):
    for device in frida.enumerate_devices():
        if device.type == type:
            return device
    return None

def run():
    device = find_device("usb")
    target_pid = device.get_process("Gadget").pid
    session = device.attach(target_pid)

    ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(ROOT_DIR, 'loader.js')) as f:
        data = f.read()
    script = session.create_script(data)
    script.load()

    def int2hex(value):
        hexed = list(struct.pack("<I", value).hex())

        size = len(hexed)
        for idx in range(size-2, 0, -2):
            hexed.insert(idx, " ")
        return "".join(hexed)

    def get_value():
        value = int(input("Enter the value: "))
        return int2hex(value)

    menus = [x for x in re.findall(r"\s*(.*):\s*function\(", data) if not x.startswith('on')]
    while True:
        show_help = ""
        for idx, name in enumerate(menus):
            show_help += "{:d}: {:s}\n".format(idx+1, name)
        show_help += "Enter > " 

        no = input(show_help)
        if not no:
            continue

        no = int(no)
        if not (0 < no and no <= len(menus)):
            print("Wrong number")
            continue

        c = menus[no-1]
        if c == 'scan':
            script.exports.scan(get_value())
        elif c == 'show':
            script.exports.show()
        elif c == 'next':
            script.exports.next(int(input("Next value:")))
        elif c == 'edit':
            script.exports.edit(int(input("Edit value:")))
        else:
            print("Please insert '{:s}' wrapper code to main.py".format(c))
            break

    session.detach()

if __name__ == '__main__':
    run()
