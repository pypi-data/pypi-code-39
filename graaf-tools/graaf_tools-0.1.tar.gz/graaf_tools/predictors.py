#!/usr/bin/env python
# coding: utf-8


from collections import OrderedDict
import json
import os
import time as time
import pandas as pd
import numpy as np
import datetime
import logging
import sys
# To save intermediate results in binary format
import pickle
# To use multiprocessing on functions with more than 1 parameter
from functools import partial
# Create folders + path access
import os
os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
from GRAAF.utils import *

import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier
from numpy import loadtxt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve
from sklearn.metrics import f1_score
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
#import scikitplot as skplt

from scikitplot.metrics import plot_lift_curve, plot_cumulative_gain, plot_roc, plot_precision_recall




class logistic_regression:

    def __init__(self, ITERAT = 5, START='01/10/2013', UPDATEGRAN=5, INPUT_DATA_PATH="", OUTPUT_DATA_PATH="", OUTPUT_FILENAME="", UNDERSAMPLING_RATIO=0, OVERSAMPLING_ALGORITHM="", OVERSAMPLING_RATIO=0, SCALING="", WORKERS=3):

        st = time.time()
        timegran = datetime.timedelta(days=1)
        start_of_data = pd.to_datetime(START, dayfirst=True)
        #baseline = BASELINE*timegran
        updategran = UPDATEGRAN*timegran


        #df = pd.read_csv(output_path+"/input.csv", index_col=0, parse_dates=['timestamp'])
        aucs_lr = []
        f1s_lr = []
        lifts_lr = []
        trainsizes = []
        testsizes = []
        fraudcasestrain = []
        fraudcasestest = []

        for i in range(ITERAT):
            #Load datasets
            self.baseline_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'baseline_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')
            self.day_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'day_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')


            #logging
            #Record the test and train data size
            trainsizes.append(self.baseline_df_embeddings.shape[0])
            testsizes.append(self.day_df_embeddings.shape[0])
            fraudcasestrain.append(self.baseline_df_embeddings[self.baseline_df_embeddings.fraud == True].shape[0])
            fraudcasestest.append(self.day_df_embeddings[self.day_df_embeddings.fraud == True].shape[0])

            X_train, y_train = preprocessing(self.baseline_df_embeddings, UNDERSAMPLING_RATIO=UNDERSAMPLING_RATIO, SCALING=SCALING, OVERSAMPLING_RATIO=OVERSAMPLING_RATIO, OVERSAMPLING_ALGORITHM=OVERSAMPLING_ALGORITHM)
            X_test, y_test = preprocessing(self.day_df_embeddings, SCALING=SCALING)


            model = LogisticRegression(solver='lbfgs', n_jobs=WORKERS, class_weight='balanced', penalty='l2', max_iter=500)
            model.fit(X_train, y_train)
            auc_lr, f1_lr, lift_lr, fpr, tpr, thresholds, fig = testing(model, X_test, y_test)

            aucs_lr.append(auc_lr)
            f1s_lr.append(f1_lr)
            lifts_lr.append(lift_lr)
            try:
                os.mkdir(OUTPUT_DATA_PATH+"images")
            except FileExistsError:
                # directory already exists
                pass
            plt.savefig(OUTPUT_DATA_PATH+"images/"+OUTPUT_FILENAME+"_logistic_regression"+"_iter_"+str(i)+'.png')
            plt.close()

            start_of_data += updategran

        # Report
        logger(OUTPUT_DATA_PATH+OUTPUT_FILENAME+"_logistic_regression", aucs_lr, f1s_lr, lifts_lr, fraudcasestrain, fraudcasestest)

        #Signal completion
        ed = time.time()
        print("Finished: ", os.getpid())
        print("Runtime of process ", os.getpid(), " was ", (ed-st))


