import queue
import threading

import speech_recognition as sr
import os

STRATEGY_MAP = {
    "sphinx": "recognize_sphinx",
    "bing": "recognize_bing",
    "google": "recognize_google",
    "google_cloud": "recognize_google_cloud",
    "houndify": "recognize_houndify",
    "ibm": "recognize_ibm",
    "wit": "recognize_wit"
}

STRATEGY_LIST = ('sphinx', 'bing', 'google', 'google_cloud', 'houndify', 'ibm', 'wit')


class Listener:

    def __init__(self, strategy="google", credentials=None):
        self._available_strategies = STRATEGY_LIST
        self._set_strategy(strategy)
        self._credentials = credentials
        self._run = False
        self._spoken_q = queue.Queue()
        self.output_q = queue.Queue()
        try:
            self.mic = sr.Microphone()
        except AttributeError:
            raise AttributeError("You'll need to install PyAudio first: https://people.csail.mit.edu/hubert/pyaudio/")

    def _set_strategy(self, chosen_strategy):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        try:
            strategy = STRATEGY_MAP[chosen_strategy]
            self.transcribe = self.recognizer.__getattribute__(strategy)
        except KeyError:
            raise KeyError("You'll need to select an available strategy: {}.  Note that the default is `google`.".format(self._available_strategies))

    def _activate(self):
        try:
            assert self.mic is not None
            with self.mic as source:
                sounds = self.recognizer.listen(source)
                self._spoken_q.put(sounds)
            while self._run:
                self._activate()
        except AssertionError:
            raise NameError("Could not find a suitable microphone.")

    def _parse(self):
        while self._run:
            audio_input = self._spoken_q.get(True)
            try:
                speech_text = self.transcribe(audio_input)
                self.output_q.put(speech_text)
            except sr.UnknownValueError:
                self._notify_error("There was a problem", "Could not process your speech into text")

    def _notify_error(self, title, err_text):
        os.system("""
        osascript -e 'display notification "{}" with title "{}"'
        """.format(err_text, title))

    def listen(self):
        self._run = True
        parse_thread = threading.Thread(target=self._parse)
        parse_thread.setDaemon(True)
        parse_thread.start()
        self._activate()

    def stop(self):
        self._run = False
