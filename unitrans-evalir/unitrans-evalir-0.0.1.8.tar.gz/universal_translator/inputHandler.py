
class InputHandler:

    def parseInput(self, gInput: str):
        '''Handles input parsing'''
        splitInput = gInput.split()
        if len(splitInput) < 3:
            print("invalid input: expecting 3 columns.")
            return
        parsedInput = []
        for i in range(0, len(splitInput) - 1, 3):
            newArr = [splitInput[i],
                      splitInput[i + 1], splitInput[i + 2]]
            parsedInput.append(newArr)
        return parsedInput

    def writeToFile(self, pathname: str, convertedUnits):
        ''' Writes the results to a file'''
        osFile = open(pathname, 'w', encoding="utf-8")
        for convertedUnit in convertedUnits:
            osFile.write(convertedUnit + "\n")
