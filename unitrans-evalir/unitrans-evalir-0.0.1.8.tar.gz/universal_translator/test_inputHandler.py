from inputHandler import *
import unittest
import io


class TestInputHandler(unittest.TestCase):
    def testParseInput(self):
        readFile = "1 m km"
        handler = InputHandler()
        self.assertEqual([['1', 'm', 'km']], handler.parseInput(readFile))
