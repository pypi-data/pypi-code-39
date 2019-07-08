import subprocess
import time
from .sender import Sender
from .message_builder import CompleteMessageBuilder


class StatusManager:
    def __init__(self, expr_name, token, channel):
        self.complete_message_builder = CompleteMessageBuilder(expr_name)
        self.sender = Sender(token, channel)
        self.on_completed = lambda stdout, stderr: None

    def run_script(self, script):
        self.complete_message_builder.set_start_time(time.time())

        script_output = subprocess.Popen(script,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
        stdout, stderr = script_output.communicate()
        message = self.on_completed(stdout, stderr)

        self.complete_message_builder.set_end_time(time.time())

        blocks = self.complete_message_builder.create_message(message)
        self.sender.send(blocks)
