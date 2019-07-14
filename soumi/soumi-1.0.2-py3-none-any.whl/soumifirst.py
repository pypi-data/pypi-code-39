# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:08:38 2019

@author: Soumitra
"""
def sayhello():
    print("Hi There Beautiful Person!")

def add(x,y):
    print(x+y)
def minus(x,y):
    print(x-y)
def prod(x,y):
    print(x*y)
def div(x,y):
    print(x/y)
def fldiv(x,y):
    print(x//y)
def power(x,y):
    print(x**y)


def fact(x):
    if type(x)==int:
        flg="invalid for negative integers"
        if x>0:
            return fact(x-1)*x
        elif x<0:
            raise Exception(flg)
        else:
            return 1
    else:
        raise Exception("invalid for non-integers")


def strrev(s):
    if type(s)==str:
        return s[::-1]
    else:
        raise Exception("Not a string")

def numrev(n):
    if type(n)==int:
        a=n
        rev=0
        while(a>0):
            rev=rev*10
            rev=rev+a%10
            a=a//10
        return rev
    else:
        raise Exception("Only positive integers allowed")

        
def palindrome(x):
    if type(x)==int:
        if numrev(x)==x:
            return True
        else:
            return False
    elif type(x)==str:
        if strrev(x)==x:
            return True
        else:
            return False
    else:
        raise Exception("Only positive integers and strings allowed")

def ncr(n,r):
    if(n>r):
        p=fact(r)*fact(n-r)
        return int((fact(n)/p))
    else:
        raise Exception("First Argument Must be Greater than Second Argument")

def npr(n,r):
    if(n>r):
        return int((fact(n)/fact(n-r)))
    else:
        raise Exception("First Argument Must be Greater than Second Argument")
