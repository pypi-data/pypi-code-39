#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Chain Class

    Dispatch 'jobs' to factories or workers.

    @author: traitor
    @github: https://github.com/tbbatbb
'''

import sys, Queue, time, threading
import worker, util, factory

reload(sys)
sys.setdefaultencoding('utf-8')


class Chain:
    def __init__(self, task_queue, jobs, in_factory=True, size=1, delay=1, debug=False, name=None, exit_on_done=False, timeout=2, split_array=True):
        '''
            Initialize the job chain.

            @param task_queue:
                The original task queue.
            @param jobs:
                The jobs that need to be done. It's an Array, a serial of jobs should place in execution sequence.
            @param name:
                Name for the chain.
        '''
        # Check the parameters
        if not isinstance(task_queue, Queue.Queue):
            self.err('Task Queue Should Be An Instance Of Queue.')
            return
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
        self.t_q = task_queue
        self.jobs = jobs
        self.info_out = debug
        self.name = name
        self.workers = []
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
                self.workers.append(
                    worker.Worker(
                        jobs[i],
                        task_queue=task_queue if i==0 else None,
                        result_queue=None,
                        delay=delay,
                        debug=debug,
                        name='Worker-{0}@{1}'.format(i, self.name),
                        exit_on_done=exit_on_done,
                        timeout=timeout
                    )
                )
        # Make workers connected
        for i in range(len(self.workers)-1):
            # Pipe the result to next worker
            self.workers[i].pipe(self.workers[i+1])
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
