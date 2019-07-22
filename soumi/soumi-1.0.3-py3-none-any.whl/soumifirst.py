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

def bubble(l):
    n=len(l)
    for i in range(n-1):
        for j in range(n-i-1):
            if(l[j]>l[j+1]):
                l[j]=l[j]+l[j+1]
                l[j+1]=l[j]-l[j+1]
                l[j]=l[j]-l[j+1]
    return l

    
def check_sorted(l):
    for i in range(len(l)-1):
        if l[i]<l[i+1]:
            continue
        else:
            return False
def linsearch(l,x):
    for i in range(len(l)):
        if x==l[i]:
            return i
        else: 
            return False
def binsearch(l,x):
    left=0
    right=len(l)-1
    while left<right:
        mid=int((left+right)/2)
        if x>l[mid]:
            left=mid+1
        else:
            right=mid-1
    if x==l[left]:
        return left
    else:
        return False
