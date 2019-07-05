#!/usr/bin/env python

class BasicAnalysis:
    
    def __init__(self, df, pred=None, resp=None, tsts=0.25):
        self.df = df
        self.pred = pred if pred is not None else [i for i in range(len(df.columns) - 1)]
        self.resp = resp if resp is not None else [len(df.columns) - 1]
        self.tsts = tsts
        
        # importing important and also basic libraries for data processing
        
        import pandas as pd
        import numpy as np
        import warnings
        warnings.filterwarnings('ignore')
        from sklearn.model_selection import train_test_split
        from sklearn import preprocessing
        
        # Pre-processing
        
        encode = preprocessing.LabelEncoder()
        
        predictors = df.iloc[:, self.pred]
        predictions = df.iloc[:, self.resp]

        X_train, X_test, y_train, y_test = train_test_split(predictors,
                                                            predictions,
                                                            test_size=self.tsts,
                                                            random_state=1)

        X_train = X_train.apply(encode.fit_transform)
        y_train = y_train.apply(encode.fit_transform)

        X_test = X_test.apply(encode.fit_transform)
        y_test = y_test.apply(encode.fit_transform)
        
        # Just looking

        for idx, col in enumerate(predictions.columns):
            print('Train data distribution:')
            td = pd.concat([predictions[col].value_counts(),
                            round(predictions[col].value_counts(normalize=True) * 100, 2)], axis=1)
            td.columns = ['Counts', 'Percentage']
            print(td)
        
        # Defining the metrics and models
        
        models = pd.DataFrame(data = {'Model' : ['Decision Trees', 'Logistic Regression', 'Naive-Bayes', 'SVM',
                                                 'Neural Netwoks', 'K-NN', 'Random Forest', 'Adaboost'],
                                      'attr' : ['tree', 'linear_model', 'naive_bayes', 'svm', 'neural_network',
                                                'neighbors', 'ensemble', 'ensemble'],
                                      'class' : ['DecisionTreeClassifier', 'LogisticRegression', 'GaussianNB',
                                                 'SVC', 'MLPClassifier', 'KNeighborsClassifier',
                                                 'RandomForestClassifier', 'AdaBoostClassifier']})

        metrics = {'Accuracy' : 'accuracy_score', 'Precision' : 'precision_score',
                   'Jaccard Score' : 'jaccard_similarity_score', 'F1_Score' : 'f1_score','R Value' : 'matthews_corrcoef',
                   'ROC AUC' : 'roc_auc_score', 'MSE' : 'mean_squared_error', 'Log Loss' : 'log_loss'}
        
        score = pd.DataFrame(columns=models['Model'], index=list(metrics.keys()))

        for i in range(len(models)):
            
            # Importing models
            
            __import__("sklearn." + models['attr'][i])
            attr = getattr(__import__("sklearn"), models['attr'][i])
            model = getattr(attr, models['class'][i])
            
            # Assigning the model and getting the metrics
            
            model=model()
            y_pred = model.fit(X_train, y_train.values.ravel()).predict(X_test)

            for j, each in enumerate(metrics):
                
                # Importing metrics
                
                __import__("sklearn.metrics")
                attr = getattr(__import__("sklearn"), 'metrics')
                metric = getattr(attr, metrics[each])

                score.loc[each, models['Model'][i]] = round(metric(y_test, y_pred), 2)
        
        if __name__ == "__main__":

            print('')
            print(score.to_string())

        else:

            print('')
            print(score.to_string())

