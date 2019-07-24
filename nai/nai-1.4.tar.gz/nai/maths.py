# -*- coding: UTF-8 -*-
import math
from functools import reduce

#Average Value of Array
def average(array):
 total = 0
 for i in array:
  total+=i
 return total/float(len(array))

#Sigmoid Function
def sigmoid(n):
  # activation function
  return 1/(1+math.exp(-n))

#Mode of Values in Array
def mode(array):
 mid = len(array)/2
 return array[mid]

#Total Sum of array
def total(array):
 sum = 0
 for i in array:
   sum+=i
 return sum

#Find factorial
def factorial(n):
 fact = 1
 for i in range(1,n+1):
   fact = fact*i
 return fact


def lcm(_list):
     """LCM
     function to find LCM for given list of elements
     :param _list: _list of which LCM is to be found out
     """
 
     def __lcm(a, b):
         """
         helper function for finding LCM
 
         :param a:
         :param b:
         :return: lcm
         """
         if a > b:
             greater = a
         else:
             greater = b
 
         while True:
             if greater % a == 0 and greater % b == 0:
                 lcm_ = greater
                 break
             greater += 1
         return lcm_
 
     return reduce(lambda x, y: __lcm(x, y), _list)


def primesin(n):
    """
    function to find and print prime numbers up
    to the specified number

    :param n: upper limit for finding all primes less than this value
    """
    primes = [True] * (n + 1)
    # because p is the smallest prime
    p = 2

    while p * p <= n:
        # if p is not marked as False, this it is a prime
        if primes[p]:
            # mark all the multiples of number as False
            for i in range(p * 2, n + 1, p):
                primes[i] = False
        p += 1

    # getting all primes
    primes = [element for element in range(2, n) if primes[element]]

    return primes

#Add two binary numbers
def addbin(a, b):
    s = ""
    c, i, j = 0, len(a)-1, len(b)-1
    zero = ord('0')
    while (i >= 0 or j >= 0 or c == 1):
        if (i >= 0):
            c += ord(a[i]) - zero
            i -= 1
        if (j >= 0):
            c += ord(b[j]) - zero
            j -= 1
        s = chr(c % 2 + zero) + s
        c //= 2 
        
    return s

def gentable(n):
  '''
    Generate Any Number Table 1-10 or > 10
  '''
  print("_"*3+"[ Table Of %s ]"%n+"_"*3+"\n")
  for i in range(1,10+1):
    print("{} × {} = {}".format(n,i,n*i))
  print("\n")

#find factor of a number 6 = 2×3
def factor(n):
  rem = [n%x for x in range(1,n) if n%x != 0]
  for z in range(n):
    for y in rem:
      if z*y == n:
        return [z,y]

#Find Percentage of each number in array
def eachpercent(array,total):
  for marks in array:
    print("{}/{}×100  = {}%".format(marks,total,(marks/float(total))*100.0))

#Number Theory Related function
def ntsquareadd(n):
  '''
  it is to find all such numbers whose square when added
  among each other gives again that number
  '''
  num = []
  for i in map(lambda x: len(str(x*x)) >= 2 and int(str(x*x)[:len(str(x*x))/2])+int(str(x*x)[len(str(x*x))/2:]) == x and x,range(n)):
     if i != bool(0):
        num.append(i)
  return num


#Generate numbers of format a+1+a+a+1
def a_n_b(n):
  x=0;a=0;b=0;c=0
  z = []
  while x <= n:
     z.append((a,b,c))
     x+=1
     a+=1
     b+=2
     c+=1
  return z