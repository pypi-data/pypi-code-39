import sys

import Euclid.euclid as euclid


def modPower(a, b, mod):
    
    if b == 0:
        return 1
    
    p = modPower(a, b//2, mod) % mod
    p = (p * p) % mod

    result = p if (b % 2 == 0) else (a * p) % mod

    return result

def modInverse(a, mod):

    gcd = euclid.gcd(a, mod)
    
    if gcd == 1:
        return modPower(a, mod -2, mod)
    else:
        raise Exception("There is no modular inverse!")

def checkInvalidArguments(argv):

    if len(argv) == 1:
        raise Exception("No input arguments!")
    elif len(argv) == 2:
        raise Exception("Not enough input arguments!")
    
    secondArgumentIsZero = int(argv[2]) == 0
    if secondArgumentIsZero:
        raise Exception("Second number do not have to be 0")

if __name__ == "__main__":
    
    try:
        
        checkInvalidArguments(sys.argv)
        a = int(sys.argv[1])
        m = int(sys.argv[2])

        inverse = modInverse(a, m)
        print("The mod inverse of " + str(a) + " mod " + str(m) + " is " + str(inverse))
    
    except Exception as ex:
        print(ex)