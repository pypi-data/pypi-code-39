
class MetricConverter:
    metricValues = {
        "dm": -1,
        "cm": -2,
        "mm": -3,
        "um": -6,
        "nm": -9,
        "pm": -12,
        "fm": -15,
        "am": -18,
        "zm": -21,
        "ym": -24,
        "m": 0,
        "dam": 1,
        "hm": 2,
        "km": 3,
        "Mm": 6,
        "Gm": 9,
        "Tm": 12,
        "Pm": 15,
        "Em": 18,
        "Zm": 21,
        "Ym": 24,
    }

    def getIndividualConversion(self, initialNum: float, fromUnit: str, toUnit: str):
        ''' Takes in the initial longitude and converts it to the target unit.'''
        diff = self.metricValues[fromUnit] - self.metricValues[toUnit]
        currNum = (10 ** (diff)) * initialNum
        return currNum

    def convert(self, units):
        ''' Converts the given array into the desired metric longitude.'''
        convertedUnits = []
        for x in units:
            initialNum = float(x[0])
            fromUnit = x[1]
            toUnit = x[2]
            convertedUnit = self.getIndividualConversion(
                initialNum, fromUnit, toUnit)
            convertedUnitString = x[0] + " " + x[1] + \
                " " + x[2] + " " + str(convertedUnit)
            convertedUnits.append(convertedUnitString)
        return convertedUnits
