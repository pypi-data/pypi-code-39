import time
import paramiko
from PyQt5 import QtCore


class SerialThread(QtCore.QThread):
    """"""
    current_outputs_signal = QtCore.pyqtSignal(str)
    unreachable_hots_signal = QtCore.pyqtSignal(str)
    configured_hosts_signal = QtCore.pyqtSignal(str)

    def __init__(self, user_name, pass_word, commands, hosts_file, port=22,
                 connection_timeout=10, command_delay=2):

        super().__init__()
        self.user_name = user_name
        self.pass_word = pass_word
        self.commands = commands
        self.hosts_file = hosts_file
        self.port = port
        self.connection_timeout = connection_timeout
        self.command_delay = command_delay

    def send_command(self):
        """ """
        ssh = paramiko.SSHClient()

        for host in self.hosts_file:

            try:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=self.user_name,
                            password=self.pass_word, look_for_keys=False,
                            timeout=self.connection_timeout, port=self.port)

                print("Connected to {0}\n".format(host))
            except:
                self.unreachable_hots_signal.emit(host)
                print("Could not connect to {0}".format(host))
                ssh.close()
            else:
                channel = ssh.invoke_shell()
                for cmd in self.commands:

                    channel.send(cmd + "\n")
                    self.current_outputs_signal.emit(cmd)  # Send signal and data
                    time.sleep(self.command_delay)

                    output = channel.recv(99999)
                    time.sleep(self.command_delay)
                    self.current_outputs_signal.emit(output)  # Send signal and data

                    print(output)
                    print("#" * 120)
                self.configured_hosts_signal.emit(host)  # Send signal and data
                channel.close()
                ssh.close()

    def run(self):
        """ """
        self.send_command()

