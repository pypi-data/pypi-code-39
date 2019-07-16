#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import yaml
#import sys

def check_arguments(args):
    """
    Verify if arguments are in the norm during the call of main.py
    """
    if len(args)!=2:
        raise ValueError('Correct use is: python main.py <parameter-file>')
    if not os.path.isfile(os.getcwd()+'/'+args[1]):
        raise FileNotFoundError('File %s was not found.'%args[1])
    return args[1];

def read_parameters(filename):
    """
    Read file.yaml and return the parameters along dict form
    """
    # Reading Parameters From YAML 
    
    try:
        f=open(filename,'r')
    except: 
        raise FileNotFoundError('File %s was not found.')
    parameters = yaml.load(f)
    f.close()
    
    # Checking the existence of required parameters 
    # TODO: Implement checks
    
    # Returning the parameters
    return parameters;





