# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

from future.builtins import object, str

import io
import logging
import os
import time
import uuid
from distutils.version import LooseVersion  # pylint: disable=no-name-in-module, import-error

import PIL

from neptune.generated.swagger_client.models.tensorflow_graph import TensorflowGraph
from neptune.internal.client_library.job_development_api.channel_type import ChannelType
from neptune.internal.client_library.job_development_api.image import Image
from neptune.internal.common import NeptuneException

_LOGGER = logging.getLogger(__name__)


_integrated_with_keras = False
_tensorflow_integrator = None


class ThirdPartyIntegration(object):

    # pylint:disable=global-statement

    ''' Objective wrapper for functions within this module. '''

    def __init__(self, verbose=False):
        self.verbose = verbose

    def integrate_with_tensorflow(self, job):
        return integrate_with_tensorflow(job)

    def integrate_with_keras(self, job):
        integrate_with_keras(job, self.verbose)


class TensorflowIntegrator(object):

    def __init__(self, job, api_service):
        self._job = job
        self._api_service = api_service
        self._channels = {}
        self._summary_writer_to_graph_id = {}

    def add_summary(self, summary_writer, summary, global_step=None):

        from tensorflow.core.framework import summary_pb2  # pylint:disable=import-error,no-name-in-module

        if isinstance(summary, bytes):
            summ = summary_pb2.Summary()
            summ.ParseFromString(summary)
            summary = summ

        x = self._calculate_x_value(global_step)

        for value in summary.value:

            field = value.WhichOneof('value')

            if field == 'simple_value':
                self._send_numeric_value(summary_writer, value.tag, x, value.simple_value)

            elif field == 'image':
                self._send_image(summary_writer, value.tag, x, value.image.encoded_image_string)

    def add_graph_def(self, graph_def, logdir):
        writer = self.get_writer_name(logdir)
        if writer in list(self._summary_writer_to_graph_id.keys()):
            graph_id = self._summary_writer_to_graph_id[writer]
            graph = TensorflowGraph(graph_id, str(graph_def))
        else:
            graph_id = str(uuid.uuid4())
            self._summary_writer_to_graph_id[writer] = graph_id
            graph = TensorflowGraph(graph_id, str(graph_def))

        self._api_service.put_tensorflow_graph(self._job.id, graph)

    def _send_numeric_value(self, summary_writer, value_tag, x, simple_value):
        channel = self._get_channel(summary_writer, value_tag, ChannelType.NUMERIC)
        channel.send(x, simple_value)

    def _send_image(self, summary_writer, image_tag, x, encoded_image):
        channel = self._get_channel(summary_writer, image_tag, ChannelType.IMAGE)
        pil_image = PIL.Image.open(io.BytesIO(encoded_image))
        image_desc = "({}. Step {})".format(image_tag, x)
        channel.send(x=x, y=Image(name=image_desc, description=image_desc, data=pil_image))

    def _get_channel(self, summary_writer, value_tag, channel_type):
        # pylint: disable=protected-access
        writer_name = self.get_writer_name(summary_writer.get_logdir())
        channel_name = '{}_{}'.format(writer_name, value_tag)
        return self._job.create_channel(channel_name, channel_type)

    @staticmethod
    def get_writer_name(log_dir):
        return os.path.basename(os.path.normpath(log_dir))

    @staticmethod
    def _calculate_x_value(global_step):
        if global_step is not None:
            return int(global_step)
        else:
            return time.time()


def _create_neptune_add_summary_wrapper(tensorflow_integrator, _add_summary_method):

    def _neptune_add_summary(summary_writer, summary, global_step=None, *args, **kwargs):
        tensorflow_integrator.add_summary(summary_writer, summary, global_step)
        _add_summary_method(summary_writer, summary, global_step, *args, **kwargs)

    return _neptune_add_summary


def integrate_with_tensorflow(job):

    _LOGGER.info("====    Integrating Tensorflow with Neptune    ====")

    global _tensorflow_integrator  # pylint:disable=global-statement

    if _tensorflow_integrator:
        return _tensorflow_integrator

    print('neptune: Integrating with tensorflow...')

    _tensorflow_integrator = _integrate_with_tensorflow(job)

    return _tensorflow_integrator


