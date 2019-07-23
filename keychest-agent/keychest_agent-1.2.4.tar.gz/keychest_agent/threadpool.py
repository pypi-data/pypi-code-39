#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@keychest.net>, 2019
"""
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@keychest.net'
__status__ = 'Development'

# this is mostly from:
# http://code.activestate.com/recipes/577187-python-thread-pool/

from threading import Thread, Event
from time import sleep
import socket
from multiprocessing import JoinableQueue

from keychest_agent.logger import logger


# default exception handler. if you want to take some action on failed tasks
# maybe add the task back into the queue, then make your own handler and pass it in
def default_handler(name, exception, *args, **kwargs):
    logger.error("Discovery worker error", name=name, cause=str(exception),
                 args=repr(args), kwargs=repr(kwargs))
    pass


def test_ip(_each_ip, port, timeout=5):
    # noinspection PyBroadException
    try:
        each_ip = str(_each_ip)
        _dns = False
        name = None
        # noinspection PyBroadException
        try:
            dns_resolv = socket.gethostbyaddr(each_ip)
            _dns = True
            name = dns_resolv[0]
        except:
            _dns = False

        _open = False
        # noinspection PyBroadException
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.settimeout(timeout)
            _result = sock.connect_ex((each_ip, port))
            if _result == 0:
                _open = True
            sock.close()
        except:
            pass
        logger.debug("Tested a new IP address", ip=each_ip, port=port, result=_open, name=name)
        if _open:
            return {'name': name, 'ip': each_ip, 'port': port}
        else:
            return None
    except Exception as ex:
        logger.trace("DNS resolve failed", cause=str(ex))
        # if dns doesn't work it will return an exception
        return None
        pass

# class for workers
class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self, name, queue, results, abort, idle, exception_handler):
        Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.results = results
        self.abort = abort
        self.idle = idle
        self.exception_handler = exception_handler
        self.daemon = True
        self.start()

    """Thread work loop calling the function with the params"""

    def run(self):
        # keep running until told to abort
        while not self.abort.is_set():
            # noinspection PyBroadException
            try:
                # get a task and raise immediately if none available
                func, args, kwargs = self.queue.get(False)
                self.idle.clear()
            except:
                # no work to do
                # if not self.idle.is_set():
                #  print >> stdout, '%s is idle' % self.name
                self.idle.set()
                continue

            try:
                # the function may raise
                _result = func(*args, **kwargs)
                if _result is not None:
                    self.results.put(_result)
            except Exception as e:
                # so we move on and handle it in whatever way the caller wanted
                self.exception_handler(self.name, e, args, kwargs)
            finally:
                # task complete no matter what happened
                self.queue.task_done()


# class for thread pool
class DiscoveryPool:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, thread_count, batch_mode=False, exception_handler=default_handler):
        # batch mode means block when adding tasks if no threads available to process
        self.queue = JoinableQueue(thread_count if batch_mode else 0)
        self.resultQueue = JoinableQueue(0)
        self.thread_count = thread_count
        self.exception_handler = exception_handler
        self.aborts = []
        self.idles = []
        self.threads = []

    def __del__(self):
        """
        Tell my threads to quit

        :return:
        """
        self.abort()

    def run(self, block=False):
        """
        Start the threads, or restart them if you've aborted
        :param block:
        :return:
        """
        # either wait for them to finish or return false if some arent
        if block:
            while self.alive():
                sleep(1)
        elif self.alive():
            return False

        # go start them
        self.aborts = []
        self.idles = []
        self.threads = []
        for n in range(self.thread_count):
            abort = Event()
            idle = Event()
            self.aborts.append(abort)
            self.idles.append(idle)
            thread = Worker('poolthread-%d' % n, self.queue, self.resultQueue, abort, idle, self.exception_handler)
            self.threads.append(thread)
        return True

    """Add a task to the queue"""

    def enqueue(self, func, *args, **kargs):
        self.queue.put((func, args, kargs))

    """Wait for completion of all the tasks in the queue"""

    def join(self):
        self.queue.join()

    """Tell each worker that its done working"""

    def abort(self, block=False):
        # tell the threads to stop after they are done with what they are currently doing
        for a in self.aborts:
            a.set()
        # wait for them to finish if requested
        while block and self.alive():
            sleep(1)

    """Returns True if any threads are currently running"""

    def alive(self):
        return True in [t.is_alive() for t in self.threads]

    """Returns True if all threads are waiting for work"""

    def idle(self):
        return False not in [_i.is_set() for _i in self.idles]

    """Returns True if not tasks are left to be completed"""

    def done(self):
        return self.queue.empty()

    """Get the set of results that have been processed, repeatedly call until done"""

    def results(self, wait=0):
        sleep(wait)
        results = []
        # noinspection PyBroadException
        try:
            while True:
                # get a result, raises empty exception immediately if none available
                results.append(self.resultQueue.get(False))
                self.resultQueue.task_done()
        except:
            pass
        return results

    # run the test


if __name__ == '__main__':
    def work(x):
        sleep(5)
        logger.debug('Threadpool finished - main', id=x)
        return x


    def wait_for_results(_pool):
        while not _pool.done() or not _pool.idle():
            for _result in _pool.results():
                logger.debug("Threadpool got results - main", result=str(_result))
        for _result in _pool.results():
            logger.debug("Threadpool got result - main", result=str(_result))

    p = DiscoveryPool(3)
    logger.debug("Threadpool queueing work - main")
    for i in range(10):
        p.enqueue(work, i)
    logger.debug("Threadpool starting work - main")
    p.run(True)
    logger.debug("Threadpool waiting - main")
    sleep(8)
    for result in p.results():
        logger.debug("Threadpool get result - main", result=str(result))

    logger.debug("Threadpool cancel remaining work - main")
    p.abort()
    logger.debug("Threadpool waiting and restarting - main")
    p.run(True)
    logger.debug("Threadpool restarted waiting for results - main")
    wait_for_results(p)
    logger.debug("Threadpool adding more work - main")
    for i in range(10, 17):
        p.enqueue(work, i)
    wait_for_results(p)
