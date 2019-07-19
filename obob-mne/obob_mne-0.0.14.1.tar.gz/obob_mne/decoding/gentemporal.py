# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the obob_mne Project, see:
# https://gitlab.com/obob/obob_mne
#
# obob_mne is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# obob_mne is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with obob_mne. If not, see <http://www.gnu.org/licenses/>.

import mne
import numpy
import copy
import logging
import collections
import scipy.stats

from .temporal import TemporalArray
from.helpers import _get_Y_from_metadata


class GeneralizedTemporalArray(mne.utils.SizeMixin):
    """Base class for Temporal Generalization Decoding.

    Parameters
    ----------
    scores_raw : :class:`numpy.ndarray` shape (n_times, n_times) or \
                (n_folds, n_times, n_times)
        Classifier accuracies.
    scoring_name : str
        Name of the scoring function (i.e. Accuracy...)
    n_classes : int
        Number of classes of the classification
    c_factors_training : str
        Name of the factors over which was collapsed in the training set
    weights : :class:`numpy.ndarray` shape (n_channels, n_times)
        Classifier weights
    info : dict
        Info dict
    times_training : :class:`numpy.ndarray` shape (n_times)
        Array of times in seconds of the training data
    tmin : int
        ???
    times_testing : None or :class:`numpy.ndarray` shape (n_times)
        Array of times in seconds of the testing data. If ``None``,
        it is copied from times_training.
    c_factors_testing : None or str
        Name of the factors over which was collapsed in the testing set.
        If ``None``, it is copied from c_factors_training.
    nave : int
        Number of epochs in the training set.
    nave_testing : int or None
        Number of epochs in the testing set. If ``None``, it is copied
        from nave.
    """

    def __init__(self, scores_raw, scoring_name, n_classes, c_factors_training,
                 weights, info, times_training, tmin,
                 times_testing=None, c_factors_testing=None, nave=1,
                 nave_testing=None):
        self._scores_raw = scores_raw
        self._scoring_name = scoring_name
        self._nclasses = n_classes
        self._c_factors_training = c_factors_training
        self._weights = weights
        if c_factors_testing is None:
            self._c_factors_testing = self._c_factors_training
        else:
            self._c_factors_testing = c_factors_testing

        self._times_training = times_training
        if times_testing is None:
            self._times_testing = self._times_training
        else:
            self._times_testing = times_testing

        self._info = info
        self._tmin = tmin
        self._nave = nave

        if nave_testing is None:
            nave_testing = nave

        self._nave_testing = nave_testing

    @property
    def info(self):
        """:class:`Measurement info <mne.Info>`"""
        return self._info

    @property
    def tmin(self):
        """float: tmin"""
        return self._tmin

    @property
    def nave(self):
        """int: Number of epochs in the training set."""
        return self._nave

    @property
    def nave_testing(self):
        """int: Number of epochs in the testing set."""
        return self._nave_testing

    @property
    def scores(self):
        """:class:`numpy.ndarray`: The scores of the classification"""
        if self._scores_raw.ndim <= 2:
            return self._scores_raw
        else:
            return numpy.average(self._scores_raw, axis=0)

    @property
    def weights(self):
        """:class:`numpy.ndarray`:The classifier weights"""
        return self._weights

    @property
    def chance_level(self):
        """float: The chance level of the classifier."""
        return 1.0 / self._nclasses

    def diagonal_as_temporal(self):
        """Return the non-generalized results."""
        if self._scores_raw.ndim == 2:
            raw_scores = numpy.diagonal(self._scores_raw)
        else:
            raw_scores = numpy.diagonal(self._scores_raw, axis1=1, axis2=2)

        return TemporalArray(raw_scores=raw_scores,
                             weights=self.weights,
                             n_classes=self._nclasses,
                             info=self.info,
                             tmin=self.tmin,
                             scoring_name=self._scoring_name,
                             nave=self.nave,
                             nave_testing=self.nave_testing,
                             c_factors_training=self._c_factors_training,
                             c_factors_testing=self._c_factors_testing
                             )

    def get_temporal_from_training_interval(self, tmin, tmax):
        """Average the scores of a training interval.

        Parameters
        ----------
        tmin : int
            Start time in seconds of the training interval to average.
        tmax : int
            End time in seconds of the training interval to average.

        Returns
        -------
        data : instance of :class:`TemporalArray`
            The :class:`TemporalArray` with the averaged scores.
        """
        time_idx = numpy.where(
            numpy.logical_and(
                self._times_training >= tmin,
                self._times_training <= tmax))[0]
        if self._scores_raw.ndim == 2:
            raw_scores = numpy.mean(self._scores_raw[time_idx, :], axis=0)
        else:
            raw_scores = numpy.mean(self._scores_raw[:, time_idx, :], axis=1)

        return TemporalArray(raw_scores=raw_scores,
                             weights=self.weights,
                             n_classes=self._nclasses,
                             info=self.info,
                             tmin=self.tmin,
                             scoring_name=self._scoring_name,
                             nave=self.nave,
                             nave_testing=self.nave_testing,
                             c_factors_training=self._c_factors_training,
                             c_factors_testing=self._c_factors_testing
                             )

    def _plot_image(self, values, axes=None, show=True, cmap='Reds',
                    colorbar=True,
                    interpolation='bessel'):
        import matplotlib.pyplot as plt

        if not isinstance(axes, plt.Axes):
            fig, axes = plt.subplots(1, 1)
        else:
            fig = axes.get_figure()

        im = axes.imshow(values, interpolation=interpolation, origin='lower',
                         cmap=cmap,
                         extent=numpy.append(self._times_training[[0, -1]],
                                             self._times_testing[[0, -1]]),
                         aspect='auto')

        xlabel = 'Testing time (s)'
        ylabel = 'Training time (s)'

        if self._c_factors_testing:
            xlabel = '\n'.join([self._c_factors_testing, xlabel])

        if self._c_factors_training:
            ylabel = '\n'.join([self._c_factors_training, ylabel])

        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        axes.set_title('Temporal Generalization')
        axes.axvline(0, color='k')
        axes.axhline(0, color='k')
        old_xlim = axes.get_xlim()
        old_ylim = axes.get_ylim()
        axes.plot(axes.get_xlim(), axes.get_ylim(), color='k')
        axes.set_xlim(old_xlim)
        axes.set_ylim(old_ylim)
        if colorbar:
            plt.colorbar(im, ax=axes)

        if show:
            plt.show()

        return fig

    def plot_scores(self, axes=None, show=True, cmap='Reds', colorbar=True,
                    mask_below_chance=False, interpolation='bessel'):
        """Plot the scores as a Matrix.

        Parameters
        ----------
        axes : :class:`matplotlib.axes.Axes` or None, optional
            The axes where to draw the plot. If ``None``, a new figure is
            created.
        show : bool, optional
            True to actually show the plot.
        cmap : str or :class:`matplotlib.colors.Colormap`, optional
            The colormap.
        colorbar : bool, optional
            Whether to draw the colorbar.
        mask_below_chance : bool, optional
            If True, values below chance level get masked.
        interpolation : str, optional
            The interpolation method used.
        """
        scores = self.scores

        if mask_below_chance:
            scores = numpy.ma.masked_less(scores, self.chance_level)

        return self._plot_image(values=scores, axes=axes, show=show, cmap=cmap,
                                colorbar=colorbar, interpolation=interpolation)


