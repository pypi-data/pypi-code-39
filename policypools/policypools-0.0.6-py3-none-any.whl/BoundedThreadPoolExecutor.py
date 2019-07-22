from policypools.AbstractThreadPool import AbstractThreadPoolExecutor


class BoundedThreadPoolExecutor(AbstractThreadPoolExecutor):

    def __init__(self, max_q_size: int = 1, num_workers: int = 1, thread_name_prefix: str = ''):
        """
        Creates a thread pool bounded by the size and the num workers
        since there is no policy this pool throws exceptions
        :param max_q_size: the maximum size for the thread queue
        :param num_workers: the maximum number of concurrently running workers
        """
        super(BoundedThreadPoolExecutor, self).__init__(max_q_size, num_workers, thread_name_prefix)

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            future, worker = super().submit(fn, args, kwargs)
            self._work_queue.put(worker, block=False)
            self._adjust_thread_count()
            return future

    submit.__doc__ = AbstractThreadPoolExecutor.submit.__doc__
