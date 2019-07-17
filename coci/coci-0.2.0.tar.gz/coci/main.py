import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
from catboost import Pool
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def progress_bar(barname, rate):
    '''
    :param barname:
    :param rate:
    :return:
    '''
    num = int(rate/0.05) + 1
    bar = ('#' * num).ljust(20, '-')
    sys.stdout.write(f'\r{barname} : [{bar}] {rate*100:.2f}%')

def get_sensitivity_ranges(x, split_num):
    '''

    :param x:
    :param split_num:
    :return:
    '''

    min_x = x.min(axis=0)
    max_x = x.max(axis=0)

    minmax = np.vstack([min_x, max_x]).T

    sensitivity_ranges = []

    len_x = x.shape[1]
    cnt = 1

    for row in minmax:

        progress_bar("Loading sensitivity ranges: {}/{}".format(cnt, len_x), cnt/len_x)
        cnt += 1

        min_ = row[0]
        max_ = row[1]

        sensitivity_ranges.append(np.linspace(min_, max_, num=split_num))

    print()

    return sensitivity_ranges


class TreeExplainer():

    def __init__(self, model):
        '''

        :param model:
        '''

        self._model = model

        self.palette = sns.diverging_palette(255, 0, sep=1, n=3)
        self.cmap = sns.diverging_palette(255, 0, as_cmap=True)

        self._x = None
        self._x_array = None
        self._y = None
        self._sensitivities = None
        self._idx = None
        self._sample_size = None

        self.feature_names = None

        if 'catboost' in str(type(model)):
            self.model_type = 'catboost'
        elif 'lightgbm' in str(type(model)):
            self.model_type = 'lightgbm'

        assert self.model_type is not None

    def sensitivity(self, x, feature_names=None, split_num=2, sample_size=None, label_names=None):
        '''

        :param x:
        :param feature_names:
        :param split_num:
        :param sample_size:
        :return:
        '''

        if type(x) is list:
            self._x_array = np.array(x)
        elif 'catboost.core.Pool' in str(type(x)):
            self._x_array = x.get_features()
        elif 'numpy.ndarray' in str(type(x)):
            self._x_array = x

        self._split_num = split_num

        if sample_size is None:
            if self._x_array.shape[0] < 500:
                self._sample_size = len(x)
            else:
                self._sample_size = 500
        else:
            self._sample_size = sample_size

        idx = np.random.RandomState(seed=42).permutation(len(self._x_array))[:int(self._sample_size/self._split_num)]

        self._x_array = self._x_array[idx]

        if 'catboost.core.Pool' in str(type(x)):
            self._x = Pool(self._x_array)
        else:
            self._x = self._x_array

        if feature_names is not None:
            assert self._x_array.shape[1] == len(feature_names), "feature_name has different length from x features length"
            self.feature_names = feature_names
        else:
            self.feature_names = np.arange(self._x_array.shape[1])

        if label_names is not None:
            self.label_names = label_names
        else:
            self.label_names = None

        if self.model_type == 'lightgbm':
            self._y = self._model.predict(self._x)
        elif self.model_type == 'catboost':
            self._y = self._model.predict(self._x, prediction_type='Probability')

        self.sensitivity_ranges = get_sensitivity_ranges(self._x_array, self._split_num)

        self.sensitivity_analysis()

    def sensitivity_analysis(self):
        '''

        :return:
        '''

        _sensitivities = []

        try:
            y_class = len(self._y[0])
        except:
            y_class = 1

        cnt = 1
        len_x = self._x_array.shape[1]

        for col in range(len_x):

            if len(self.sensitivity_ranges[col]) != 0:

                progress_bar("Analyzing sensitivity: {}/{}".format(cnt, len_x), cnt / len_x)
                cnt += 1

                lis_x = []
                lis_y = [[] for _ in range(y_class)]

                if self.model_type == 'lightgbm':
                    importance = self._model.feature_importance()
                elif self.model_type == 'catboost':
                    importance = self._model.get_feature_importance()

                if importance[col] == 0:
                    pass
                else:
                    for sr in self.sensitivity_ranges[col]:

                        tmp_x = self._x_array.copy()

                        delta_x = sr - tmp_x[:, col]

                        # print('tmp_x', tmp_x[:, col])

                        tmp_x[:, col] = sr

                        if 'catboost.core.Pool' in str(type(self._x)):
                            tmp_x = Pool(tmp_x)
                        else:
                            tmp_x = tmp_x

                        # try:
                        if self.model_type == 'lightgbm':
                            pred_y = self._model.predict(tmp_x)
                        elif self.model_type == 'catboost':
                            pred_y = self._model.predict(tmp_x, prediction_type='Probability')

                        delta_y = np.subtract(pred_y, self._y)

                        lis_x += list(delta_x)

                        for i in range(y_class):

                            try:
                                lis_y[i] += list(delta_y[:, i].flatten())
                            except:
                                lis_y[i] += list(delta_y.flatten())

                        # except Exception as e:
                        #     print('Error', str(e))

                _sensitivities.append([np.array(lis_x), np.array(lis_y)])

        # sort by mean delta y
        y_mean = np.array([abs(s[1]).mean() for s in _sensitivities])
        y_mean[np.isnan(y_mean)] = 0

        self.y_mean = y_mean.argsort()[::-1]

        self._sensitivities = _sensitivities

    def export_csv(self, file_name, max_display=None):

        if max_display is None:
            max_display = self._x_array.shape[1]

        cat_num = len(self._sensitivities[0][1])
        feature_names = self.feature_names

        dfs = {i: pd.DataFrame() for i in range(cat_num)}

        for idx in self.y_mean[:max_display]:

            val = self._sensitivities[idx]

            x = val[0]
            y = val[1]

            for y_num in range(cat_num):
                tmp_df = pd.DataFrame(list(zip(x, y[y_num])))
                columns = [(feature_names[idx], 'delta_x'), (feature_names[idx], 'delta_y')]
                tmp_df.columns = pd.MultiIndex.from_tuples(columns)

                dfs[y_num] = pd.concat([dfs[y_num], tmp_df], axis=1)

        for idx, df in dfs.items():

            if self.label_names is not None:
                save_file_name = file_name + "_" + self.label_names[idx] + '.csv'
            else:
                save_file_name = file_name + "_" + idx + '.csv'

            df.to_csv(save_file_name)



    def trend_plot(self, max_display=None, feature_index=None, feature_name=None, jitter=0, x_estimator=False):

        assert feature_name is not None \
               or feature_index is not None\
                or max_display is not None, "The trend plot requires only one of feature_index or feature_name"

        y_len = len(self._sensitivities[0][1])

        if feature_index is not None:
            if isinstance(feature_index, list):
                idxes = feature_index
            else:
                idxes = [feature_index]
        elif feature_name is not None:
            if isinstance(feature_name, list):
                idxes = [self.feature_names.index(name) for name in feature_name]
            else:
                idxes = [self.feature_names.index(feature_name)]
        elif max_display is not None:
            idxes = self.y_mean[:max_display]

        for idx in idxes:

            feature = '△' + self.feature_names[idx]
            x = []
            y = []
            hue = []
            target = []
            intercept = []
            coeff = []

            for y_idx in range(y_len):

                s = self._sensitivities[idx]

                hue_norm = ((s[0] + abs(s[0].min())) / (s[0].max() + abs(s[0].min()))) - 0.5

                x += list(s[0].astype('float'))
                y += list(s[1][y_idx].astype('float'))
                hue += list(hue_norm)
                target += list(np.full(len(s[1]), fill_value=y_idx))

                # get coeffs of linear fit
                reg = LinearRegression()
                reg.fit(np.array(x).reshape(-1, 1), y)
                intercept.append(reg.intercept_)
                coeff.append(reg.coef_[0])

            df = pd.DataFrame(list(zip(x, y, hue, target)), columns=[feature, 'Sensitivity', 'color', 'target'])

            if x_estimator:
                x_estimator = np.mean
            else:
                x_estimator = None

            # print(x, y)

            g = sns.FacetGrid(df, col='target', col_wrap=2)

            g.map(sns.lmplot,
                  feature,
                  'Sensitivity',
                  # color='g',
                  # fit_reg=True,
                  # x_jitter=jitter,
                  # x_estimator=x_estimator
                  )

            g.set(yticks=[-1, -.5, 0, .5, 1])

            # sns.lmplot(
            #     x=feature, y='Sensitivity',
            #     hue='target',
            #     data=df,
            #     fit_reg=True,
            #     # palette=self.palette,
            #     x_jitter=jitter,
            #     x_estimator=x_estimator,
            #     # scatter_kws={'color':'g'},
            #     # line_kws={'label': "y={0:.9f}x+{1:.9f}".format(coeff, intercept)}
            # )

        plt.show()

    def summary_bar_plot(self, max_display=10):

        x = []
        y = []
        target = []

        try:
            y_len = len(self._sensitivities[0][1])
        except:
            y_len = 1

        for id_ in self.y_mean[:max_display]:

            s = self._sensitivities[id_]

            for y_idx in range(y_len):

                target.append(y_idx)

                try:
                    x.append(abs(s[1][y_idx]).mean())
                except:
                    x.append(abs(s[1]).mean())

                y.append(self.feature_names[id_])

        df = pd.DataFrame(list(zip(target, x, y)), columns=['target', 'sensitivity', 'Features'])

        df = pd.pivot_table(df, index=['Features'], columns=['target'], values=['sensitivity'])

        df['sum'] = df.sum(axis=1)

        df = df.sort_values(by=['sum']).drop(columns=['sum'])
        df.columns = df.columns.get_level_values(1)

        sns.set()
        ax = df.plot.barh(stacked=True, title='Summary Bar Plot', width=.5, figsize=(10, max_display))
        ax.set_xlabel("mean(|sensitivity|)")

        plt.show()

    def summary_scatter_plot(self, max_display=10):

        fig, ax = plt.subplots(figsize=(10, max_display * 3))

        x = []
        y = []
        hue = []

        try:
            y_len = len(self._sensitivities[0][1])
        except:
            y_len = 1

        for id_ in self.y_mean[:max_display]:

            s = self._sensitivities[id_]

            for y_idx in range(y_len):

                hue_norm = ((s[0] + abs(s[0].min())) / (s[0].max() + abs(s[0].min()))) - 0.5

                hue_norm[hue_norm > 0] = 100
                hue_norm[hue_norm < 0] = -100

                try:
                    x += list(s[1][y_idx].astype('float'))
                except:
                    x += list(s[1].astype('float'))

                y += list(np.full(len(s[1]), fill_value=self.feature_names[id_]))
                hue += list(hue_norm)

        sns.swarmplot(
            x=x, y=y,
            hue=hue,
            palette=self.palette,
        )

        fig.set_size_inches(10, max_display)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ## create colorbar ##
        plt.legend('')
        divider = make_axes_locatable(plt.gca())
        ax_cb = divider.new_horizontal(size="1%", pad=0.05)
        fig.add_axes(ax_cb)
        cb1 = matplotlib.colorbar.ColorbarBase(ax_cb, cmap=self.cmap, ticks=[0, 1], orientation='vertical')
        cb1.ax.set_yticklabels(['Low', 'High'])
        cb1.set_label('Feature Value Changes')
        plt.show()


    def summary_plot(self, max_display=10):
        '''

        :param max_display:
        :return:
        '''

        if max_display is None:
            max_display = self._x_array.shape[1]

        if len(self._sensitivities[0][1]) > 1:
            self.summary_bar_plot(max_display=max_display)
        else:
            self.summary_scatter_plot(max_display=max_display)

























