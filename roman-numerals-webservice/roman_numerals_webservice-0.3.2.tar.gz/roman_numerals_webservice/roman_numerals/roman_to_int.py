from . int_to_roman import int_to_roman

class RomanToArabic(object):
    _char_2_number = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}

    @staticmethod
    def convert(input : str) -> int:
        """ Convert a Roman numeral to an integer.

        """
        if not isinstance(input, str):
            raise TypeError("expected string, got {}".format(type(input)))
        input = input.upper()
        nums = RomanToArabic._char_2_number
        sum = 0
        for i in range(len(input)):
            try:
                value = nums[input[i]]
                # If the next place holds a larger number, this value is negative
                if i+1 < len(input) and nums[input[i+1]] > value:
                    sum -= value
                else: 
                    sum += value
            except KeyError:
                raise ValueError('input is not a valid Roman numeral: {}'.format(input))
        # easiest test for validity...
        if int_to_roman(sum) == input:
            return sum
        else:
            raise ValueError('input is not a valid Roman numeral: {}'.format(input))


roman_to_int = RomanToArabic.convert