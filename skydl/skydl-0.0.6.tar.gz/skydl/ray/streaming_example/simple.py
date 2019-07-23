from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import logging
import time

import ray
from skydl.ray.experimental.streaming.streaming import Environment
from skydl.ray.experimental.streaming.batched_queue import BatchedQueue
from skydl.ray.experimental.streaming.operator import OpType, PStrategy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", required=True, help="the input text file")


# Test functions
def splitter(line):
    return line.split()


def filter_fn(word):
    if "f" in word:
        return True
    return False


if __name__ == "__main__":
    args = parser.parse_args()
    ray.init()
    ray.register_custom_serializer(BatchedQueue, use_pickle=True)
    ray.register_custom_serializer(OpType, use_pickle=True)
    ray.register_custom_serializer(PStrategy, use_pickle=True)

    # A Ray streaming environment with the default configuration
    env = Environment()

    # Returns the second attribute of a tuple
    def attribute_selector(tuple):
        return tuple[1]

    # Returns the first attribute of a tuple
    def key_selector(tuple):
        return tuple[0]

    class CustormSorce:
        def __init__(self):
            self._count = 0
        def get_next(self):
            self._count += 1
            if self._count > 10:
                return None
            else:
                return "United States"

    stream = env.source(CustormSorce()) \
                .shuffle() \
                .flat_map(splitter) \
                .set_parallelism(2) \
                .key_by(key_selector) \
                .sum(attribute_selector) \
                .inspect(print)  # Prints the contents of the
    # stream to stdout
    start = time.time()
    env_handle = env.execute()
    ray.get(env_handle)  # Stay alive until execution finishes
    end = time.time()
    logger.info("Elapsed time: {} secs".format(end - start))
    logger.info("Output stream id: {}".format(stream.id))
    print("end!")