class XGB:

    def __init__(self, ITERAT = 5, START='01/10/2013', UPDATEGRAN=5, INPUT_DATA_PATH="", OUTPUT_DATA_PATH="", OUTPUT_FILENAME="", UNDERSAMPLING_RATIO=0, OVERSAMPLING_ALGORITHM="", OVERSAMPLING_RATIO=0, SCALING="", WORKERS=3):

        st = time.time()
        timegran = datetime.timedelta(days=1)
        start_of_data = pd.to_datetime(START, dayfirst=True)
        #baseline = BASELINE*timegran
        updategran = UPDATEGRAN*timegran


        #df = pd.read_csv(output_path+"/input.csv", index_col=0, parse_dates=['timestamp'])
        aucs_xg = []
        f1s_xg = []
        lifts_xg = []
        trainsizes = []
        testsizes = []
        fraudcasestrain = []
        fraudcasestest = []

        for i in range(ITERAT):
            #Load datasets
            self.baseline_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'baseline_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')
            self.day_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'day_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')


            #logging
            #Record the test and train data size
            trainsizes.append(self.baseline_df_embeddings.shape[0])
            testsizes.append(self.day_df_embeddings.shape[0])
            fraudcasestrain.append(self.baseline_df_embeddings[self.baseline_df_embeddings.fraud == True].shape[0])
            fraudcasestest.append(self.day_df_embeddings[self.day_df_embeddings.fraud == True].shape[0])

            X_train, y_train = preprocessing(self.baseline_df_embeddings, UNDERSAMPLING_RATIO=UNDERSAMPLING_RATIO, SCALING=SCALING, OVERSAMPLING_RATIO=OVERSAMPLING_RATIO, OVERSAMPLING_ALGORITHM=OVERSAMPLING_ALGORITHM)
            X_test, y_test = preprocessing(self.day_df_embeddings, SCALING=SCALING)

            model = XGBClassifier(n_jobs=WORKERS)
            model.fit(X_train, y_train)
            auc_xg, f1_xg, lift_xg, fpr, tpr, thresholds, fig = testing(model, X_test, y_test)

            aucs_xg.append(auc_xg)
            f1s_xg.append(f1_xg)
            lifts_xg.append(lift_xg)

            try:
                os.mkdir(OUTPUT_DATA_PATH+"images")
            except FileExistsError:
                # directory already exists
                pass
            plt.savefig(OUTPUT_DATA_PATH+"images/"+OUTPUT_FILENAME+"_XGB"+"_iter_"+str(i)+'.png')
            plt.close()

            start_of_data += updategran

        # Report
        logger(OUTPUT_DATA_PATH+OUTPUT_FILENAME+"_XGB", aucs_xg, f1s_xg, lifts_xg, fraudcasestrain, fraudcasestest)

        #Signal completion
        ed = time.time()
        print("Finished: ", os.getpid())
        print("Runtime of process ", os.getpid(), " was ", (ed-st))


class random_forest:

    def __init__(self, ITERAT = 5, START='01/10/2013', UPDATEGRAN=5, INPUT_DATA_PATH="", OUTPUT_DATA_PATH="", OUTPUT_FILENAME="", UNDERSAMPLING_RATIO=0, OVERSAMPLING_ALGORITHM="", OVERSAMPLING_RATIO=0, SCALING="", WORKERS=3):

        st = time.time()
        timegran = datetime.timedelta(days=1)
        start_of_data = pd.to_datetime(START, dayfirst=True)
        #baseline = BASELINE*timegran
        updategran = UPDATEGRAN*timegran


        #df = pd.read_csv(output_path+"/input.csv", index_col=0, parse_dates=['timestamp'])
        aucs_rf = []
        f1s_rf = []
        lifts_rf = []
        trainsizes = []
        testsizes = []
        fraudcasestrain = []
        fraudcasestest = []

        for i in range(ITERAT):
            #Load datasets
            self.baseline_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'baseline_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')
            self.day_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'day_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')


            #logging
            #Record the test and train data size
            trainsizes.append(self.baseline_df_embeddings.shape[0])
            testsizes.append(self.day_df_embeddings.shape[0])
            fraudcasestrain.append(self.baseline_df_embeddings[self.baseline_df_embeddings.fraud == True].shape[0])
            fraudcasestest.append(self.day_df_embeddings[self.day_df_embeddings.fraud == True].shape[0])

            X_train, y_train = preprocessing(self.baseline_df_embeddings, UNDERSAMPLING_RATIO=UNDERSAMPLING_RATIO, SCALING=SCALING, OVERSAMPLING_RATIO=OVERSAMPLING_RATIO, OVERSAMPLING_ALGORITHM=OVERSAMPLING_ALGORITHM)
            X_test, y_test = preprocessing(self.day_df_embeddings, SCALING=SCALING)

            model = RandomForestClassifier(class_weight='balanced', n_estimators=100, n_jobs=WORKERS)
            model.fit(X_train, y_train)
            auc_rf, f1_rf, lift_rf, fpr, tpr, thresholds, fig = testing(model, X_test, y_test)

            aucs_rf.append(auc_rf)
            f1s_rf.append(f1_rf)
            lifts_rf.append(lift_rf)
            try:
                os.mkdir(OUTPUT_DATA_PATH+"images")
            except FileExistsError:
                # directory already exists
                pass
            plt.savefig(OUTPUT_DATA_PATH+"images/"+OUTPUT_FILENAME+"_random_forest"+"_iter_"+str(i)+'.png')
            plt.close()

            start_of_data += updategran

        # Report
        logger(OUTPUT_DATA_PATH+OUTPUT_FILENAME+"_random_forest", aucs_rf, f1s_rf,lifts_rf, fraudcasestrain, fraudcasestest)

        #Signal completion
        ed = time.time()
        print("Finished: ", os.getpid())
        print("Runtime of process ", os.getpid(), " was ", (ed-st))

