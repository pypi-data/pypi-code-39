"""
Speech API algorithm
"""
# pylint: disable=no-name-in-module
import os
import logging
import json
import speech_recognition as sr
from PySide2.QtCore import QObject, Signal

LOGGER = logging.getLogger("voice_recognition_logger")


class VoiceRecognitionService(QObject):
    """
    Voice Recognition service which takes an microphone input and converts it
    to text by using the Google Cloud Speech-to-Text API
    """

    next = Signal()
    previous = Signal()
    undo = Signal()
    quit = Signal()
    voice_command = Signal(str)

    def __init__(self):

        """
        Constructor.
        """

        LOGGER.info("Creating Voice Recognition Service")
        # Need this for SignalInstance
        super(VoiceRecognitionService, self).__init__()

        self.stop_listen = None

        #  this is to add the credentials for the google cloud api
        #  set the environment variable GOOGLE_APPLICATION_CREDENTIALS
        #  to the path  of your json file with credentials
        key_file_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        with open(key_file_path, 'r') as file:
            self.credentials = file.read()

        #  this raises a ValueError if the credential file isn't a valid json
        json.loads(self.credentials)

        LOGGER.info("Created Voice Recognition Service")

    def listen(self):

        """
        Method which starts listening in the background
        """
        #  self.next.emit()
        # Record Audio
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        #  initialization of the background listening thread
        LOGGER.info("Say something!")
        self.stop_listen = recognizer\
            .listen_in_background(microphone, self.callback)

    def callback(self, recognizer, audio):

        """
        Method which gets called by the background listener
        :param recognizer: recognizer from Python speech API
        :param audio: audio input (e.g. microphone)
        :return:
        """

        #  this is called by the background thread,
        #  converting speech in a string
        try:
            # google cloud speech to text with credentials (json file)
            words = recognizer\
                .recognize_google_cloud(audio,
                                        credentials_json=self.credentials)
            LOGGER.info("You said: %s", words)
            #  if the string equals a certain keyword (here "start")
            #  the background thread is stopped and the a method
            #  is called to listen to one single command
            if words == "start ":
                self.stop_listen(wait_for_stop=False)
                self.listen_to_command()
        except sr.UnknownValueError:
            LOGGER.info("Google Speech Recognition could not understand audio")
        except sr.RequestError as exception:
            LOGGER.info("Could not request results from Google Speech "
                        "Recognition service; %s", exception)

    def listen_to_command(self):

        """
        This method gets called when a specific command is said.
        It then listens for specific commands and converts them to QT Signals
        :return:
        """

        recognizer = sr.Recognizer()
        #  listen to a single command
        with sr.Microphone() as source:
            LOGGER.info("Listening for command")
            audio = recognizer.listen(source)
        try:
            #  convert command to string,
            #  this string should later be used to fire a certain GUI command
            words = recognizer.\
                recognize_google_cloud(audio,
                                       credentials_json=self.credentials)
            #  convert the spoken input in a signal
            #  for next, quit, previous and undo there are specific signals
            #  if none of them is said, a generic signal is emitted, containing
            #  the string of the spoken input
            if words == "next ":
                self.next.emit()
            elif words == "quit ":
                self.quit.emit()
            elif words == "previous ":
                self.previous.emit()
            elif words == "undo ":
                self.undo.emit()
            else:
                self.voice_command.emit(words)
        except sr.UnknownValueError:
            LOGGER.info("Google Speech Recognition could not understand audio")
        except sr.RequestError as exception:
            LOGGER.info("Could not request results from Google Speech "
                        "Recognition service; %s", exception)

        #  call self.listen() again
        #  to get the background thread start listening again
        self.listen()
