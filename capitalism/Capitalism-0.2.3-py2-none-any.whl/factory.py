#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Factory Class

    Get a task from the 'task_queue',
    do the job with function 'target',
    finally put the results into 'result_queue'.

    @author: traitor
    @github: https://github.com/tbbatbb
'''

import sys, Queue, time, threading
import worker, util

reload(sys)
sys.setdefaultencoding('utf-8')


class Factory:
    def __init__(self, target, task_queue=None, size=1, result_queue=None, delay=1, debug=False, name=None, exit_on_done=False, timeout=2, split_array=True):
        '''
            Initialize the thread pool

            @param task_queue:
                Task queue which contains the tasks to be done.
                Actually, the queue contains parameters for 'target' function.
            @param target:
                Actual function to deal with each parameters in 'task_queue'.
            @param size:
                How many workers can I own.
            @param result_queue:
                A queue for placing the results.
            @param delay:
                How much time should the thread to sleep after finishing a job.
            @param debug:
                Wether to output the information.
            @param name:
                The name of the worker thread.
            @param exit_on_done:
                Wether exit the loop when there is no task in the queue.
            @param timeout:
                How much time should the thread wait for getting a job or putting results.
            @param split_array:
                When the job is done, should workers split the result before put it in result queue if it's an array?
        '''
        # Check the parameters
        if not target:
            return
        # Set several property
        self.name = name
        self.t_q = task_queue
        self.r_q = result_queue
        self.info_out = debug
        self.workers = []
        # Initilize workers in the factory
        for i in range(size):
            # Append a new worker to the factory
            self.workers.append(
                worker.Worker(
                    target,
                    task_queue=task_queue,
                    result_queue=result_queue,
                    delay=delay,
                    debug=debug,
                    name='Worker-{0}@{1}'.format(i, name),
                    exit_on_done=exit_on_done,
                    timeout=timeout,
                    split_array=split_array
                )
            )
        # Print the information
        self.info('Initilized.')

    def start(self):
        '''
            Make each worker in the factory to work.
        '''
        for w in self.workers:
            # Hurry up! Start working!!!
            w.start()
        # Well, they're working now!
        self.info('All The Workers Start Working.')
        return self
    
    def join(self):
        '''
            Join all the worker threads.
        '''
        for w in self.workers:
            # Join now
            w.join()
        # Well, all joined
        self.info('All The Workers Have Joined.')
        return self

    def stop(self):
        '''
            Make each worker in the factory to stop working.
        '''
        for w in self.workers:
            # Stop now
            w.stop()
        # Well, all stopped???
        self.info('All The Workers Have Stopped.')
        return self

    def set_task_queue(self, target):
        '''
            Set task queue to target

            @param target:
                The new task queue.
        '''
        # If target queue is not valid
        if not target:
            # Print some information
            self.err('Oops! Not A Valid Task Queue.')
            return self
        # Set task queue of me
        self.t_q = target
        # Set the task queue of each worker
        for w in self.workers:
            w.set_task_queue(target)
        return self
    
    def set_result_queue(self, target):
        '''
            Set result queue to target

            @param target:
                The new result queue.
        '''
        # If target queue is not valid
        if not target:
            # Print some information
            self.err('Oops! Not A Valid Result Queue.')
            return self
        # Set result queue of me
        self.r_q = target
        # Set the result queue of each worker
        for w in self.workers:
            w.set_result_queue(target)
        return self

    def pipe(self, next_factory):
        '''
            Transfer the results to next factory.

            @param next_factory:
                Next factory who receives my result as task.
        '''
        # Can I transfer to None????
        if not next_factory:
            self.err('How Can I Transfer My Result To NONE???')
            return self
        # # If next factory does'nt have any worker
        # if len(next_factory.workers) <= 0:
        #     self.err('Well, The Target Factory Does\'nt Have Any Worker.')
        #     return
        # Get the result queue
        target_queue = next_factory.t_q
        if not self.r_q and not target_queue:
            # Generate a temprary queue
            tmp_queue = Queue.Queue()
            # Set result queue
            self.set_result_queue(tmp_queue)
            # Set task queue of next factory
            next_factory.set_task_queue(tmp_queue)
        elif self.r_q:
            # Set task queue of next factory
            next_factory.set_task_queue(self.r_q)
        else:
            # Set result queue of me
            self.set_result_queue(target_queue)
        return next_factory

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