class SVM:

    def __init__(self, ITERAT = 5, START='01/10/2013', UPDATEGRAN=5, INPUT_DATA_PATH="", OUTPUT_DATA_PATH="", OUTPUT_FILENAME="", UNDERSAMPLING_RATIO=0, OVERSAMPLING_ALGORITHM="", OVERSAMPLING_RATIO=0, SCALING="", WORKERS=3):

        st = time.time()
        timegran = datetime.timedelta(days=1)
        start_of_data = pd.to_datetime(START, dayfirst=True)
        #baseline = BASELINE*timegran
        updategran = UPDATEGRAN*timegran


        #df = pd.read_csv(output_path+"/input.csv", index_col=0, parse_dates=['timestamp'])
        aucs_svm = []
        f1s_svm = []
        lifts_svm = []
        trainsizes = []
        testsizes = []
        fraudcasestrain = []
        fraudcasestest = []

        for i in range(ITERAT):
            #Load datasets
            self.baseline_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'baseline_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')
            self.day_df_embeddings = pd.read_pickle(INPUT_DATA_PATH+'day_df_embeddings_'+start_of_data.strftime('%d%m%Y')+'.pkl')


            #logging
            #Record the test and train data size
            trainsizes.append(self.baseline_df_embeddings.shape[0])
            testsizes.append(self.day_df_embeddings.shape[0])
            fraudcasestrain.append(self.baseline_df_embeddings[self.baseline_df_embeddings.fraud == True].shape[0])
            fraudcasestest.append(self.day_df_embeddings[self.day_df_embeddings.fraud == True].shape[0])

            X_train, y_train = preprocessing(self.baseline_df_embeddings, UNDERSAMPLING_RATIO=UNDERSAMPLING_RATIO, SCALING=SCALING, OVERSAMPLING_RATIO=OVERSAMPLING_RATIO, OVERSAMPLING_ALGORITHM=OVERSAMPLING_ALGORITHM)
            X_test, y_test = preprocessing(self.day_df_embeddings, SCALING=SCALING)

            model = CalibratedClassifierCV(base_estimator=LinearSVC(penalty='l2', class_weight='balanced', dual=False), cv=5)
            model.fit(X_train, y_train)
            #model = SVC(class_weight='balanced', probability=True, kernel="linear") #dual=False)
            #model.fit(X_train, y_train)
            auc_svm, f1_svm, lift_svm, fpr, tpr, thresholds, fig = testing(model, X_test, y_test)

            aucs_svm.append(auc_svm)
            f1s_svm.append(f1_svm)
            lifts_svm.append(lift_svm)

            try:
                os.mkdir(OUTPUT_DATA_PATH+"images")
            except FileExistsError:
                # directory already exists
                pass
            plt.savefig(OUTPUT_DATA_PATH+"images/"+OUTPUT_FILENAME+"_SVM"+"_iter_"+str(i)+'.png')
            plt.close()

            start_of_data += updategran

        # Report
        logger(OUTPUT_DATA_PATH+OUTPUT_FILENAME+"_SVM", aucs_svm, f1s_svm, lifts_svm, fraudcasestrain, fraudcasestest)

        #Signal completion
        ed = time.time()
        print("Finished: ", os.getpid())
        print("Runtime of process ", os.getpid(), " was ", (ed-st))

