import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns


def Decompose_model(df,features,model_coef):
    decomp_fields = features.copy()
    decomp = df[features].copy()

    for spend in features:
        decomp[spend] = decomp[spend]*model_coef.query('Fields == "%s"' % spend)['Coef'].values[0]

    decomp['Base'] = model_coef.query('Fields == "Intercept"')['Coef'].values[0]

    return decomp


def Decompose_plots(df,color_dict=None,my_cmap=None):
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

    df.plot.area(stacked=True,cmap=my_cmap, figsize=(23,13))
    plt.title('Decomposition')
    plt.show()

    (df.mean()/df.mean().sum()).sort_values(ascending=False).plot.bar(cmap=my_cmap,figsize=(23,13))
    plt.title('Decomposition')
    plt.show()

    (df.ix[:,:-2].sum(axis=1)/df.sum(axis=1)).plot(c=color_dict['1st'],figsize=(23,13))
    plt.title('Marketing Driver on Sales')
    plt.show()


def Plot_ROAS_vs_Potentail(decomp,model_summary,spends,loc=None,color_dict=None):
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

    roas_vs_cap = pd.DataFrame()
    df = model_summary[model_summary['Fields'].isin(spends)]
    df_decomp = decomp[spends]

    roas_df = pd.DataFrame()

    roas_df = df[df['Coef'] > 0].set_index('Fields')*100
    cap_df = pd.DataFrame(df_decomp.max() - df_decomp.mean()).dropna().rename(columns={0:'Growth'})
    cap_df['Current Sales']  = pd.DataFrame(df_decomp.mean()).dropna()

    roas_vs_cap = roas_df.join(cap_df)

    x = roas_vs_cap['Coef'].values
    y = roas_vs_cap['Growth'].values/roas_vs_cap['Current Sales'].values
    y1 = roas_vs_cap['Current Sales'].values

    n = roas_vs_cap.index.values

    fig, ax = plt.subplots(figsize=(20,6.5))

    plt.scatter(x,y,s=200, c=color_dict['1st'], alpha=0)

    plt.xlabel('ROAS per £100', fontsize=18)
    plt.ylabel('Potentail Growth (x * current sales)', fontsize=18)

    plt.title('ROAS vs. Potentail Growth', fontsize=18)

    for i, txt in enumerate(n):
        ax.annotate(txt.lower().replace('brand','').replace('_spend','').replace('_',' ').title(), (x[i], y[i]), fontsize=15)
    sns.despine()

    if loc == None:
        pass
    else:
        fig.savefig(loc)

    return roas_vs_cap
