from otherPackage.Texto import Texto

class PrintText:

    def printTextCustom(self, text):
        tx = Texto()
        tx.printText("Hello : " + text)