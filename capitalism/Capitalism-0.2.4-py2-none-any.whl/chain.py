#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Chain Class

    Dispatch 'jobs' to factories or workers.

    @author: traitor
    @github: https://github.com/tbbatbb
'''

import sys, Queue, time, threading, signal
import worker, util, factory

reload(sys)
sys.setdefaultencoding('utf-8')


class Chain:
    def __init__(self, task_queue, jobs, in_factory=True, size=1, delay=1, debug=False, name=None, exit_on_done=False, timeout=2, split_array=True, int_handler=None):
        '''
            Initialize the job chain.

            @param task_queue:
                The original task queue.
            @param jobs:
                The jobs that need to be done. It's an Array, a serial of jobs should place in execution sequence.
            @param name:
                Name for the chain.
            @param int_handler:
                The function called when receive keyboard interrupt.
        '''
        # Check the parameters
        if (not isinstance(task_queue, Queue.Queue)
            and not isinstance(task_queue, list)):
            self.err('Task Queue Should Be An Instance Of Queue Or Array.')
            return
        # If the task_queue is an instance of queue
        if isinstance(task_queue, list):
            # Initialize a new queue
            self.t_q = Queue.Queue()
            for tk in task_queue:
                # Put all the tasks in the task queue
                try:
                    self.t_q.put(tk, block=False, timeout=timeout)
                except Queue.Full:
                    # Output error message
                    self.err('Task Queue Is Currently Full.')
                    continue
        else:
            self.t_q = task_queue
        # Jobs should be an array
        if not isinstance(jobs, list):
            self.err('Parameter Jobs Should Be A List Of Funtions.')
            return
        # Check each jobs
        for job in jobs:
            # If the job is not a function
            if not callable(job):
                util.err('Each Job Should Be A Function.')
                return
        # Set the attributes
        self.jobs = jobs
        self.info_out = debug
        self.name = name
        self.info_out = debug
        self.workers = []
        self.int_handler = int_handler
        # Initialize the factories of workers
        if in_factory:
            # If use factories to do jobs
            for i in range(len(jobs)):
                # Initialize a factory
                self.workers.append(
                    factory.Factory(
                        jobs[i],
                        task_queue=task_queue if i==0 else None,
                        size=size,
                        result_queue=None,
                        delay=delay,
                        debug=debug,
                        name='F{0}@{1}'.format(i, self.name),
                        exit_on_done=exit_on_done,
                        timeout=timeout,
                        split_array=split_array
                    )
                )
        else:
            # If use workers to do jobs
            for i in range(len(jobs)):
                # Initialize a factory
                w = worker.Worker(
                    jobs[i],
                    task_queue=task_queue if i==0 else None,
                    result_queue=None,
                    delay=delay,
                    debug=debug,
                    name='Worker-{0}@{1}'.format(i, self.name),
                    exit_on_done=exit_on_done,
                    timeout=timeout
                )
                w.setDaemon(True)
                self.workers.append(w)
        # Make workers connected
        for i in range(len(self.workers)-1):
            # Pipe the result to next worker
            self.workers[i].pipe(self.workers[i+1])
        # If the callback for keyborad interrupt is given
        signal.signal(signal.SIGINT, self.int_hdl)
        signal.signal(signal.SIGTERM, self.int_hdl)
        # Well, Initialized
        self.info('Initialized.')
    
    def start(self):
        '''
            Start all the factories or workers.
        '''
        for w in self.workers:
            w.start()
        return self
    
    def stop(self):
        '''
            Stop all the factories or workers.
        '''
        for w in self.workers:
            w.stop()
        return self
    
    def join(self):
        '''
            Join all the factories or workers.
        '''
        for w in self.workers:
            w.join()
        return self

    def info(self, i):
        '''
            Output some information.

            @param i:
                The information which is going to be outputed.
        '''
        # If not in the debug mode
        if not self.info_out:
            return
        util.info('[{0}]: {1}'.format(self.name, i))
    
    def err(self, e):
        '''
            Output some error information.

            @param e:
                The error information which is going to be outputed.
        '''
        # If not in the debug mode
        if not self.info_out:
            return
        util.err('[{0}]: {1}'.format(self.name, e))

    def int_hdl(self, num, frame):
        '''
            The callback for keyboard interrupt.
        '''
        # Stop all the workers
        self.stop()
        self.info('I\'m Exiting...')
        # If int_handler is callable
        if callable(self.int_handler):
            self.int_handler(num, frame)