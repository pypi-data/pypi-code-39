import random
msgs = ["Wire", "LED", "Resistor", "Ping Sensor", "Speaker", "Button", "Buzzer", "Motor"]


def part():
    mainmsg = random.choice(msgs)
    print(mainmsg)