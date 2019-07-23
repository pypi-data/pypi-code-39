from policypools.AbstractThreadPoolExecutor import AbstractThreadPoolExecutor


class BoundedThreadPoolExecutor(AbstractThreadPoolExecutor):

    def __init__(self, max_q_size: int = 1, max_workers: int = 1, thread_name_prefix: str = ''):
        """
        Creates a thread pool bounded by the size and the num workers
        since there is no policy this pool throws exceptions
        :param max_q_size: the maximum size for the thread queue
        :param max_workers: the maximum number of concurrently running workers
        """
        super(BoundedThreadPoolExecutor, self).__init__(max_q_size=max_q_size,
                                                        max_workers=max_workers,
                                                        thread_name_prefix=thread_name_prefix)

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            future, worker, executing = super().submit(fn, *args, *kwargs)
            if not executing:
                if not len(self._pre_work_queue) >= self._max_q_size:
                    self._pre_work_queue.append(worker)
                else:
                    raise RuntimeError("Pre-work queue is full")
            return future

    submit.__doc__ = AbstractThreadPoolExecutor.submit.__doc__
