def gcd(a, b):
    while (b > 0):
        a, b = b, a % b
    
    return a

def extgcd(a, b):
    # Return in x and y form a*x + b*y
    # x is the inverse of a
    # y is the inverse if b
    # There is only an inverse if gcd(a,b) == 1
    if a == 0:
        return (0, 1)
    else:
        x, y = extgcd(b % a, a)
        x1 = y - (b // a) * x
        y1 = x
        return (x1, y1)

def moduloInverseOf(a, b):
    inv = extgcd(a, b)
    return inv[0] % b

if __name__ == "__main__":
    
    numberList = [0, 1, 2, 3, 4 ,5]
    b = 5

    for a in numberList:
        resultGCD = gcd(a,b)

        inverse = "No Inverse"
        if resultGCD == 1:
            inverse = moduloInverseOf(a, b)

        print("Greatest Common Divisor: ", resultGCD)
        print("Inverse of " + str(a) + " mod " + str(b) + " is: ", inverse)
        print("------------------------------")