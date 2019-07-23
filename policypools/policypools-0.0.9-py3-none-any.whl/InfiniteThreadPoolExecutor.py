from os import cpu_count

from policypools.AbstractThreadPoolExecutor import AbstractThreadPoolExecutor


class InfiniteThreadPoolExecutor(AbstractThreadPoolExecutor):

    def __init__(self, thread_name_prefix: str = ''):
        """
        Infinite thread pool, very large queue size and num workers set based off computer specs
        """
        super(InfiniteThreadPoolExecutor, self).__init__(max_q_size=0,
                                                         max_workers=cpu_count() * 10,
                                                         thread_name_prefix=thread_name_prefix)

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            future, worker, executing = super().submit(fn, *args, *kwargs)
            if not executing:
                self._pre_work_queue.put(worker, block=False)
            return future

    submit.__doc__ = AbstractThreadPoolExecutor.submit.__doc__
