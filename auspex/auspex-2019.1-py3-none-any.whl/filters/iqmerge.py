# Copyright 2016 Raytheon BBN Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

__all__ = ['IQMerger']

import queue
import itertools
import numpy as np
import os.path
import time

from auspex.stream import InputConnector, OutputConnector
from auspex.log import logger
import auspex.config as config
from .filter import Filter


class IQMerger(Filter):

    I           = InputConnector()
    Q           = InputConnector()
    source      = OutputConnector()

    def __init__(self, filter_name=None, **kwargs):
        super(IQMerger, self).__init__(filter_name=filter_name, **kwargs)
        self.quince_parameters = []

    def update_descriptors(self):
        if None in [ss.descriptor for ss in [self.I, self.Q]]:
            return # Wait until both input streams are updated

        if self.I.descriptor.dims() != self.Q.descriptor.dims():
            raise Exception(f"I and Q descriptor different sizes in {self}")
        self.descriptor = self.I.descriptor.copy()
        self.source.descriptor = self.descriptor
        self.source.update_descriptors()

    def main(self):
        self.done.clear()
        i_stream = self.I.input_streams[0]
        q_stream = self.Q.input_streams[0]

        # Buffers for stream data
        stream_data = {i_stream: np.zeros(0, dtype=self.I.descriptor.dtype),
                       q_stream: np.zeros(0, dtype=self.Q.descriptor.dtype)}

        # Store whether streams are done
        streams_done      = {i_stream: False, q_stream: False}
        points_per_stream = {i_stream: 0, q_stream: 0}

        while not self.exit.is_set():

            # Try to pull all messages in the queue. queue.empty() is not reliable, so we
            # ask for forgiveness rather than permission.
            msgs_by_stream = {i_stream: [], q_stream: []}

            for stream in [i_stream, q_stream]:
                while not self.exit.is_set():
                    try:
                        msgs_by_stream[stream].append(stream.queue.get(False))
                    except queue.Empty as e:
                        time.sleep(0.002)
                        break

            # Process many messages for each stream
            for stream, messages in msgs_by_stream.items():
                for message in messages:
                    message_type = message['type']
                    message_data = message['data']
                    message_data = message_data if hasattr(message_data, 'size') else np.array([message_data])
                    if message_type == 'event':
                        if message['event_type'] == 'done':
                            streams_done[stream] = True
                        elif message['event_type'] == 'refine':
                            logger.warning("ElementwiseFilter doesn't handle refinement yet!")
                        self.push_to_all(message)
                    elif message_type == 'data':
                        # Add any old data...
                        points_per_stream[stream] += len(message_data.flatten())
                        stream_data[stream] = np.concatenate((stream_data[stream], message_data.flatten()))

            # Now process the data with the elementwise operation
            smallest_length = min([d.size for d in stream_data.values()])
            new_data = [d[:smallest_length] for d in stream_data.values()]
            result = stream_data[i_stream][:smallest_length] + 1.0j*stream_data[q_stream][:smallest_length]
        
            if result.size > 0:
                self.source.push(result)

            # Add data to carry_data if necessary
            for stream in stream_data.keys():
                if stream_data[stream].size > smallest_length:
                    stream_data[stream] = stream_data[stream][smallest_length:]
                else:
                    stream_data[stream] = np.zeros(0, dtype=self.I.descriptor.dtype)

            # If the amount of data processed is equal to the num points in the stream, we are done
            if np.all([streams_done[stream] for stream in stream_data.keys()]):
                self.done.set()
                break
