# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt

from renom_q.exception import ReNomQError
from .qaa import QAA


class QSVM(QAA):
    """ Quantum Support Vector Machine

    Args:
        set_qasm (boolean):
            If it is true, qasm code is added to the calculation result.
            Defaults to False.

    Example:
        >>> import renom_q.ml.qsvm
        >>> qsvm = renom_q.ml.qsvm.QSVM(True)
    """

    def __init__(self, set_qasm=False):
        self.set_qasm = set_qasm
        self.train_dict = None

    def plot_graph(self, x_train=None, y_train=None, x_test=None, y_pred=None):
        """ Draw a graph of data used in quantum SVM algorithm

        Args:
            x_train (array or list):
                A array of train data. Defaults to None.
            y_train (array or list):
                A list of labels of train data. Defaults to None.
            x_test (array or list):
                A array of test data. Defaults to None.
            y_pred (array or list):
                A list of labels of test data. Defaults to None.

        Returns:
            matplotlib.figure:
                A matplotlib figure object of a graph of data used in quantum
                SVM algorithm.

        Example:
            >>> import renom_q.ml.qsvm
            >>> qsvm = renom_q.ml.qsvm.QSVM()
            >>> x_train = [[5, 4], [6, 6], [4, 9], [8, 1]]
            >>> y_train = [1, -1, 1, -1]
            >>> qsvm.plot_graph(x_train, y_train)
        """
        if x_train is not None and y_train is not None and x_test is not None and y_pred is not None:
            x_train = np.array(x_train).T
            x_test = np.array(x_test).T
            array = np.hstack((x_train, x_test))
            plt.xlabel("x")
            plt.ylabel("y")
            plt.xlim([sorted(array[0])[0]-1, sorted(array[0])[-1]+1])
            plt.ylim([sorted(array[1])[0]-1, sorted(array[1])[-1]+1])
            bn1 = x_train.shape[1]
            bn2 = x_test.shape[1]

            handles = []
            labels = ['-1_train', '1_train', '-1_test', '1_test']
            label_a = True
            label_b = True
            label_c = True
            label_d = True

            for i in range(bn1):
                if y_train[i] == -1:
                    a, = plt.plot(x_train[0][i], x_train[1][i], "s", color='black',
                                  markerfacecolor='red', markersize=10)
                    if label_a:
                        handles.append(a)
                        label_a = False
                else:
                    b, = plt.plot(x_train[0][i], x_train[1][i], "s", color='black',
                                  markerfacecolor='cyan', markersize=10)
                    if label_b:
                        handles.append(b)
                        label_b = False

            for i in range(bn2):
                if y_pred[i] == -1:
                    c, = plt.plot(x_test[0][i], x_test[1][i], "ro", markersize=10)
                    if label_c:
                        handles.append(c)
                        label_c = False
                else:
                    d, = plt.plot(x_test[0][i], x_test[1][i], "co", markersize=10)
                    if label_d:
                        handles.append(d)
                        label_d = False

        elif x_test is None and y_pred is None:
            x_train = np.array(x_train).T
            bn = x_train.shape[1]
            plt.xlabel("x")
            plt.ylabel("y")
            plt.xlim([sorted(x_train[0])[0]-1, sorted(x_train[0])[-1]+1])
            plt.ylim([sorted(x_train[1])[0]-1, sorted(x_train[1])[-1]+1])
            handles = []
            labels = ['-1_train', '1_train']
            label_a = True
            label_b = True

            for i in range(bn):
                if y_train[i] == -1:
                    a, = plt.plot(x_train[0][i], x_train[1][i], "s", color='black',
                                  markerfacecolor='red', markersize=10)
                    if label_a:
                        handles.append(a)
                        label_a = False
                else:
                    b, = plt.plot(x_train[0][i], x_train[1][i], "s", color='black',
                                  markerfacecolor='cyan', markersize=10)
                    if label_b:
                        handles.append(b)
                        label_b = False

        elif x_train is None and y_train is None:
            x_test = np.array(x_test).T
            bn = x_test.shape[1]
            plt.xlabel("x")
            plt.ylabel("y")
            plt.xlim([sorted(x_test[0])[0]-1, sorted(x_test[0])[-1]+1])
            plt.ylim([sorted(x_test[1])[0]-1, sorted(x_test[1])[-1]+1])
            handles = []
            labels = ['-1_test', '1_test']
            label_a = True
            label_b = True

            for i in range(bn):
                if y_pred[i] == -1:
                    a, = plt.plot(x_test[0][i], x_test[1][i], "ro", markersize=10)
                    if label_a:
                        handles.append(a)
                        label_a = False
                else:
                    b, = plt.plot(x_test[0][i], x_test[1][i], "co", markersize=10)
                    if label_b:
                        handles.append(b)
                        label_b = False

        plt.legend(handles, labels, bbox_to_anchor=(0.8, 0.5, 0.5, .100))
        plt.show()

    def fit(self, train_data, train_label):
        """ Setting training data used in quantum SVM algorithm

        Args:
            train_data (array or list):
                A array of train data.
            train_label (array or list):
                A list of labels of train data.

        Example:
            >>> import renom_q.ml.qsvm
            >>> qsvm = renom_q.ml.qsvm.QSVM()
            >>> x_train = [[5, 4], [6, 6], [4, 9], [8, 1]]
            >>> y_train = [1, -1, 1, -1]
            >>> qsvm.fit(x_train, y_train)
        """
        self.y_train = np.array(train_label)
        self.x_train = np.array(train_data).T
        train_dict = {}
        for i in range(self.x_train.shape[1]):
            train_dict[str(self.x_train[:, i])] = train_label[i]

        self.train_dict = train_dict

    def predict(self, test_data):
        """ Predict labels of test data using training data

        Args:
            test_data (array or list):
                A array of test data.

        Returns:
            y_pred (list):
                A list of labels of test data.

        Example:
            >>> import renom_q.ml.qsvm
            >>> qsvm = renom_q.ml.qsvm.QSVM()
            >>> x_train = [[5, 4], [6, 6], [4, 9], [8, 1]]
            >>> y_train = [1, -1, 1, -1]
            >>> qsvm.fit(x_train, y_train)
            >>> x_test = [[3, 2], [7, 1], [5, 2], [1, 3]]
            >>> qsvm.predict(x_test)
            [1, -1, 1, 1]
        """
        if self.train_dict is None:
            raise ReNomQError("this function is only available after using the ",
                              "QSVM.fit() function")
        x_test = np.array(test_data)
        y_pred = []
        result_dict = {}
        for test in x_test:
            if str(test) in self.train_dict:
                y_pred.append(self.train_dict[str(test)])
                continue

            A = np.hstack((self.x_train, np.array([test]).T))
            bn = A.shape[1]
            J = np.zeros((bn, bn))
            for i in range(bn):
                for j in range(bn):
                    if i < j:
                        u = A[:, i]
                        v = A[:, j]
                        d = scipy.spatial.distance.euclidean(u, v)
                        if d == 0:
                            J[j][i] = J[i][j] = 0
                        else:
                            J[j][i] = J[i][j] = 1/d

            hz = np.append(self.y_train, 0)
            result = self.qaa(J, hz=-hz, hx=1, maxcut_mode=True, set_qasm=self.set_qasm)
            result_dict[str(test)] = result

            label = 2*result['solution']-1
            label = list(label)

            change_label = []
            for i in range(bn):
                if hz[i] != label[i]:
                    change_label.append(i)

            if len(change_label) > bn/2:
                label = list(-np.array(label))

            y_pred.append(-label[-1])

        self.result = result_dict

        return y_pred
