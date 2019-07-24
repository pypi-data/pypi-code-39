import numbers


class ArabicToRoman(object):

    _int_nums = (
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )

    @staticmethod
    def convert(arabic: int) -> str:
        """Convert an Arabic numeral to a Roman numeral

        To convert Arabic numerals we chose the algorithm from Paul M. Winkler
        presented in  :code:`"Python Cookbook" by David Ascher, Alex Martelli ISBN: 0596001673`.
        since it is arguably the most readable algorithm.     
        
        Args:
            arabic (int): Arabic numeral represented as integer. The number must be be in :code:`[1,...,3999]`
        
        
        Raises:
            TypeError: arabic does not satisfy  :code:`isinstance(arabic, numbers.Integral)` must be true.
            ValueError: arabic does not satisfy :code:`1 <= v <= 3999`

        Returns:
            str : string encoding the input as Roman numeral
        """

        if not isinstance(arabic, numbers.Integral):
            raise TypeError("expected integer, got {}".format(type(arabic)))

        if arabic < 1 or arabic > 3999:
            raise ValueError("Argument must be between 1 and 3999")

        result = []
        for val, chars in ArabicToRoman._int_nums:
            count = int(arabic // val)
            result.append(chars * count)
            arabic -= val * count

        return "".join(result)


def arabic_to_roman(arabic: int) -> str:
    """Convert an Arabic numeral to a Roman numeral

    Shorthand for :py:meth:`ArabicToRoman.convert`, see
    :py:meth:`ArabicToRoman.convert` for full documentation.
    
    Args:
        arabic: Arabic numeral represented as integer.
    
    Raises:
        TypeError: arabic does not satisfy  :code:`isinstance(arabic, numbers.Integral)` must be true.
        ValueError: arabic does not satisfy :code:`1 <= v <= 3999`

    Returns:
        str : string encoding the input as Roman numeral
    """

    return ArabicToRoman.convert(arabic)