class GeneralizedTemporalFromCollection(GeneralizedTemporalArray):
    """Base class for Temporal Generalization data from multiple subjects.

    The individual elements must match in number of classes, times etc.

    Parameters
    ----------
    data_list : iterable of :class:`GeneralizedTemporalArray`
        A list (or any other iterable) of :class:`GeneralizedTemporalArray`
    raw_scores : :class:`numpy.ndarray` shape (n_channels, n_times) or \
                (n_folds, n_channels, n_times)
        The already processed (i.e., averaged, statistically tested) scores.
    weights : :class:`numpy.ndarray` shape (n_channels, n_times)
        The already processed (i.e., averaged, statistically tested) weights.
    """

    must_be_equal = ['_scoring_name', '_nclasses', '_c_factors_training',
                     '_times_training', 'tmin', '_times_testing',
                     '_c_factors_testing']

    def __init__(self, data_list, raw_scores, weights):
        if not all(isinstance(item, GeneralizedTemporalArray) for item in
                   data_list):
            raise TypeError('Only GeneralizedTemporal instances allowed!')

        self._check_same(data_list)

        first_item = data_list[0]

        nave = first_item.nave
        n_classes = first_item._nclasses
        scoring_name = first_item._scoring_name
        c_factors_training = first_item._c_factors_training
        info = first_item.info
        times_training = first_item._times_training
        tmin = first_item.tmin
        times_testing = first_item._times_testing
        c_factors_testing = first_item._c_factors_testing

        super(GeneralizedTemporalFromCollection, self).__init__(
            scores_raw=raw_scores,
            scoring_name=scoring_name, n_classes=n_classes,
            c_factors_training=c_factors_training, weights=weights, info=info,
            times_training=times_training, tmin=tmin,
            times_testing=times_testing,
            c_factors_testing=c_factors_testing, nave=nave)

    def _check_same(self, data_list):
        first_item = data_list[0]
        for cur_item in data_list:
            for cur_parameter in self.must_be_equal:
                first = getattr(first_item, cur_parameter)
                cur = getattr(cur_item, cur_parameter)
                cmp = first == cur
                if not isinstance(cmp, collections.Iterable):
                    cmp = [cmp]
                if not all(cmp):
                    # raise ValueError('All items must come
                    # from the same contrast!')
                    pass


