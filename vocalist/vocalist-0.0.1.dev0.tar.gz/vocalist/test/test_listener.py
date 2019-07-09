import time
from threading import Timer
from unittest import TestCase
from unittest import mock
from ..listener import Listener
import os
import speech_recognition as sr


class ListenerTest(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_successful_strategy_mapping(self):
        with mock.patch('speech_recognition.Microphone', return_value=object):
            try:
                _ = Listener(strategy="sphinx")
                assert True
            except KeyError:
                self.fail()
            except Exception:
                self.fail()

    def test_erroneous_strategy_mapping(self):
        try:
            _ = Listener(strategy="testException")
            self.fail()
        except KeyError:
            self.assertRaises(KeyError)
        except Exception:
            self.fail()

    def test_pyaudio_not_installed(self):
        with mock.patch('speech_recognition.Microphone') as mocked_mic:
            mocked_mic.side_effect = AttributeError("test")
            try:
                _ = Listener()
                self.fail()
            except AttributeError as err:
                self.assertEqual("You'll need to install PyAudio first: https://people.csail.mit.edu/hubert/pyaudio/", str(err))
            except Exception:
                self.fail()

    def test_no_mic_found(self):
        with mock.patch('speech_recognition.Microphone', return_value=None):
            l = Listener()
            try:
                l.listen()
                l.stop()
                self.fail()
            except NameError as err:
                self.assertEqual("Could not find a suitable microphone.", str(err))
            except Exception:
                self.fail()

    def test_could_not_parse_text(self):
        with mock.patch('speech_recognition.Microphone') as mocked_mic:
            mocked_mic.return_value.__enter__ = lambda x: time.sleep(.5)
            rel_path = os.path.join(os.getcwd(), "audio-files/harvard.wav")
            harvard = sr.AudioFile(rel_path)
            os.system = mock.MagicMock()
            l = Listener()
            with harvard as source:
                audio = l.recognizer.record(source)
            l.recognizer.listen = mock.MagicMock(return_value=audio)
            l.transcribe = mock.Mock(side_effect=sr.UnknownValueError("test"))
            s = Timer(1.0, l.stop)
            s.start()
            l.listen()
            assert os.system.called
