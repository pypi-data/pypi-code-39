import threading
from abc import abstractmethod
from datetime import datetime
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed

from munch import Munch

from api.handler.ICacheAbleHandler import ICacheAbleHandler
from api.handler.ITaskHandler import ITaskHandler
from api.handler.outputer.IBatchOutputer import IBatchOutputer
from api.model.BatchOutputPipe import BatchOutputPipe
from api.model.ResultVO import *
from client import DataCrawlClient
from schedule.utils.log import TaskLogFileAppender


class AbstractBatchCrawl(ITaskHandler, IBatchOutputer, ICacheAbleHandler):
    # 由于这个的实现有可能是 单例的,所以要使用ThreadLocal
    def __init__(self):
        super().__init__()
        self.__code_local_host = threading.local()
        self.__process_id_local = threading.local()
        self.__execution_message_local = threading.local()

        self.__tasks_local_host = threading.local()

        self.killed = False

    def __action(self, data_crawl, output_stream, params, is_finished, messages):
        # 异步线程来对数据进行输入
        try:
            self.set_local_code(data_crawl.site + "_" + data_crawl.projectCode + "_" + data_crawl.code)
            self.set_process_id(params.get("__processLogId__"))
            TaskLogFileAppender.prepare_to_log(datetime.strptime(params["__triggerTime__"], "%Y-%m-%d %H:%M:%S"),
                                               params["__logId__"])
            self.__execution_message_local.content = []
            self.do_crawl(BatchOutputPipe(output_stream, len(data_crawl.outputFdCodes)), params)
        finally:
            is_finished[0] = True
            messages[0] = "success" if self.__execution_message_local.content is None or len(
                self.__execution_message_local.content) == 0 else str(self.__execution_message_local.content)
            # 清理 MessageLocal 和 LocalCode
            self.clear_local_code()
            self.clear_process_id()
            self.__execution_message_local.content = None
            TaskLogFileAppender.end_log()

    def execute(self, params: dict):

        if params is None or len(params) == 0 or ("site_" not in params) or ("projectCode_" not in params) or (
                "code_" not in params):
            # 不存在crawl的信息,没法执行
            return ResultVO(FAIL_CODE, "执行失败,没有Crawl的信息")

        self.__tasks_local_host.tasks = []

        output_stream = Queue()

        self.killed = False

        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="batch-ce-") as executor:
            # 这个的逻辑是这样的:
            # 1.传入一个 队列进去,然后异步等待这个线程做完
            try:
                # 找到对应的dataCrawl
                data_crawl: Munch = DataCrawlClient.get(params["site_"], params["projectCode_"], params["code_"])

                if data_crawl is None or data_crawl.type != "CUSTOM":
                    return ResultVO(FAIL_CODE, f"执行失败,没有找到Code:{params['site_']}的Crawl,或者该Crawl类型不为Custom")

                is_finished = [False]
                messages = [None]

                self.__tasks_local_host.tasks.append(
                    executor.submit(self.__action, data_crawl, output_stream, params, is_finished, messages))

                # 增加发送结果的线程
                self.__tasks_local_host.tasks.append(
                    executor.submit(self.batch_output, params["code_"], data_crawl.outputFdCodes,
                                    is_finished, output_stream))

                # 阻塞主线程
                for future in as_completed(self.__tasks_local_host.tasks):
                    try:
                        data = future.result()
                    except Exception as e:
                        return ResultVO(FAIL_CODE, f"执行失败,Code:{params['code_']}的Crawl,原因:{str(e)}")

                if messages[0] is not None:
                    return ResultVO(SUCCESS_CODE, messages[0])

                return SUCCESS
            finally:
                self.__tasks_local_host.tasks.clear()
                executor.shutdown(wait=True)
                output_stream.queue.clear()

    def kill(self):
        self.killed = True
        if self.__tasks_local_host.tasks is not None:
            for task in self.__tasks_local_host.tasks:
                try:
                    task._stop()
                except:
                    pass

    def is_killed(self):
        return self.killed

    def get_execution_message_cache(self):
        """
        返回message_cache
        :return:
        """
        return self.__execution_message_local.content

    def get_batch_size(self) -> int:
        # TODO 先写死100
        return 100

    def get_code_thread_local(self):
        """
        实现上下文的code
        :return:
        """
        return self.__code_local_host

    def get_process_thread_local(self):
        """
        上下文的Id
        :return:
        """
        return self.__process_id_local

    @abstractmethod
    def do_crawl(self, output_stream: BatchOutputPipe, params: dict):
        """
        真正执行数据挖掘的逻辑
        :param output_stream: 数据的输出
        :param params: 需要的参数
        :return:
        """
