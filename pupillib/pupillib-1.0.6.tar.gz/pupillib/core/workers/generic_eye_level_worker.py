'''
(*)~---------------------------------------------------------------------------
This file is part of Pupil-lib.

Pupil-lib is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pupil-lib is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pupil-lib.  If not, see <https://www.gnu.org/licenses/>.

Copyright (C) 2018  Gregory W. Mierzwinski
---------------------------------------------------------------------------~(*)
'''
import copy
import os
import threading
import numpy as np
from threading import Thread

from pupillib.core.utilities.MPLogger import MultiProcessingLog
from pupillib.core.workers.processors.eye_processor import EyeProcessor
from pupillib.core.workers.processors.generic_eye_level_processor import GenericEyeLevelProcessor
from pupillib.core.workers.trigger_worker import PLibTriggerWorker

import pupillib.core.utilities.utilities as utilities


class GenericEyeLevelWorker(Thread):
    def __init__(self, config, dataset=None, markers=None):
        Thread.__init__(self)
        self.config = copy.deepcopy(config)    # Metadata about how to process the given datasets.
        self.dataset = dataset
        if dataset and 'data' in self.dataset and 'timestamp' in self.dataset:
            self.dataset['srate'] = np.size(self.dataset['data'], 0) / \
                (np.max(self.dataset['timestamps']) - np.min(self.dataset['timestamps']))
            self.config['srate'] = dataset['srate']
        else:
            self.config['srate'] = 0

        self.markers = markers
        print(self.markers)
        self.logger = MultiProcessingLog.get_logger()

        self.initial_data = {
            'config': config,    # Metadata about how to process the given datasets.
            'dataset': dataset,
            'markers': markers
        }

        self.trigger_data = {}
        self.proc_data = {}

    def reset_initial_data(self):
        self.config = self.initial_data['config']
        self.dataset = self.initial_data['dataset']
        self.markers = self.initial_data['markers']

    def set_data(self, data, markers):
        self.dataset = data
        if data and 'data' in data and 'timestamp' in data:
            self.dataset['srate'] = np.size(data['data'], 0) / \
                (np.max(data['timestamps']) - np.min(data['timestamps']))
        self.markers = markers
        self.config['srate'] = self.dataset['srate']

        self.initial_data = {
            'config': self.config,    # Metadata about how to process the given datasets.
            'dataset': self.dataset,
            'markers': self.markers
        }

    def run(self):
        self.trigger_data = {}
        self.proc_data = {}

        def data_name_to_processor(data_name):
            data_proc_list = {
                'eye0': EyeProcessor(),
                'eye1': EyeProcessor(),
            }

            if data_name in data_proc_list:
                return data_proc_list[data_name]
            else:
                return GenericEyeLevelProcessor()

        if self.config['testing']:
            self.logger.send('INFO', 'I am an eye worker. I split the triggers.', os.getpid(), threading.get_ident())

        # If this eye is in the yaml config, specify it's
        # configuration by replacing the current one with a new one.
        self.config = utilities.parse_yaml_for_config(self.config, self.getName())

        print('Working on: ' + self.getName())
        print('with the following triggers: ' + str(self.config['triggers']))

        # Run the pre processors.
        processor = None
        name = self.getName().split(":")[-1]
        if self.config['eye_pre_processing']:
            processor = data_name_to_processor(name)

            for config in self.config['eye_pre_processing']:
                if config['name'] in processor.pre_processing.all:
                    processor.pre_processing.all[config['name']](self.dataset, config)

        trigger_workers = {}
        base_trig_worker = PLibTriggerWorker(self.config, self.dataset)
        parallel = False
        # For each trigger, get the number of trials that are within
        # each of them and start a thread to process those.
        trig_list = []
        if self.config['triggers'] and self.markers['eventnames'] is not None:
            trig_list = self.config['triggers']
        else:
            trig_list = []

        for i in trig_list:
            inds = utilities.get_marker_indices(self.markers['eventnames'], i)
            proc_mtimes = utilities.indVal(self.markers['timestamps'], inds)
            #self.logger.send('INFO', str(inds), os.getpid(), threading.get_ident())
            #self.logger.send('INFO', str(proc_mtimes), os.getpid(), threading.get_ident())
            if len(proc_mtimes) == 0:
                self.logger.send('INFO', 'The trigger name ' + i + ' cannot be found in the dataset.', os.getpid(),
                            threading.get_ident())
                continue

            self.trigger_data[i] = {}

            # If we have enough workers available, do them all in parallel.
            # Otherwise, we simply do them sequentially.
            if self.config['max_workers'] > self.config['num_datasets'] + \
                    self.config['num_eyes'] + self.config['total_triggers']:
                trigger_worker = PLibTriggerWorker(self.config, self.dataset, inds, proc_mtimes, i)
                trigger_worker.setName(self.getName() + ":trigger" + i)
                trigger_workers[i] = trigger_worker
                trigger_worker.start()
                parallel = True
            else:
                base_trig_worker.setName(self.getName() + ":trigger" + i)
                base_trig_worker.marker_inds = inds
                base_trig_worker.marker_times = proc_mtimes
                base_trig_worker.marker_name = copy.deepcopy(i)
                base_trig_worker.reset_initial_data()
                base_trig_worker.run()
                self.trigger_data[i] = copy.deepcopy(base_trig_worker.proc_trigger_data)

        if parallel:
            for i in trigger_workers:
                trigger_workers[i].join()
            #self.logger.send('INFO', 'Done all eyes for ' + self.getName())
            for i in self.config['triggers']:
                self.trigger_data[i] = trigger_workers[i].proc_trigger_data

        self.proc_data = {
            'config': {
                'name': self.getName(),
                'dataset': self.dataset,
                'srate': self.config['srate']
            },
            'triggers': self.trigger_data if trig_list else None
        }

        # No triggers in data, skip post-processing
        if self.proc_data['triggers'] is None:
            return

        # Run the post processors.
        if self.config['eye_post_processing']:
            if not processor:
                processor = data_name_to_processor(name)

            for config in self.config['eye_post_processing']:
                if config['name'] in processor.post_processing.all:
                    processor.post_processing.all[config['name']](self.proc_data, config)