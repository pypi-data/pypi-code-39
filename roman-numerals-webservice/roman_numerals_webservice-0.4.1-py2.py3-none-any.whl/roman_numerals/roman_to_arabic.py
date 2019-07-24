from .arabic_to_roman import arabic_to_roman


class RomanToArabic(object):
    _char_2_number = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}

    @staticmethod
    def convert(roman: str) -> int:
        """ Convert a Roman numeral to an Arabic Numeral.


        To convert Arabic numerals we chose the algorithm from Paul M. Winkler
        presented in  :code:`"Python Cookbook" by David Ascher, Alex Martelli ISBN: 0596001673`.
        since it is arguably the most readable algorithm.
        
        Args:
            roman (str): Roman numeral represented as string.
        
        Raises:
            TypeError: roman is not a string
            ValueError: roman is not a valid Roman numeral

        Returns:
            int : int encoding the input as Arabic numeral       
        """
        if not isinstance(roman, str):
            raise TypeError("expected string, got {}".format(type(roman)))
        roman = roman.upper()
        nums = RomanToArabic._char_2_number
        sum = 0
        for i in range(len(roman)):
            try:
                value = nums[roman[i]]
                # If the next place holds a larger number, this value is negative
                if i + 1 < len(roman) and nums[roman[i + 1]] > value:
                    sum -= value
                else:
                    sum += value
            except KeyError:
                raise ValueError("roman is not a valid Roman numeral: {}".format(roman))

        # only if the inverse gives input as result it was a vaid roman numeral
        if arabic_to_roman(sum) == roman:
            return sum
        else:
            raise ValueError("roman is not a valid Roman numeral: {}".format(roman))




def roman_to_arabic(arabic: int) -> str:
    """ Convert a Roman numeral to an Arabic Numeral.
    
     Shorthand for :py:meth:`RomanToArabic.convert`, see
    :py:meth:`RomanToArabic.convert` for full documentation.
    
    Args:
        roman (str): Roman numeral represented as string.
    
    Raises:
        TypeError: roman is not a string
        ValueError: roman is not a valid Roman numeral

    Returns:
        int : int encoding the input as Arabic numeral       
    """
    return RomanToArabic.convert(arabic)