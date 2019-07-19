# coding=utf-8
"""
Demo for the Speech API module
"""
# pylint: disable=c-extension-no-member, no-name-in-module, no-self-use
import sys
import logging
import PySide2.QtCore
from sksurgeryspeech.algorithms import voice_recognition_service as speech_api

LOGGER = logging.getLogger("voice_recognition_logger")


class VoiceListener(PySide2.QtCore.QObject):

    """
    Class which contains the slots for the demo application
    """

    @PySide2.QtCore.Slot()
    def on_next(self):
        """
        Slot for next signal
        :return:
        """
        LOGGER.info("Next signal caught")

    @PySide2.QtCore.Slot()
    def on_previous(self):
        """
        Slot for the previous signal
        :return:
        """
        LOGGER.info("Previous signal caught")

    @PySide2.QtCore.Slot()
    def on_undo(self):
        """
        Slot for the undo signal
        :return:
        """
        LOGGER.info("Undo signal caught")

    @PySide2.QtCore.Slot()
    def on_quit(self):
        """
        Slot for the quit signal
        Quits application
        :return:
        """
        LOGGER.info("Quit signal caught... Exit application")
        PySide2.QtCore.QCoreApplication.quit()

    @PySide2.QtCore.Slot()
    def on_voice_signal(self, input_string):
        """
        Slot for the voice signal,
        which just contains the microphone input as string
        :return:
        """
        LOGGER.info("Generic voice signal caught with input: %s", input_string)


class SpeechRecognitionDemo(PySide2.QtCore.QObject):

    """
    Demo class for the Speech API module
    """
    def __init__(self):
        """
        Constructor.
        """
        super(SpeechRecognitionDemo, self).__init__()
        self.voice_recognition = speech_api.VoiceRecognitionService()
        self.listener = VoiceListener()
        #  connect the Signals emitted by the VoiceRecognitionService()
        #  with the Slots of the VoiceListener
        self.voice_recognition.next.connect(self.listener.on_next)
        self.voice_recognition.previous.connect(self.listener.on_previous)
        self.voice_recognition.undo.connect(self.listener.on_undo)
        self.voice_recognition.quit.connect(self.listener.on_quit)
        self.voice_recognition.voice_command\
            .connect(self.listener.on_voice_signal)

    def run_demo(self):
        """
        Entry point to run the demo
        :return:
        """
        #  instantiate the QCoreApplication
        app = PySide2.QtCore.QCoreApplication()
        #  set up the logger
        voice_recognition_logger = logging.getLogger("voice_recognition_logger")
        voice_recognition_logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        file_handler = logging.FileHandler('voice_recognition_log.log')
        file_handler.setLevel(logging.INFO)
        voice_recognition_logger.addHandler(console_handler)
        voice_recognition_logger.addHandler(file_handler)

        #  this is the main call to start the background thread listening,
        #  which also later has to be called within the SmartLiver code
        self.voice_recognition.listen()
        #  start the application, meaning starting the infinite Event Loop which
        #  stops when the user says "start" followed by "quit"
        return sys.exit(app.exec_())
