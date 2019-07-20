#!-*-coding:utf-8-*-
import os
import sys
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append("../../")
import makinyan as mak

plt.rcParams["font.family"] = "IPAexGothic"


__all__ = ["hist","boxplt","pairplot","heatmap","cycle","lineplt"]

def lineplt( X , Y , df , save=False , filename=False , path=False ):
    sns.set()
    sns.scatterplot  ( x=X, y=Y, data=df , size=1 )
    _saveorshow( flag=save , filename=filename , path=path )
    plt.clf()


def hist( data , save=False , path=False ):
    """
    Histgram
    """
    y = list( data.values() )
    x = list( data.keys() )
    plt.bar( np.array( range( len( x ) ) ) , y )
    plt.xticks( np.array( range( len( x ) ) ) , x )

    _saveorshow( flag=save , filename="tf_hist.png" , path=path )


def boxplt( df , title="" , xlabel="X" , ylabel="Y" , save=False , path=False , filename="boxplot.png" ):
    """
    BoxPlot
    """
    sns.set(style="whitegrid")
    sns.boxplot(x=xlabel, y=ylabel, data=df);

    _saveorshow( flag=save , filename=filename , path=path )
    plt.clf()


def pairplot( df , hue=False , save=False , path=False , filename="paireplot.png" ):
    """
    PairePlot
    """

    sns.set(style="darkgrid")

    if hue == False:
        sns.pairplot( df )
    else:
        sns.pairplot(df,hue=hue,palette="muted",size=2 )

    _saveorshow( flag=save , filename=filename , path=path )
    plt.clf()


def heatmap( df , vmin=-1.0 , vmax=1.0 , save=False , path=False , filename="heatmap.png" ):
    """
    Heatmap
    """
    sns.set(style="darkgrid")
    sns.heatmap(df.corr(), annot=True , vmin=vmin , vmax=vmax , cmap="inferno")

    _saveorshow( flag=save , filename=filename , path=path )
    plt.clf()


def cycle( x , labels , save=False , path=False , filename="cycle.png" ):
    """
    Cycle graph
    """
    sns.set()
    plt.pie(x, labels=labels)
    plt.axis('equal')

    _saveorshow( flag=save , filename=filename , path=path )
    plt.clf()

def _saveorshow( flag , filename , path ):
    if flag and path:
        plt.savefig( path + "/" + filename )
    else:
        plt.show()