def _integrate_with_tensorflow(job):

    try:
        import tensorflow
    except ImportError:
        raise NeptuneException('Requested integration with tensorflow while '
                               'tensorflow is not installed.')

    # pylint: disable=no-member, protected-access, no-name-in-module, import-error

    tensorflow_integrator = TensorflowIntegrator(job, job._api_service)

    version = LooseVersion(tensorflow.__version__)

    if LooseVersion('0.11.0') <= version < LooseVersion('0.12.0'):

        _add_summary_method = tensorflow.train.SummaryWriter.add_summary
        _add_graph_def_method = tensorflow.train.SummaryWriter._add_graph_def

        tensorflow.train.SummaryWriter.add_summary = \
            _create_neptune_add_summary_wrapper(tensorflow_integrator, _add_summary_method)
        tensorflow.train.SummaryWriter._add_graph_def = \
            _create_neptune_add_graph_def_wrapper(tensorflow_integrator, _add_graph_def_method)

    elif (LooseVersion('0.12.0') <= version < LooseVersion('0.13.0')) or (
            LooseVersion('1.0.0') <= version):

        _add_summary_method = tensorflow.summary.FileWriter.add_summary
        _add_graph_def_method = tensorflow.summary.FileWriter._add_graph_def

        tensorflow.summary.FileWriter.add_summary = \
            _create_neptune_add_summary_wrapper(tensorflow_integrator, _add_summary_method)
        tensorflow.summary.FileWriter._add_graph_def = \
            _create_neptune_add_graph_def_wrapper(tensorflow_integrator, _add_graph_def_method)

    else:
        raise NeptuneException("Tensorflow version {} is not supported.".format(version))

    return tensorflow_integrator


def _create_neptune_add_graph_def_wrapper(tensorflow_integrator, _add_graph_def_method):

    def _neptune_add_graph_def(summary_writer, graph_def, global_step=None, *args, **kwargs):

        try:
            from tensorflow.tensorboard.backend import process_graph  # pylint:disable=import-error
        except ImportError:
            from tensorboard.backend import process_graph  # pylint:disable=import-error

        # Restricting graph only to UI relevant information.
        process_graph.prepare_graph_for_ui(graph_def)
        # pylint: disable=protected-access
        tensorflow_integrator.add_graph_def(graph_def, summary_writer.get_logdir())
        _add_graph_def_method(summary_writer, graph_def, global_step, *args, **kwargs)

    return _neptune_add_graph_def


def integrate_with_keras(job, verbose=True):

    global _integrated_with_keras  # pylint:disable=global-statement

    if _integrated_with_keras:
        return

    if verbose:
        print('neptune: Integrating with keras...')

    _integrate_with_keras(job, verbose=verbose)

    _integrated_with_keras = True

    if verbose:
        print('neptune: Done.\n')


def _integrate_with_keras(job, verbose=True):

    try:
        import keras
    except ImportError:
        raise NeptuneException('Requested integration with keras while keras is not installed.')

    from keras.callbacks import BaseLogger, Callback    # pylint:disable=import-error

    class NeptuneLogger(Callback):

        def __init__(self, job, verbose):
            super(NeptuneLogger, self).__init__()
            self.job = job
            self.verbose = verbose

        def on_batch_end(self, batch, logs=None):  # pylint:disable=unused-argument

            if logs is None:
                return

            for metric, value in logs.items():

                if metric in ('batch', 'size'):
                    continue

                name = 'keras_on_batch_end_' + metric
                self.job.create_channel(name, ChannelType.NUMERIC).send(value)

        def on_epoch_end(self, epoch, logs=None):  # pylint:disable=unused-argument

            if logs is None:
                return

            for metric, value in logs.items():

                if metric in ('epoch', 'size'):
                    continue

                name = 'keras_on_epoch_end_' + metric
                self.job.create_channel(name, ChannelType.NUMERIC).send(value)

    class KerasAggregateCallback(Callback):

        def __init__(self, *callbacks):
            super(KerasAggregateCallback, self).__init__()
            self.callbacks = callbacks

        def set_params(self, params):
            for callback in self.callbacks:
                callback.params = params

        def set_model(self, model):
            for callback in self.callbacks:
                callback.model = model

        def on_epoch_begin(self, epoch, logs=None):
            for callback in self.callbacks:
                callback.on_epoch_begin(epoch, logs=logs)

        def on_batch_end(self, batch, logs=None):
            for callback in self.callbacks:
                callback.on_batch_end(batch, logs=logs)

        def on_epoch_end(self, epoch, logs=None):
            for callback in self.callbacks:
                callback.on_epoch_end(epoch, logs=logs)

    def monkey_patched_BaseLogger(*args, **kwargs):
        return KerasAggregateCallback(BaseLogger(*args, **kwargs), NeptuneLogger(job, verbose))

    keras.callbacks.BaseLogger = monkey_patched_BaseLogger
