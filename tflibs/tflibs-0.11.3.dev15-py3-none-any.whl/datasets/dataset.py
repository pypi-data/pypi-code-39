"""
    When defining a dataset, a class that inherits `tflibs.datasets.BaseDataset` should be defined.

    The following is an example of a definition.

    >>> import os
    >>> from tflibs.datasets import ImageSpec, LabelSpec
    >>>
    >>> class CatDogDataset(BaseDataset):
    >>>     def __init__(self, dataset_dir, image_size):
    >>>         self._image_size = image_size
    >>>         BaseDataset.__init__(self, os.path.join(dataset_dir, 'cat_dog'))
    >>>
    >>>     @property
    >>>     def tfrecord_filename(self):
    >>>         return 'cat_dog.tfrecord'
    >>>
    >>>     def _init_feature_specs(self):
    >>>         return {
    >>>             'image': ImageSpec([self._image_size, self._image_size, 3]),
    >>>             'label': LabelSpec(3, class_names=['Cat', 'Dog', 'Cookie'])
    >>>         }
    >>>
    >>>     @classmethod
    >>>     def add_arguments(cls, parser):
    >>>         parser.add_argument('--image-size',
    >>>                             type=int,
    >>>                             default=128,
    >>>                             help='The size of output image.')

    When writing TF-record files, create dataset object and call `write()`.

    >>> dataset = CatDogDataset('/tmp/dataset', 64)
    >>>
    >>> images = ['/cat/abc.jpg', '/dog/def.jpg', '/cookie/ghi.jpg']
    >>> labels = ['Cat', 'Dog', 'Cookie']
    >>>
    >>> def process_fn((image_path, label_str), feature_specs):
    >>>     id_string = os.path.splitext(os.path.basename(image_path))[0]
    >>>
    >>>     def build_example(_id, image, label):
    >>>         return {
    >>>             '_id': _id.create_with_string(id_string),
    >>>             'image': image.create_with_path(image_path),
    >>>             'label': label.create_with_label(label_str),
    >>>         }
    >>>
    >>>     return build_example(**feature_specs)
    >>>
    >>> dataset.write(zip(images, labels), process_fn)

    When reading TF-record files, create dataset object and call `read()`.

    >>> dataset = CatDogDataset('/tmp/dataset', 64)
    >>>
    >>> # Returns a `tf.data.Dataset`
    >>> # {
    >>> #   '_id': {
    >>> #       'dtype': tf.string,
    >>> #       'shape': (),
    >>> #   },
    >>> #   'image': {
    >>> #       'dtype': tf.uint8,
    >>> #       'shape': [64, 64, 3],
    >>> #   },
    >>> #   'label': {
    >>> #       'dtype': tf.int64,
    >>> #       'shape': [3],
    >>> #   }
    >>> # }
    >>> tfdataset = dataset.read()


"""
from __future__ import absolute_import, division, print_function

import os
import threading
import argparse
import itertools

import tensorflow as tf
import numpy as np
from tqdm import tqdm
from pandas import DataFrame

from tflibs.utils import map_dict, flatten_nested_dict
from tflibs.datasets.feature_spec import IDSpec, FeatureSpec


