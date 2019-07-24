# -*- coding: utf-8 -*-
import ray
import logging
import traceback
import time

from py_common_util.common.date_utils import DateUtils
from ray.experimental.streaming.communication import QueueConfig
from ray.experimental.streaming.streaming import Environment

# define logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RayStreamingExecutor:
    """
    ray流计算执行器，子类可以重写execute()方法
    """
    def __init__(self):
        logger.info("starting a streaming executor...")

    def execute_without_try(self, env, stream):
        # stream = self.env.source(
        #         NocodeBacktestStreamingSource()
        #     ).set_parallelism(12).flat_map(
        #         flatmap_fn=Source.splitter
        #     ).set_parallelism(12).map(
        #         map_fn=self.handle_record1,
        #         name="nocode_backtest_map"
        #     ).set_parallelism(100)
        # stream = env.source(
        #     NocodeBacktestStreamingSource()
        # ).set_parallelism(100).inspect(print)
        ray.get(env.execute())
        logger.info("Output stream id: {}".format(stream.id))
        logger.info("ray streaming is on!!!")

    def execute_forever(self, env, stream):
        while(True):
            try:
                self.execute_without_try(env, stream)
            except Exception as e:
                logger.error("Error Occurred on Ray Streaming: %s", str(e))
                traceback.print_exc()
                # TODO 发送运维警报
                time.sleep(30)  # 30秒后重启streaming

    def execute(self, streaming_parallelism=1, env=None):
        """注意streaming算子类必须要预先install在所有节点中，或者在该方法里定义"""
        def splitter(record):
            """convert record to another record list, e.g. [record]"""
            return [record]

        def handle_record(record):
            """处理回测的逻辑"""
            logger.info("record=" + record)
            time.sleep(1000)
            
        class DefaultStreamingEnvConfig(object):
            """
            default ray streaming env config
            """
            def __init__(self, max_size=999999,
                         max_batch_size=99999,
                         max_batch_time=0.01,
                         prefetch_depth=10,
                         background_flush=False,
                         parallelism=1):
                self.queue_config = QueueConfig(
                    max_size=max_size,
                    max_batch_size=max_batch_size,
                    max_batch_time=max_batch_time,
                    prefetch_depth=prefetch_depth,
                    background_flush=background_flush)
                self.parallelism = parallelism

        class DefaultStreamingSource(object):
            """default streaming source implement"""
            def get_next(self):
                # get current record
                return None

        class NocodeBacktestStreamingSource(DefaultStreamingSource):
            def __init__(self):
                self._count = 0

            def get_next(self):
                self._count += 1
                if self._count % 20 == 0:
                    # print("***get_next_nvl***:" + str(self._count))
                    return "uuunited\nStates"
                else:
                    return "United States"

        def print_log(content):
            logger.info(content)
            time.sleep(10)
            logger.info(content + ",finished:" + DateUtils.now_to_str())
        try:
            env = Environment(DefaultStreamingEnvConfig(parallelism=streaming_parallelism))
            stream = env.source(
                NocodeBacktestStreamingSource()
            ).set_parallelism(20).inspect(print_log)
            self.execute_forever(env, stream)
        except Exception as e:
            logger.error("RayStreamingExecutor fail on execute(): %s", str(e))