class GeneralizedTemporalAverage(GeneralizedTemporalFromCollection):
    """Create average instance of Temporal Generalization results.

    Given a list of Temporal Generalization Results, this class computes the
    average of their weights and returns an instance of
    :class:`GeneralizedTemporalArray` so you can plot the average scores
    and weights.

    Parameters
    ----------
    data_list : iterable of :class:`GeneralizedTemporalArray`
        A list (or any other iterable) of :class:`GeneralizedTemporalArray`

    """

    def __init__(self, data_list):
        weights = numpy.average(numpy.stack([x._weights for x in data_list]),
                                axis=0)
        scores_raw = numpy.average(
            numpy.stack([x._scores_raw for x in data_list]), axis=0)

        super(GeneralizedTemporalAverage, self).__init__(data_list,
                                                         raw_scores=scores_raw,
                                                         weights=weights)


class GeneralizedTemporalStatistics(GeneralizedTemporalAverage):
    """Run statistics on Temporal Generalization results.

    Given a list of Temporal Generalization Results, this class calculates
    a statistic on the weights and returns an instance of
    :class:`GeneralizedTemporalArray`.
    """

    def __init__(self, data_list, stat_function=scipy.stats.ttest_1samp,
                 popmean=None, **kwargs):
        super(GeneralizedTemporalStatistics, self).__init__(data_list)

        if popmean is None:
            popmean = self.chance_level

        scores_for_stats = numpy.stack(x.scores for x in data_list)

        self.stat_values, self.p = stat_function(scores_for_stats,
                                                 popmean=popmean, **kwargs)
        self.p = self.p / 2.0

    def plot_scores(self, axes=None, show=True, cmap='Reds', colorbar=True,
                    mask_below_chance=False, interpolation='bessel',
                    mask_p=None):
        """Plot the scores as a Matrix.

        Parameters
        ----------
        axes : :class:`matplotlib.axes.Axes` or None, optional
            The axes where to draw the plot. If ``None``, a new figure is
            created.
        show : bool, optional
            True to actually show the plot.
        cmap : str or :class:`matplotlib.colors.Colormap`, optional
            The colormap.
        colorbar : bool, optional
            Whether to draw the colorbar.
        mask_below_chance : bool, optional
            If True, values below chance level get masked.
        interpolation : str, optional
            The interpolation method used.
        mask_p : float or None, optional
            If set, the plot is masked for the given p-value.
        """
        scores = self.scores

        if mask_below_chance:
            scores = numpy.ma.masked_less(scores, self.chance_level)

        if mask_p is not None:
            scores = numpy.ma.masked_where(self.p > mask_p, scores)

        return self._plot_image(values=scores, axes=axes, show=show, cmap=cmap,
                                colorbar=colorbar, interpolation=interpolation)

    def get_temporal_from_training_interval(self, tmin, tmax):
        """Average the scores of a training interval.

        Parameters
        ----------
        tmin : int
            Start time in seconds of the training interval to average.
        tmax : int
            End time in seconds of the training interval to average.

        Returns
        -------
        data : instance of :class:`TemporalArray`
            The :class:`TemporalArray` with the averaged scores.
        """
        temporal = super(GeneralizedTemporalStatistics,
                         self).get_temporal_from_training_interval(tmin=tmin,
                                                                   tmax=tmax)

        time_idx = numpy.where(
            numpy.logical_and(self._times_training >= tmin,
                              self._times_training <= tmax))[0]

        stats = numpy.mean(self.stat_values[time_idx, :], axis=0)
        temporal.stat_values = stats

        return temporal


