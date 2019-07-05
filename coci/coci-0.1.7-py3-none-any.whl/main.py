import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
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
        self._y = None
        self._sensitivities = None
        self._idx = None
        self._sample_size = None

        self.feature_names = None


    def sensitivity(self, x, feature_names=None, split_num=2, sample_size=None):
        '''

        :param x:
        :param feature_names:
        :param split_num:
        :param sample_size:
        :return:
        '''

        self._split_num = split_num

        if sample_size is None:
            if len(x) < 500:
                self._sample_size = len(x)
            else:
                self._sample_size = 500
        else:
            self._sample_size = sample_size

        idx = np.random.RandomState(seed=42).permutation(len(x))[:int(self._sample_size/self._split_num)]

        self._x = x[idx]

        if feature_names is not None:
            assert x.shape[1] == len(feature_names), "feature_name has different length from x features length"
            self.feature_names = feature_names
        else:
            self.feature_names = np.arange(x.shape[1])

        self._y = self._model.predict(self._x)

        self.sensitivity_ranges = get_sensitivity_ranges(self._x, self._split_num)

        self.sensitivity_analysis()

    def sensitivity_analysis(self):
        '''

        :return:
        '''

        _sensitivities = []

        cnt = 1
        len_x = self._x.shape[1]

        for col in range(len_x):

            if len(self.sensitivity_ranges[col]) != 0:

                progress_bar("Analyzing sensitivity: {}/{}".format(cnt, len_x), cnt / len_x)
                cnt += 1

                lis_x = []
                lis_y = []

                importance = self._model.feature_importance()

                if importance[col] == 0:
                    pass
                else:
                    for sr in self.sensitivity_ranges[col]:
                        tmp_x = self._x.copy()

                        delta_x = sr - tmp_x[:, col]

                        tmp_x[:, col] = sr

                        delta_y = self._model.predict(tmp_x) - self._y

                        lis_x += list(delta_x)
                        lis_y += list(delta_y)

                _sensitivities.append(np.array([lis_x, lis_y]))

        # sort by mean delta y
        y_mean = np.array([abs(s[1]).mean() for s in _sensitivities])
        y_mean[np.isnan(y_mean)] = 0

        self.y_mean = y_mean.argsort()[::-1]

        self._sensitivities = _sensitivities

    def trend_plot(self, max_display=None, feature_index=None, feature_name=None, jitter=0, x_estimator=False):

        assert feature_name is not None \
               or feature_index is not None\
                or max_display is not None, "The trend plot requires only one of feature_index or feature_name"

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

            s = self._sensitivities[idx]

            hue_norm = ((s[0] + abs(s[0].min())) / (s[0].max() + abs(s[0].min()))) - 0.5

            x += list(s[0].astype('float'))
            y += list(s[1].astype('float'))
            hue += list(hue_norm)


            df = pd.DataFrame(list(zip(x, y, hue)), columns=[feature, 'Sensitivity', 'color'])

            # get coeffs of linear fit
            reg = LinearRegression()
            reg.fit(np.array(x).reshape(-1, 1), y)
            intercept = reg.intercept_
            coeff = reg.coef_[0]

            if x_estimator:
                x_estimator = np.mean
            else:
                x_estimator = None

            ax = sns.lmplot(
                x=feature, y='Sensitivity',
                # hue='color',
                data=df,
                fit_reg=True,
                # palette=self.palette,
                x_jitter=jitter,
                x_estimator=x_estimator,
                scatter_kws={'color':'g'},
                line_kws={'label': "y={0:.9f}x+{1:.9f}".format(coeff, intercept)}
            )

            ax.add_legend()

        plt.show()

    def summary_plot(self, max_display=10):
        '''

        :param max_display:
        :return:
        '''

        if max_display is None:
            max_display = len(self.idx)

        fig, ax = plt.subplots(figsize=(10, max_display * 3))

        x = []
        y = []
        hue = []

        self.hue = []

        for id_ in self.y_mean[:max_display]:

            s = self._sensitivities[id_]

            hue_norm = ((s[0] + abs(s[0].min())) / (s[0].max() + abs(s[0].min()))) - 0.5

            hue_norm[hue_norm > 0] = 100
            hue_norm[hue_norm < 0] = -100

            x += list(s[1].astype('float'))
            y += list(np.full(len(s[1]), fill_value=self.feature_names[id_]))
            hue += list(hue_norm)

            self.hue.append(hue)

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























