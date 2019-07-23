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

from sklearn.linear_model import Lasso, Ridge

def FitModel_formula(formula,all_data,test,holdout,target,size=(20,20)):
    res = smf.ols(formula = formula, data = test).fit()
    res_all = smf.ols(formula = formula, data = all_data).fit()

    holdout['predicted'] = res.predict(holdout)
    test['predicted'] = res.predict(test)
    all_data['predicted_test'] =  res.predict(all_data)
    all_data['predicted_all'] =  res_all.predict(all_data)

    #R^2
    mn = np.mean(holdout[target])
    tot = np.sum((holdout[target] - mn)**2)
    rss = np.sum((holdout[target] - holdout['predicted'])**2)
    score = 1 - rss/tot

    #fstat
    p_val = sp.stats.f_oneway(test['predicted'],holdout['predicted'])[1]

    ax = plt.subplot(131)
    plt.scatter(test[target],
                test['predicted'],
                color = sns.color_palette()[2],
                s = 10,
                marker = 'o')
    ax.set_title('Test Fit')
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')

    ax = plt.subplot(132)
    plt.scatter(holdout[target],
                holdout['predicted'],
                color = sns.color_palette()[1],
                s = 10,
                marker = 'o')
    ax.set_title('Holdout Fit')
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')

    ax = plt.subplot(133)
    plt.scatter(all_data[target],
                all_data['predicted_all'],
                color = sns.color_palette()[2],
                s = 10,
                marker = 'o',
                alpha = 0.5)
    plt.scatter(all_data[target],
                all_data['predicted_test'],
                color = sns.color_palette()[1],
                s = 10,
                marker = 'o',
                alpha = 0.2)

    ax.set_title('All Fit')
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')

    plt.show()

    return (res,res_all,score,p_val)


def FitModel_Lasso(train,test,target,independent,size=(10,10)):

    lasso = Lasso(alpha=0.1,positive=True)
    res = lasso.fit(train[independent], train[target])

    train['predicted'] = res.predict(train[independent])
    test['predicted'] = res.predict(test[independent])


    model_summary = pd.DataFrame(columns=['Fields','Coef'])

    model_summary['Fields'] = independent
    model_summary['Coef'] = res.coef_
    model_summary.loc[-1] = ['Intercept', res.intercept_]
    model_summary = model_summary.sort_index()


    plt.figure(figsize=size)

    plt.scatter(train[target],
                train['predicted'],
                color = sns.color_palette()[0],
                s = 20,
                marker = 'o')

    plt.scatter(test[target],
                test['predicted'],
                color = sns.color_palette()[1],
                s = 20,
                marker = 'o')

    plt.title('Predict vs. Actual')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.legend(['Train','Test'])

    plt.show()

    return (res,model_summary.sort_values(by='Coef',ascending=False))


def FitModel_Ridge(train,test,target,independent,size=(10,10),log=False):
    from sklearn.linear_model import Ridge

    ridge = Ridge(alpha=0.05)
    res = ridge.fit(train[independent], train[target])

    train['predicted'] = res.predict(train[independent])
    test['predicted'] = res.predict(test[independent])


    model_summary = pd.DataFrame(columns=['Fields','Coef'])

    model_summary['Fields'] = independent
    model_summary['Coef'] = res.coef_
    model_summary.loc[-1] = ['Intercept', res.intercept_]
    model_summary = model_summary.sort_index()


    plt.figure(figsize=size)

    plt.scatter(train[target],
                train['predicted'],
                color = sns.color_palette()[0],
                s = 20,
                marker = 'o')

    plt.scatter(test[target],
                test['predicted'],
                color = sns.color_palette()[1],
                s = 20,
                marker = 'o')

    plt.title('Predict vs. Actual')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.legend(['Train','Test'])

    plt.show()

    return (res,model_summary.sort_values(by='Coef',ascending=False))
