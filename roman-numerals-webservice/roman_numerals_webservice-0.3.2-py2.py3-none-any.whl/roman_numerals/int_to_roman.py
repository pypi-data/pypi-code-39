import numbers

class ArabicToRoman(object):

    _int_nums = ((1000, 'M'), (900, 'CM'), (500, 'D'), 
                 (400, 'CD'), (100, 'C'), (90, 'XC'), 
                 (50, 'L'), (40, 'XL'), (10, 'X'),
                 (9, 'IX'), (5, 'V'), (4, 'IV'), 
                 (1, 'I'))

    @staticmethod
    def convert(input : int) -> str:
        """ Convert an integer to a Roman numeral. """

        if not isinstance(input,  numbers.Integral):
            raise TypeError("expected integer, got {}".format(type(input)))

        if input < 1 or input > 3999:
            raise ValueError("Argument must be between 1 and 3999")
        
        result = []
        for val, chars in ArabicToRoman._int_nums:
            count = int(input // val)
            result.append( chars * count)
            input -= val * count

        return ''.join(result) 

int_to_roman  = ArabicToRoman.convert