class BaseDataset:
    """
    A base class for defining a dataset

    :param str dataset_dir: A directory where tfrecord files are stored
    """

    def __init__(self, dataset_dir):
        self._dataset_dir = dataset_dir

        if not tf.gfile.Exists(dataset_dir):
            tf.gfile.MakeDirs(dataset_dir)

    def feature_specs(self, split=None):
        feature_specs = self._init_feature_specs(split=split)
        feature_specs.update({
            '_id': IDSpec()
        })

        return feature_specs

    @property
    def tfrecord_filename(self):
        """
        It should return the name of TF-record file.

        This should be implemented when defining a dataset.

        :return: TF-record filename
        :rtype: str
        """
        raise NotImplementedError

    def _init_feature_specs(self, split=None):
        raise NotImplementedError

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser):
        """
        Adds arguments.

        Called when `tflibs.runner.DatasetInitializer <./Initializers.html#tflibs.runner.initializer.DatasetInitializer>`_ creates a dataset object.

        :param argparse.ArgumentParser parser: Argument parser used to add arguments
        """
        pass

    def write(self, iterable, process_fn, split=None, num_parallel_calls=16, length: int = None):
        """
        Writes examples on tfrecord files

        :param iterable iterable:
        :param function process_fn:
        :param int num_parallel_calls:
        """
        feature_specs = self.feature_specs(split=split)

        def process_wrapper(coll, length, thread_idx):
            # Make tfrecord writer
            fname, ext = os.path.splitext(self.tfrecord_filename)
            fname_pattern = '{fname}{split}{thread_idx:03d}-of-{num_threads:03d}{ext}'
            kwargs = {
                'fname': fname,
                'split': '_{split}_' if split is not None else '_',
                'thread_idx': thread_idx,
                'num_threads': num_parallel_calls,
                'ext': ext
            }
            tfrecord_filepattern = os.path.join(self._dataset_dir, fname_pattern.format(**kwargs))

            if split is not None:
                writer = tf.python_io.TFRecordWriter(tfrecord_filepattern.format(split=split))
            else:
                writer = tf.python_io.TFRecordWriter(tfrecord_filepattern)

            for elem in tqdm(coll, total=length, position=thread_idx):
                # Process
                processed = process_fn(elem, feature_specs)
                if processed is None:
                    continue

                # Write
                if not isinstance(processed, list):
                    processed = [processed]

                for processed_e in processed:
                    # Build feature proto
                    nested_feature = {k: feature_spec.feature_proto(processed_e[k]) for k, feature_spec in
                                      feature_specs.items() if k in processed_e}
                    # Flatten nested dict
                    feature = flatten_nested_dict(nested_feature)

                    # Build example proto
                    example = tf.train.Example(features=tf.train.Features(feature=feature))

                    # Write example proto on tfrecord file
                    writer.write(example.SerializeToString())

        # Split collection
        def get_spacing(length):
            return np.linspace(0, length, num_parallel_calls + 1, dtype=np.int)

        def get_ranges(length):
            spacing = get_spacing(length)
            ranges = zip(spacing[:-1], spacing[1:])

            return ranges

        if isinstance(iterable, list):
            ranges = get_ranges(len(iterable))
            colls = [{'coll': iterable[s:e], 'length': e - s} for s, e in ranges]
        elif isinstance(iterable, DataFrame):
            spacing = get_spacing(len(iterable))
            colls = [{'coll': coll.iterrows(), 'length': len(coll)} for coll in np.split(iterable, spacing[1:-1])]
        elif length is not None:
            ranges = get_ranges(length)
            colls = [{'coll': itertools.islice(iterable, s, e), 'length': e - s} for s, e in ranges]
        else:
            raise ValueError('`length` should be provided')

        threads = []
        for i, coll in enumerate(colls):
            kwargs = coll
            kwargs.update(thread_idx=i)

            thread = threading.Thread(target=process_wrapper, kwargs=kwargs)
            threads.append(thread)
            thread.start()

        for i, thread in enumerate(threads):
            tf.logging.info('Waiting for joining thread {}'.format(i))
            thread.join()
            tf.logging.info('Thread {} is joined'.format(i))

    def read(self, split=None, num_parallel_reads=16, num_parallel_calls=16, cache=True):
        """
        Reads tfrecord and makes it tf.data.Dataset

        :param split:
        :param num_parallel_reads:
        :param num_parallel_calls:
        :param cache:
        :return: A dataset
        """

        def dataset_fn():
            feature_specs = self.feature_specs(split=split)

            def parse(record):
                return {k: feature_spec.parse(k, record) for k, feature_spec in feature_specs.items()}

            fname, ext = os.path.splitext(self.tfrecord_filename)
            fname_pattern = '{fname}{split}*{ext}'
            kwargs = {
                'fname': fname,
                'split': '_{split}_'.format(split=split) if split is not None else '_',
                'ext': ext,
            }
            tfrecord_filepattern = os.path.join(self._dataset_dir, fname_pattern.format(**kwargs))

            tf.logging.info('TFRecord file pattern: {}'.format(tfrecord_filepattern))
            num_files = len(tf.gfile.Glob(tfrecord_filepattern))
            tf.logging.info('Number of TFRecord files: {}'.format(num_files))

            if num_files == 0:
                raise FileNotFoundError('There is not file named {}'.format(tfrecord_filepattern))

            files = tf.data.Dataset.list_files(tfrecord_filepattern, shuffle=False)

            num_parallel_calls_per_read = num_parallel_calls // num_parallel_reads
            num_parallel_calls_per_read += 1 if num_parallel_calls % num_parallel_reads != 0 else 0

            dataset = files.apply(tf.data.experimental.parallel_interleave(
                lambda f: tf.data.TFRecordDataset(f).map(parse,
                                                         num_parallel_calls=num_parallel_calls_per_read),
                cycle_length=num_parallel_reads))

            return dataset.cache() if cache else dataset

        return dataset_fn
