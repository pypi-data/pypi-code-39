# -*- coding: utf-8 -*-
import ray
import logging
import traceback
import time
from py_common_util.common.date_utils import DateUtils
from ray.experimental.streaming.streaming import Environment, DataStream
from skydl.ray.experimental.ray_streaming_util import DefaultStreamingSource, DefaultStreamingEnvConfig

# define logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RayStreamingExecutor:
    """
    ray流计算执行器，子类可以重写build_stream()方法
    """
    def __init__(self):
        logger.info("starting a streaming executor...")

    def execute_forever(self, env, stream):
        while(True):
            try:
                ray.get(env.execute())
                logger.info("Output stream id: {}".format(stream.id))
                logger.info("ray streaming is on!!!")
            except Exception as e:
                logger.error("Error Occurred on Ray Streaming: %s", str(e))
                traceback.print_exc()
                # TODO 发送运维警报
                time.sleep(30)  # 30秒后重启streaming

    def execute(self, streaming_parallelism=1, env=None):
        try:
            if not env:
                env = Environment(DefaultStreamingEnvConfig(parallelism=streaming_parallelism))
            stream = self.build_stream(streaming_parallelism=streaming_parallelism, env=env)
            self.execute_forever(env, stream)
        except Exception as e:
            logger.error("RayStreamingExecutor fail on execute(): %s", str(e))

    def build_stream(self, streaming_parallelism, env)->DataStream:
        """
        子类需要重写该方法构建具体的业务stream
        注意streaming算子类必须要预先install在所有节点中，或者都在该方法里定义
        @:param streaming_parallelism default value is 1
        @:param env
        @:return DataStream
        """
        def splitter(record):
            """convert record to another record list, e.g. [record]"""
            return [record]

        def handle_record(record):
            """处理回测的逻辑"""
            logger.info("record=" + record)
            time.sleep(1000)

        class FooStreamingSource(DefaultStreamingSource):
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
        stream = env.source(
            FooStreamingSource()
        ).set_parallelism(20).inspect(print_log)
        return stream