class GeneralizedTemporal(GeneralizedTemporalArray):
    """Apply a decoding pipeline using Temporal Generalization.

    Use this class to perform Temporal Generalization decoding. This means
    that a classifier is trained on every sample and then tested on all
    samples. So, if you supply epochs with 100 samples, a classifier gets
    trained on the data data of the first sample. This classifier is then
    tested on the data of the first sample, then the second sample and so on.
    The process is then repeated by training on the second sample and testing
    on all samples and so forth.

    The minimum requirements are the data as :class:`mne.Epochs` and
    the pipeline as :class:`sklearn.pipeline.Pipeline`, which is most
    commonly generated using :func:`sklearn.pipeline.make_pipeline`.

    This class treats every individual ``event_id`` as an individual target.
    If you want to combine multiple ``events_id`` into one target, you can
    use :func:`epochs.collapse_conditions`.

    If you want the training and testing data to be different, you can supply
    the training data to ``epochs`` and the testing data to ``epochs_test``.

    Cross validation will be run only if training and testing data are equal
    (i.e., when ``epochs_test=None``).

    Parameters
    ----------
    epochs : :class:`mne.Epochs`
        The epochs to apply the classifier pipeline to.
    pipeline : :class:`sklearn.pipeline.Pipeline`
        The classifier pipeline to use. Most likely created with
        :func:`sklearn.pipeline.make_pipeline`
    epochs_test : :class:`mne.Epochs` or None, optional
        If set, the classifier gets tested on this data. The event_ids must
        be equal. No crossvalidation will be run in this case.
    cv : int, optional
        The amount of folds for cross validation
    scoring : str or callable, optional
        The scoring function to use.
    n_jobs : int, optional
        Number of CPU cores to use

    """

    def __init__(self, epochs, pipeline, epochs_test=None, cv=2,
                 scoring='accuracy', n_jobs=-1, metadata_querylist=None):
        times_training = epochs.times
        times_testing = None
        nave = len(epochs)
        nave_testing = None

        new_info = mne.create_info(epochs.info['ch_names'],
                                   epochs.info['sfreq'])
        new_info['chs'] = copy.deepcopy(epochs.info['chs'])

        self._decoder = mne.decoding.GeneralizingEstimator(pipeline,
                                                           n_jobs=n_jobs,
                                                           scoring=scoring)
        X = epochs.get_data()
        if metadata_querylist is None:
            y = epochs.events[:, 2]
        else:
            y = _get_Y_from_metadata(epochs, metadata_querylist)

        n_classes = numpy.unique(y).size

        c_factors_training = ''
        if 'collapsed_factors' in epochs.info:
            c_factors_training = epochs.info['collapsed_factors']

        c_factors_testing = None

        if isinstance(epochs_test, mne.BaseEpochs):
            logging.info(
                'Using epochs argument for training and epochs_test argument '
                'for testing')

            X_test = epochs_test.get_data()
            if metadata_querylist is None:
                y_test = epochs_test.events[:, 2]
            else:
                y_test = _get_Y_from_metadata(epochs_test, metadata_querylist)
            nave_testing = len(epochs_test)

            if 'collapsed_factors' in epochs_test.info:
                c_factors_testing = epochs_test.info['collapsed_factors']

            times_testing = epochs_test.times

            if numpy.setdiff1d(y, y_test).size != 0:
                raise ValueError(
                    'Training and testing set must have the same targets!')

            if X.shape[1] != X_test.shape[1]:
                raise ValueError('Training and testing set must have the '
                                 'same number of channels!')

            self._decoder.fit(X, y)
            scores_raw = self._decoder.score(X_test, y_test)

        else:
            scores_raw = mne.decoding.cross_val_multiscore(self._decoder, X, y,
                                                           cv=cv)

        self._decoder.fit(X, y)
        weights = mne.decoding.get_coef(self._decoder, 'patterns_',
                                        inverse_transform=True)
        if weights.ndim == 3:
            weights = numpy.average(weights, axis=1)

        super(GeneralizedTemporal, self).__init__(scores_raw=scores_raw,
                                                  scoring_name=scoring,
                                                  n_classes=n_classes,
                                                  c_factors_training=c_factors_training,  # noqa
                                                  c_factors_testing=c_factors_testing,  # noqa
                                                  times_training=times_training,  # noqa
                                                  times_testing=times_testing,
                                                  weights=weights,
                                                  tmin=epochs.times[0],
                                                  info=new_info,
                                                  nave=nave,
                                                  nave_testing=nave_testing)
