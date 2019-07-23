"""
Provides a collection of functions to help calculate Adstock
"""
import pandas as pd
import numpy as np
import scipy as sp

#charts
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#statistical modelling
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.tsa as tsa

#metrics
from sklearn.metrics import r2_score

"""

y[t+1] = i*y[t] + (1-i)*y[t-1]

Usage:

(adstock_val,df[stock+"_adstock"]) = _adstock(df[stock],df[kpis[-1]])
print(stock,adstock_val)

Returns

decay factor
transformed numpy array

"""
def _adstock(X,y):

    l_corr = 0
    adstock_val = 0
    for i in np.linspace(0.4,0.8,10):
        corr = np.corrcoef(y, tsa.filters.filtertools.recursive_filter(X*i,(1.0-i)))[0][1]
        if corr > l_corr:
            adstock_val = i
            l_corr = corr

    return (adstock_val, tsa.filters.filtertools.recursive_filter(X*adstock_val,(1.0-adstock_val)))

"""

Loops through a dataframe calculating adstock for a set of columnes as follows

y[t+1] = alpha*y[t] + (1-alpha)*y[t-1]

Usage:

(adstock_val,df[stock+"_adstock"]) = _adstock(df[stock],df[kpis[-1]])
print(stock,adstock_val)

Returns

summary data set with alpha for each feature
transformation of each column


"""
def Adstock(df,y):

    df_out = pd.DataFrame()
    df_summary = pd.DataFrame(columns=['Feature','AdStock-Val'])

    if not isinstance(df, pd.DataFrame):
        raise Exception('Adstock function requires parameter 1 (df) is a Dataframe, {type} found instead'.format(type=type(df)))

    for i in list(df.columns):
        (adstock_val,df_out[i]) = _adstock(df[i],y)
        df_summary = df_summary.append({'Feature': i,'AdStock-Val' : adstock_val }, ignore_index=True)

    df_summary.set_index('Feature',inplace=True)

    return (df_summary.sort_values(by='AdStock-Val',ascending=False),df_out)


def Adstock_feature_plot(df,df_adstock,loc=None,size=(20,30),color_dict=None):
    adstock = list(df_adstock.columns)
    if color_dict==None:
        color_dict = {
            '1st': "#C71585",
            '2nd': "#A0AEBE",
            '3rd': '#00001E',
            '4th': "#003C6E",
            '5th': "#ff0099",
            '6th': "#EEAE09",
            '7th': '#C8D3DC',
            '8th': '#EC5F67',
            '9th': '#F99157',
            '10th': '#FAC863',
            '11th': '#99C794',
            '12th': '#081F2D',
            '13th': '#5FB3B3',
            '14th': '#6699CC',
            '15th': '#273A72',
            '16th': '#C594C5',
            '17th': '#EB99C7'
        }

    if loc == None:
        print('Warning: no location given to save plots')

    Tot = len(adstock)
    Cols = 2

    # Compute Rows required

    Rows = Tot // Cols
    Rows += Tot % Cols

    # Create a Position index

    Position = range(1,Tot + 1)


    fig = plt.figure(figsize=size)
    for k in range(Tot):
        ax = fig.add_subplot(Rows,Cols,Position[k])
        df[adstock[k]].plot(c=color_dict['5th'])
        df_adstock[adstock[k]].plot(c=color_dict['2nd'])
        plt.legend([df_adstock.columns[k],'ADSTOCK_'+df_adstock.columns[k]])

    plt.show()


def Adstock_summary_plot(df_adstock_summary,loc=None,size=(20,10),cmap=None):
    if loc == None:
        print('Warning: no location given to save plots')

    df_adstock_summary[df_adstock_summary['AdStock-Val'] > 0].plot(kind='bar',cmap=cmap,figsize=size)
    plt.title('Ad Stock Delay')
    plt.ylabel('Credit given on day 1 %')
    plt.legend([])
    plt.show()

if __name__ == "__main__":
    pass
