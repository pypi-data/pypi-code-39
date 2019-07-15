#  -*- coding: utf-8 -*-
#  Copyright 2019 SAMITorch Authors. All Rights Reserved.
#  #
#  Licensed under the MIT License;
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      https://opensource.org/licenses/MIT
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ==============================================================================

from samitorch.inputs.sample import Sample
from typing import List


class Batch(object):
    """
    Represent a Batch during a training process.
    """

    def __init__(self, samples: List[Sample]):
        """
        Batch initializer.å

        Args:
            samples: A list of SAMITorch samples.
        """
        self._samples = samples
        self._x = [sample.x for sample in samples]
        self._y = [sample.y for sample in samples]
        self._dataset_id = [sample.dataset_id for sample in samples]

    @property
    def samples(self):
        """
        List of samples.

        Returns:
            list: The list of samples.
        """
        return self._samples

    @property
    def x(self):
        """
        List of inputs.

        Returns:
            list: The list of inputs (X).
        """
        return self._x

    @property
    def y(self):
        """
        List of labels.

        Returns:
            list: The list of labels (y).
        """
        return self._y

    @property
    def dataset_id(self):
        """
        List of data set IDs.

        Returns:
            list: The list of data set IDs.
        """
        return self._dataset_id

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        self._dataset_id = dataset_id

    def update(self, samples: List[Sample]):
        """
        Update an existing sample from another Sample.

        Args:
            samples (list of :obj:`samitorch.inputs.sample.Sample`): Takes the properties of this list of Sample to
            update an existing Batch.

        Returns:
            :obj:`samitorch.inputs.batch.Batch`: The updated Batch.
        """
        self._samples = samples
        self._x = [sample.x for sample in samples]
        self._y = [sample.y for sample in samples]
        self._dataset_id = [sample.dataset_id for sample in samples]
        return self

    def unpack(self) -> tuple:
        """
        Unpack a Sample.

        Returns:
            tuple: A Tuple of elements representing the (X, y) properties of the Sample.
        """
        return self._x, self._y, self._dataset_id

    @classmethod
    def from_batch(cls, batch):
        """
        Create a new Batch from an existing Batch passed in parameter.

        Args:
            batch (:obj:`samitorch.inputs.batch.Batch`): A template Batch.

        Returns:
            :obj:`samitorch.inputs.batch.Batch`: A new Batch object with same properties as the one passed in
                parameter.
        """
        return cls(batch.samples)
