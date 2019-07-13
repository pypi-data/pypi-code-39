import eagle200_reader
import time
from requests.exceptions import (ConnectionError as ConnectError, HTTPError, Timeout)

try:
    testreader = eagle200_reader.EagleReader("10.0.20.207", "0093f6", "3251a7fee9b9d739")
except (ConnectError, HTTPError, Timeout, ValueError) as error:
    print("2")

try:
    data = testreader.update()
    while(True):
    #    print("Instantanous Demand:     {} kW".format(testreader.instantanous_demand()))
    #    print("Total Energy Delivered:  {} kWh".format(testreader.summation_delivered()))
    #    print("Total Energy Received:   {} kWh".format(testreader.summation_received()))
    #    print("Total Net Energy:        {} kWh".format(testreader.summation_total()))
        data = testreader.update()
        for a in data:
            print(data[a])
        time.sleep(10)
except (ConnectError, HTTPError, Timeout, ValueError) as error:
    print("3")



