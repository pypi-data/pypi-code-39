# -*- coding: UTF-8 -*-

def dec2bin(number):
     '''
         This function calculates the binary of the given decimal number
         :param number: decimal number in string or integer format
         :return : string of the equivalent binary number
 
         Algo:
         1. Divide the decimal number by 2. Treat the division as an integer division.
         2. Write down the remainder (in binary).
         3. Divide the result again by 2. Treat the division as an integer division.
         4. Repeat step 2 and 3 until result is 0.
         5. The binary value is the digit sequence of the remainders from the last to first.
     '''
     if isinstance(number, str):
         number = int(number)
     binary = []
     while number >= 1:
         remainder = number % 2
         binary.append(remainder)
         number = number // 2
 
     return ''.join(map(str, binary[::-1]))
 

def bin2dec(number):
    '''
        This function calculates the decimal of the given binary number
        :param number: decimal number in string or integer format
        :return : integer of the equivalent decimal number

        Algo:
        1. Get the last digit of the binary number.
        2. Multiply the current digit with (2^power), store the result.
        3. Increment power by 1.
        4. Repeat from step 2 until all digits have been multiplied.
        5. Sum the result of step 2 to get the answer number.
    '''
    decimal = []
    number = list(str(number)[::-1])
    for i in range(len(number)):
        decimal.append(int(number[i]) * (2 ** i))

    return sum(decimal)


def dec2hex(number):
    '''
        This function calculates the hex of the given decimal number
        :param number: decimal number in string or integer format
        :return : string of the equivalent hex number

        Algo:
        1. Divide the decimal number by 16. Treat the division as an integer division.
        2. Write down the remainder (in hexadecimal).
        3. Divide the result again by 16. Treat the division as an integer division.
        4. Repeat step 2 and 3 until result is 0.
        5. The hex value is the digit sequence of the remainders from the last to first.
    '''
    if isinstance(number, str):
        number = int(number)
    hexadec = []
    hex_equivalents = {10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F'}
    while number >= 1:
        remainder = number % 16
        if remainder < 10:
            hexadec.append(remainder)
        elif remainder >= 10:
            hexadec.append(hex_equivalents[remainder])

        number = number // 16

    return ''.join(map(str, hexadec[::-1]))


def hex2dec(number):
    '''
        This function calculates the decimal of the given hex number
        :param number: hex number in string or integer format
        :return : integer of the equivalent decimal number

        Algo:
        1. Get the last digit of the hex number.
        2. Multiply the current digit with (16^power), store the result.
        3. Increment power by 1.
        4. Repeat from step 2 until all digits have been multiplied.
        5. Sum the result of step 2 to get the answer number.
    '''
    decimal = []
    decimal_equivalents = {'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
    number = list(str(number)[::-1])
    for i in range(len(number)):
        try:
            if int(number[i]) < 10:
                decimal.append(int(number[i]) * (16 ** i))
        except ValueError:
            decimal.append(decimal_equivalents[number[i]] * (16 ** i))

    return sum(decimal)



def roman2int(s):
    number = 0
    roman = {'M':1000, 'D':500, 'C': 100, 'L':50, 'X':10, 'V':5, 'I':1}
    for i in range(len(s)-1):
        if roman[s[i]] < roman[s[i+1]]:
            number -= roman[s[i]]
        else:
            number += roman[s[i]]
    return number + roman[s[-1]]


def int2roman(num):
    """
    :type num: int
    :rtype: str
    """
    m = ["", "M", "MM", "MMM"];
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"];
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"];
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"];
    return m[num//1000] + c[(num%1000)//100] + x[(num%100)//10] + i[num%10];




   
