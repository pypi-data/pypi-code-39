from queue import Queue
from threading import Thread
from code_domain_emissary.emissary import Emissary

class Extractor:

    def __init__(self, q):
        self._input_q = q
        self._transcribe_thread = Thread(target=self._watch_q)
        self._transcribe_thread.setDaemon(True)
        self._run = False
        self.code_emissary = Emissary()
        self.output_q = Queue()

    def observe(self):
        self._run = True
        self._transcribe_thread.start()

    def ignore(self):
        self._run = False

    def _watch_q(self):
        while self._run:
            text = self._input_q.get(True)
            # send to NLP and respond with processed intents
            result = self.code_emissary.process(text)
            self.output_q.put(result)
            # print(result)
