from threading import Thread

from six.moves import queue
from abc import abstractmethod


class AbstractThreadPool:

    def __init__(self, max_q_size: int = 1, num_workers: int = 1):
        """
        Generic Abstract Thread Pool
        :param max_q_size: the maximum size for the thread queue
        :param num_workers: the maximum number of concurrently running workers
        """
        assert max_q_size >= 1 and num_workers >= 1
        self.__max_size = max_q_size
        self.__num_workers = num_workers
        self._thread_q = queue.Queue(self.__max_size)
        self.__workers = []
        self.__terminate = False
        self.__manager_thread = Thread(target=self.__start)
        self.__manager_thread.setDaemon(True)
        self.__manager_thread.start()

    def terminate(self):
        """
        Terminates the thread pool, stops the process of starting new threads and waits for all
        currently running threads to finish execution for safe termination
        :return: None
        """
        self.__terminate = True
        for thread in self.__workers:
            if thread.is_alive():
                thread.join()

    def __start(self):
        """
        Loops until termination adding and removing workers as necessary with the given max
        :return: None
        """
        while not self.__terminate:
            filled_dead_thread = False
            for i, thread in enumerate(self.__workers):
                if not thread.is_alive():
                    try:
                        self.__workers[i] = self._thread_q.get(block=False)
                        filled_dead_thread = True
                        self.__workers[i].setDaemon(True)
                        self.__workers[i].start()
                        break
                    except queue.Empty:
                        break
            if not filled_dead_thread:
                if self.__num_workers > len(self.__workers):
                    try:
                        self.__workers.append(self._thread_q.get(block=False))
                        self.__workers[-1].setDaemon(True)
                        self.__workers[-1].start()
                    except queue.Empty:
                        continue
            else:
                dead_thread_indicies = [i for i, thread in enumerate(self.__workers) if not thread.is_alive()]
                for dead_thred_index in dead_thread_indicies:
                    del self.__workers[dead_thred_index]

    @abstractmethod
    def submit(self, thread: Thread):
        """
        Submits a new thread, each policy will change how this method is implemented
        :param thread: the given thread to run
        :return: None
        """
        pass
