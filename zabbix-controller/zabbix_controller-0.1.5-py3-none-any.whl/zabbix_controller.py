import zabbix_controller

import sys
print(sys.argv)

def call_command():
    zabbix_controller.main()

if __name__ == "__main__":
    call_command()