def testing(model, X_test, y_test):

    pred_prob = model.predict_proba(X_test)[:,1]
    y_pred = model.predict(X_test)
    auc_lr = roc_auc_score(y_test, pred_prob)
    f1_lr = f1_score(y_test, y_pred)
    fpr, tpr, thresholds = roc_curve(y_test, pred_prob)

    #optimal_idx = np.argmax(np.abs(tpr - fpr))
    #optimal_threshold = thresholds[optimal_idx]
    #print("optimal threshold: ", optimal_threshold)
    #preds = np.where(pred_prob > THRESHOLD, 1, 0)

    #f1_bis = f1_score(y_test, preds)
    #print("F1: ", f1_bis)

    ###LIFT SCORE###
    cols = ['ACTUAL','PROB_POSITIVE','PREDICTED']
    data = [y_test,pred_prob,y_pred]
    df = pd.DataFrame(dict(zip(cols,data)))
    #print(df.tail(5))

    #Observations where y=1
    total_positive_n = df['ACTUAL'].sum()
    #print("Total fraud cases: ", total_positive_n)
    #Total Observations
    total_n = df.index.size
    natural_positive_prob = total_positive_n/float(total_n)

    #Sort values and take top 10%
    df_sorted = df.sort_values('PROB_POSITIVE', ascending=False).iloc[:int(np.round(0.1*total_n))]
    #print("total number in sample: ", df_sorted['PREDICTED'].count())
    #print("total correctly predicted: ", (df_sorted['PREDICTED'] & df_sorted['ACTUAL']).sum() )
    lift_positive = ((df_sorted['PREDICTED'] & df_sorted['ACTUAL']).sum())/(total_positive_n)
    percentage = ((df_sorted['ACTUAL'].count())/float(total_n))
    #print("pecentage: ", percentage)
    #print("percentage of total fraud in 10% : ", lift_positive)
    lift_index_positive = lift_positive/percentage   #(lift_positive/natural_positive_prob) #*100
    #if(lift_index_positive > 10):
        #print(lift_index_positive)

    ### Visualization ###
    f, (ax1, ax2, ax3, ax4) = plt.subplots(4,1, figsize=(5,20))
    y_pred_graphs = model.predict_proba(X_test)
    plot_lift_curve(y_test, y_pred_graphs, title='Lift Curve', ax=ax1)
    plot_cumulative_gain(y_test, y_pred_graphs, ax=ax2)
    plot_roc(y_test, y_pred_graphs, plot_micro=False, plot_macro=False, classes_to_plot=[True], ax=ax3)
    plot_precision_recall(y_test, y_pred_graphs, ax=ax4)
    ### --- ###

    return (auc_lr, f1_lr, lift_index_positive, fpr, tpr, thresholds, f)

def preprocessing(df, UNDERSAMPLING_RATIO=0, SCALING="", OVERSAMPLING_RATIO=0, OVERSAMPLING_ALGORITHM=""):

    if UNDERSAMPLING_RATIO:
        print("undersampling")
        non_fraud_indices = df[df.fraud == False].index
        sample_size = int(np.round(np.sum(df.fraud == True)*UNDERSAMPLING_RATIO))
        random_indices = np.random.choice(non_fraud_indices, sample_size, replace=False)
        non_fraud_sample = df.loc[random_indices]
        fraud_sample = df[df.fraud == True]

        df = pd.concat([non_fraud_sample, fraud_sample])
        df = df.sample(frac=1)

    try:
        df = df.drop(["scores_ST","scores_MT","scores_LT"], axis=1)
    except:
        pass

    X_train = df.drop(["transaction", "client", "merchant", "category","country","amount","timestamp","fraud"], axis=1).values

    if SCALING == 'min_max_scaler':
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train = min_max_scaler.fit_transform(X_train)
    elif SCALING == 'standard_scaler':
        standard_scaler = StandardScaler()
        X_train = standard_scaler.fit_transform(X_train)

    y_train = df.fraud

    if OVERSAMPLING_RATIO:
        print("oversampling")
        if OVERSAMPLING_ALGORITHM == "RandomOverSampler":

            ros = RandomOverSampler(sampling_strategy=(1/OVERSAMPLING_RATIO), random_state=0)
            X_train, y_train = ros.fit_resample(X_train, y_train)
        elif OVERSAMPLING_ALGORITHM == "SMOTE":

            smote = SMOTE(sampling_strategy=(1/OVERSAMPLING_RATIO))
            X_train, y_train = smote.fit_resample(X_train, y_train)
        elif OVERSAMPLING_ALGORITHM == "ADASYN":

            adasyn = ADASYN(sampling_strategy=(1/OVERSAMPLING_RATIO))
            X_train, y_train = adasyn.fit_resample(X_train, y_train)

    return (X_train, y_train)

def logger(filename, aucs, f1s, lifts, fraudcasestrain, fraudcasestest):
    logs = OrderedDict()
    logs["auc"] = aucs

    logs["f1"] = f1s
    logs["lift@10%"] = lifts
    logs["number_of_fraud_cases_train"] = fraudcasestrain
    logs["number_of_fraud_cases test"] = fraudcasestest

    print("saving file")
    with open(filename+'.json', 'w') as out:
        json.dump(logs, out)
        out.close()
