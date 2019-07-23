# split the data "properly"
import random
import pandas as pd
import numpy as np
import scipy as sp

def Generate_Formula(target,independent):
    return target + '~' + '+'.join(independent)


def Split(df,targets,split=0.33,seed=1235):

    random.seed(seed)

    p_vals = len(targets)

    c = 0
    while p_vals/len(targets) > 0.05 or c <= 100:
        rows = random.sample(list(df.index), int(len(df)*split))
        test = df.ix[rows].copy()
        train = df.drop(rows).copy()

        #check that we have equal splits
        #you may have to run this block several times
        p_vals = 0
        for target in targets:
            fstat1,p_val = sp.stats.f_oneway(test[target], train[target])
            p_vals = p_val + p_vals

        c = c + 1

    if c == 100 and  p_vals/len(targets) > 0.05:
        print("Warning unable to split into two equal groups after 100 tries")

    return (train,test, p_vals/len(targets))


def Taxi_groups(columns,groups):
    lst =[]
    for group in groups:
        lst.append([f for f in columns if group in f.lower()])

    return lst
