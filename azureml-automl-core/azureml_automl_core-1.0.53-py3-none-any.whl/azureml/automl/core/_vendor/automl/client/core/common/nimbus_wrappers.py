# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module to wrap NimbusML models."""
from typing import Any, Dict, Optional, Union
import os
import tempfile

import numpy as np

import sklearn
from sklearn.base import (BaseEstimator, ClassifierMixin, RegressorMixin,
                          TransformerMixin, clone)
from sklearn.utils.multiclass import unique_labels
from automl.client.core.common.exceptions import ConfigException

import automl.client.core.common
from automl.client.core.common.model_wrappers import _AbstractModelWrapper
try:
    import nimbusml as nml
    import nimbusml.linear_model as nml_linear
    import nimbusml.multiclass as nml_multiclass
    nimbusml_present = True
except ImportError:
    nimbusml_present = False

if nimbusml_present:
    class NimbusMlWrapperBase(_AbstractModelWrapper):
        """
        Nimbusml base class.

        Contains code common to multiple NumbusML learners.
        """

        SERIALIZED_MODEL_STATE_KEY = "_serialized_model_"

        def get_model(self):
            """
            Return Nimbusml model.

            :return: Returns self.
            """
            return self

        def get_random_state(self, args: Dict[str, Any]) -> Any:
            """
            Get and remove the random state from args.

            :param args: parameter dictionary.
            :type args: dict
            :param y: Input target values.
            :return: Random state.
            """
            random_state = args.pop('random_state', None)

            for argname in ['n_jobs', 'model', 'steps']:
                args.pop(argname, None)

            # The RandomState class is not supported by Pipeline.
            if isinstance(random_state, np.random.RandomState):
                random_state = None

            return random_state

        def __getstate__(self):
            """
            Get the internal state of this pipeline, allowing it to be safely pickle-able.

            :return: a dict containing serializable state.
            """
            state = self.__dict__
            model_file = self._get_nimbus_model_file_for_serialization()
            with open(model_file, "rb") as bf:
                state[self.SERIALIZED_MODEL_STATE_KEY] = bf.read()
            return state

        def __setstate__(self, state):
            """
            Set the internal state of this pipeline, allowing it to be safely unpickle-able.

            :param state: dictionary containing object state
            :type state: dict
            """
            model_state = state.pop(self.SERIALIZED_MODEL_STATE_KEY)
            self.__dict__ = state
            model_file = self._get_nimbus_model_file_for_serialization()
            try:
                with open(model_file, "wb") as bf:
                    bf.write(model_state)
            except IOError:
                # let's create a file where we can dump this model
                file_handle, file_name = tempfile.mkstemp(suffix=".bin", prefix="binary_model_", dir=os.getcwd())
                with os.fdopen(file_handle, "wb") as bf:
                    bf.write(state[model_state])
                self._set_nimbus_model_file_for_serialization(file_name)

        def _get_nimbus_model_file_for_serialization(self):
            pass

        def _set_nimbus_model_file_for_serialization(self, model_file):
            pass

    class NimbusMlPipelineWrapper(nml.Pipeline, NimbusMlWrapperBase):
        """Wrapper for a NimbusML Pipeline to make predict/predict_proba API follow SciKit return types."""

        def __init__(self, steps=None, **kwargs):
            """
            Initialize Nimbusml Pipeline wrapper class.

            :param steps:
                List of (name, transform) tuples (implementing fit/transform) that are chained.
            :type steps: List of Tuple.
            """
            self.classes_ = None
            super(NimbusMlPipelineWrapper, self).__init__(steps=steps, **kwargs)  # type: ignore

        def fit(self, X, y, **kwargs):
            """Fit the Pipeline."""
            result = super(NimbusMlPipelineWrapper, self).fit(X, y, **kwargs)
            if self.last_node.type == NimbusMlClassifierMixin._estimator_type:
                classes = getattr(self, "classes_", None)
                if classes is None:
                    classes = unique_labels(y)
                self.classes_ = classes
            return result

        def predict(self, X, *args, **kwargs):
            """Apply transforms to the data, and predict with the final estimator."""
            projected_column = None
            if self.last_node.type == NimbusMlClassifierMixin._estimator_type:
                projected_column = "PredictedLabel"
            elif self.last_node.type == NimbusMlRegressorMixin._estimator_type:
                projected_column = "Score"
            else:
                raise ConfigException("Unsupported nimbusml pipeline type")

            return super(NimbusMlPipelineWrapper, self).predict(X, *args, **kwargs)[projected_column].values

        def _get_nimbus_model_file_for_serialization(self):
            return self.model

        def _set_nimbus_model_file_for_serialization(self, model_file):
            self.model = model_file

    class NimbusMlEstimatorMixin(nml.internal.core.base_pipeline_item.BasePipelineItem, NimbusMlWrapperBase):
        """Base class for all NimbusML learners / transformers handling pickling/unpickling scenarios."""

        def _get_nimbus_model_file_for_serialization(self):
            return self.model_

        def _set_nimbus_model_file_for_serialization(self, model_file):
            self.model_ = model_file

    class NimbusMlClassifierMixin(NimbusMlEstimatorMixin, ClassifierMixin):
        """Base class for all NimbusML classifiers, implementing common functionality."""

        def fit(self, X, y, **kwargs):
            """Fit method for a NimbusML classfier."""
            super().fit(X, y, **kwargs)
            return self

        def predict(self, X, *args, **kwargs):
            """
            Prediction function for a Nimbusml Classifier model.

            :param X: Input data.
            :type X: numpy.ndarray
            :return: Prediction values from a Nimbusml Classifier model.
            """
            return super().predict(X, *args, **kwargs).values

    class NimbusMlRegressorMixin(NimbusMlEstimatorMixin, RegressorMixin):
        """Base class for all NimbusML regressors, implementing common functionality."""

        def predict(self, X, *args, **kwargs):
            """
            Prediction function for a Nimbusml Regressor model.

            :param X: Input data.
            :return: Prediction values from a Nimbusml Regressor model.
            """
            return self.predict(X, *args, **kwargs).values

    class AveragedPerceptronClassifier(NimbusMlClassifierMixin):
        """
        Nimbusml Averaged Perceptron Classifier class usable only in SciKit pipelines.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number generator;
            If RandomState instance, random_state is the random number generator;
            If None, the random number generator is the RandomState instance used
            by `np.random`.
        :type random_state: int or RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://docs.microsoft.com
            /en-us/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier
            for more parameters.
        """

        def __init__(self,
                     random_state: Optional[Union[int, np.random.RandomState]] = 0,
                     n_jobs: int = 1,
                     **kwargs: Any) -> None:
            """
            Initialize Nimbusml Averaged Perceptron Classifier class usable only in SciKit pipelines.

            :param random_state:
                RandomState instance or None, optional (default=None)
                If int, random_state is the seed used by the random number generator;
                If RandomState instance, random_state is the random number generator;
                If None, the random number generator is the RandomState instance used
                by `np.random`.
            :type random_state: int or RandomState
            :param n_jobs: Number of parallel threads.
            :type n_jobs: int
            :param kwargs: Other parameters
                Check https://docs.microsoft.com
                /en-us/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier
                for more parameters.
            """
            self.params = kwargs
            self.classes_ = None
            self.model = None
            self.type = NimbusMlClassifierMixin._estimator_type

        def fit(self, X, y, **kwargs):
            """Fit method for the AveragedPerceptronClassifier."""
            args = dict(self.params)
            nml_model = nml_linear.AveragedPerceptronBinaryClassifier(**args)
            if len(unique_labels(y)) > 2:
                # predict_proba returns classes in the order of their indexes in string order.
                nml_model = nml_multiclass.OneVsRestClassifier(nml_model)
            nml_model.fit(X, y, **kwargs)
            self.model = nml_model
            self.classes_ = self.model.classes_
            return self

        def predict(self, X):
            """
            Prediction function for Nimbusml Averaged Perceptron Classifier model.

            :param X: Input data.
            :type X: numpy.ndarray
            :return: Prediction values from Nimbusml Averaged Perceptron Classifier model.
            """
            if self.model is None:
                raise sklearn.exceptions.NotFittedError()
            return self.model.predict(X).values

        def predict_proba(self, X):
            """
            Prediction class probabilities for X for Nimbusml Averaged Perceptron Classifier model.

            :param X: Input data.
            :type X: numpy.ndarray
            :return: Prediction probability values from Nimbusml Averaged Perceptron Classifier model.
            """
            if self.model is None:
                raise sklearn.exceptions.NotFittedError()
            return self.model.predict_proba(X)

        def get_model(self):
            """
            Return Nimbusml model.

            :return: Returns wrapped Nimbus ML model.
            """
            return self.model

        def _get_node(self, **all_args):
            pass

        def _get_nimbus_model_file_for_serialization(self):
            return self.model.model_

        def _set_nimbus_model_file_for_serialization(self, model_file):
            self.model.model_ = model_file

    class AveragedPerceptronBinaryClassifier(NimbusMlClassifierMixin, nml_linear.AveragedPerceptronBinaryClassifier):
        """
        Nimbusml Averaged Perceptron Binary Classifier class that can be used within Nimbus pipelines.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number generator;
            If RandomState instance, random_state is the random number generator;
            If None, the random number generator is the RandomState instance used
            by `np.random`.
        :type random_state: int or RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://docs.microsoft.com
            /en-us/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier
            for more parameters.
        """

        def __init__(self,
                     random_state: Optional[Union[int, np.random.RandomState]] = 0,
                     n_jobs: int = 1,
                     **kwargs: Any) -> None:
            """
            Initialize Nimbusml Averaged Perceptron Binary Classifier class that can be used within Nimbus pipelines.

            :param random_state:
                RandomState instance or None, optional (default=None)
                If int, random_state is the seed used by the random number generator;
                If RandomState instance, random_state is the random number generator;
                If None, the random number generator is the RandomState instance used
                by `np.random`.
            :type random_state: int or RandomState
            :param n_jobs: Number of parallel threads.
            :type n_jobs: int
            :param kwargs: Other parameters
                Check https://docs.microsoft.com
                /en-us/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier
                for more parameters.
            """
            self.params = kwargs
            self.classes_ = None
            self.type = NimbusMlClassifierMixin._estimator_type
            if not nimbusml_present:
                raise ConfigException("nimbusml not installed, " +
                                      "please install nimbusml for including nimbusml based models")
            args = dict(self.params)
            nml_linear.AveragedPerceptronBinaryClassifier.__init__(self, **args)

        def get_params(self, deep=True):
            """
            Return parameters for Nimbusml Averaged Perceptron Classifier model.

            :param deep: If True, will return the parameters for this estimator and contained subobjects that are
                estimators.
            :type deep: boolean
            :return: Parameters for the Nimbusml Averaged Perceptron classifier model.
            """
            return super(AveragedPerceptronBinaryClassifier, self).get_params(deep)

    class AveragedPerceptronMultiClassClassifier(NimbusMlClassifierMixin, nml_multiclass.OneVsRestClassifier):
        """
        Nimbusml Averaged Perceptron Classifier for multiple classes that can be used within Nimbus pipelines.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number generator;
            If RandomState instance, random_state is the random number generator;
            If None, the random number generator is the RandomState instance used
            by `np.random`.
        :type random_state: int or RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://docs.microsoft.com
            /en-us/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier
            for more parameters.
        """

        def __init__(self,
                     random_state: Optional[Union[int, np.random.RandomState]] = 0,
                     n_jobs: int = 1,
                     **kwargs: Any) -> None:
            """
            Initialize Nimbusml Averaged Perceptron Classifier class.

            :param random_state:
                RandomState instance or None, optional (default=None)
                If int, random_state is the seed used by the random number
                generator.
                If RandomState instance, random_state is the random number
                generator.
                If None, the random number generator is the RandomState instance
                used by `np.random`.
            :type random_state: int or RandomState
            :param n_jobs: Number of parallel threads.
            :type n_jobs: int
            :param kwargs: Other parameters
                Check https://docs.microsoft.com
                /en-us/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier
                for more parameters.
            """
            self.params = kwargs
            self.classes_ = None
            self.type = NimbusMlClassifierMixin._estimator_type
            if not nimbusml_present:
                raise ConfigException("nimbusml not installed, " +
                                      "please install nimbusml for including nimbusml based models")
            args = dict(self.params)
            nml_multiclass.OneVsRestClassifier.__init__(self, nml_linear.AveragedPerceptronBinaryClassifier(**args))

        def get_params(self, deep=True):
            """
            Return parameters for Nimbusml Averaged Perceptron Classifier model.

            :param deep: If True, will return the parameters for this estimator and contained subobjects that are
                estimators.
            :type deep: boolean
            :return: Parameters for the Nimbusml Averaged Perceptron classifier model.
            """
            # TODO: Fix this as it is not applicable anymore
            return super(AveragedPerceptronMultiClassClassifier, self).get_params(deep)

    class FastLinearClassifier(NimbusMlClassifierMixin, nml_linear.FastLinearClassifier):
        """
        Nimbusml Fast Linear Classifier class.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number generator;
            If RandomState instance, random_state is the random number generator;
            If None, the random number generator is the RandomState instance used
            by `np.random`.
        :type random_state: int or RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://docs.microsoft.com/en-us/python/api/nimbusml/nimbusml.linear_model.fastlinearclassifier
            for more parameters.
        """

        def __init__(self,
                     random_state: Optional[Union[int, np.random.RandomState]] = 0,
                     n_jobs: int = 1,
                     **kwargs: Any) -> None:
            """
            Initialize Nimbusml Fast Linear Classifier class.

            :param random_state:
                RandomState instance or None, optional (default=None)
                If int, random_state is the seed used by the random number
                generator.
                If RandomState instance, random_state is the random number
                generator.
                If None, the random number generator is the RandomState instance
                used by `np.random`.
            :type random_state: int or RandomState
            :param n_jobs: Number of parallel threads.
            :type n_jobs: int
            :param kwargs: Other parameters
                Check https://docs.microsoft.com/en-us/python/api/nimbusml/nimbusml.linear_model.fastlinearclassifier
                for more parameters.
            """
            self.params = kwargs
            self.params['random_state'] = random_state if random_state is not None else 0
            self.params['n_jobs'] = n_jobs
            self.classes_ = None
            if not nimbusml_present:
                raise ConfigException("nimbusml not installed, " +
                                      "please install nimbusml for including nimbusml based models")

            args = dict(self.params)
            random_state = self.get_random_state(args)
            nml_linear.FastLinearClassifier.__init__(self, **args)

    class FastLinearRegressor(NimbusMlRegressorMixin, nml_linear.FastLinearRegressor):
        """
        Nimbusml Fast Linear Regressor class.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number generator;
            If RandomState instance, random_state is the random number generator;
            If None, the random number generator is the RandomState instance used
            by `np.random`.
        :type random_state: int or RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://docs.microsoft.com/en-us/python/api/nimbusml/nimbusml.linear_model.fastlinearregressor
            for more parameters.
        """

        def __init__(self,
                     random_state: Optional[Union[int, np.random.RandomState]] = 0,
                     n_jobs: int = 1,
                     **kwargs: Any) -> None:
            """
            Initialize Nimbusml Fast Linear Regressor class.

            :param random_state:
                RandomState instance or None, optional (default=None)
                If int, random_state is the seed used by the random number
                generator.
                If RandomState instance, random_state is the random number
                generator.
                If None, the random number generator is the RandomState instance
                used by `np.random`.
            :type random_state: int or RandomState
            :param n_jobs: Number of parallel threads.
            :type n_jobs: int
            :param kwargs: Other parameters
                Check https://docs.microsoft.com/en-us/python/api/nimbusml/nimbusml.linear_model.fastlinearregressor
                for more parameters.
            """
            self.params = kwargs
            self.params['random_state'] = random_state if random_state is not None else 0
            self.params['n_jobs'] = n_jobs
            if not nimbusml_present:
                raise ConfigException("nimbusml not installed, " +
                                      "please install nimbusml for including nimbusml based models")

            args = dict(self.params)
            random_state = self.get_random_state(args)

            nml_linear.FastLinearRegressor.__init__(self, **args)

        def get_model(self):
            """
            Return Nimbusml Fast Linear Regressor model.

            :return: Returns the fitted model if fit method has been called.
            Else returns None.
            """
            return self

        def get_params(self, deep=True):
            """
            Return parameters for Nimbusml Fast Linear Regressor model.

            :param deep: If True, will return the parameters for this estimator and contained subobjects that are
                estimators.
            :type deep: boolean
            :return: Parameters for the Nimbusml Fast Linear Regressor model.
            """
            return super().get_params(deep=True)
