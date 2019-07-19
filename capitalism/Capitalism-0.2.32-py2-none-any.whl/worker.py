#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Worker Class

    Get a task from the 'task_queue',
    do the job with function 'target',
    finally put the results into 'result_queue'.

    @author: traitor
    @github: https://github.com/tbbatbb
'''

import sys, Queue, time, threading
import util

reload(sys)
sys.setdefaultencoding('utf-8')


class Worker(threading.Thread):
    def __init__(self, target, task_queue=None, result_queue=None, delay=1, debug=False, name=None, exit_on_done=False, timeout=2, split_array=True):
        '''
            Initialize the thread

            @param task_queue:
                Task queue which contains the tasks to be done.
                Actually, the queue contains parameters for 'target' function.
            @param target:
                Actual function to deal with each parameters in 'task_queue'.
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
                When the job is done, should I split the result before put it in result queue if it's an array?
        '''
        # Check the parameters
        if not target:
            return
        threading.Thread.__init__(self)
        # Set several property
        self.t_q = task_queue
        self.do = target
        self.r_q = result_queue
        self.sleep_time = delay
        self.info_out = debug
        self.name = name
        self.exit_on_done = exit_on_done
        self.timeout = timeout
        self.should_stop = False
        self.split_arr = split_array
        # Print the information
        self.info('Initilized.')
    
    def run(self):
        '''
            Actual loop for doing the job.
        '''
        # If task queue is not set
        if not self.t_q:
            # Print information
            self.err('The Task Queue Hasn\'t Been Set.')
            return
        while not self.should_stop:
            try:
                # Try to get a job
                param = self.t_q.get(block=False, timeout=self.timeout)
            except Queue.Empty:
                # The task queue is empty
                self.info('Task Queue Is Empty At The Present.')
                if self.exit_on_done:
                    # Print some information
                    self.info('Exit Due To Empty Task Queue.')
                    break
                # Sleep for some time
                time.sleep(self.sleep_time)
                continue
            except Exception, e:
                # Print the error
                self.err(e)
                continue
            # OK, now we got the task, and get the result
            self.result = self.do(param)
            # If there is no result queue?
            if isinstance(self.r_q, Queue.Queue):
                # Well, we need to put the result into result queue
                try:
                    # Try to put the result
                    if self.split_arr and isinstance(self.result, list):
                        for i in range(len(self.result)):
                            self.r_q.put(self.result[i], block=False, timeout=self.timeout)
                    else:
                        self.r_q.put(self.result, block=False, timeout=self.timeout)
                except Queue.Full:
                    # The result queue is full
                    self.err('Result Queue Is Full At The Present.')
                except Exception, e:
                    # Print the error
                    self.err(e)
            self.t_q.task_done()
            # I'm so tired, can I sleep for a while?
            time.sleep(self.sleep_time)
        # WHO KILLED ME!!!!!!!!!
        self.info('Oops! I Was Killed. Do You Know Who It Is?')
    
    def stop(self):
        '''
            Stop the thread.
        '''
        self.should_stop = True
        return self

    def set_task_queue(self, target):
        '''
            Set my task queue to target

            @param target:
                Target queue to get tasks
        '''
        # If not a valid target
        if not target:
            # Print some information
            self.err('Oops! The New Task Queue Is Invalid.')
            return
        # Set the task queue
        self.t_q = target
        return self

    def set_result_queue(self, target):
        '''
            Set my result queue to target

            @param target:
                Target queue to put results
        '''
        # If not a valid target
        if not target:
            # Print some information
            self.err('Oops! The New Result Queue Is Invalid.')
            return
        # Set the result queue
        self.r_q = target
        return self

    def pipe(self, poor_guy):
        '''
            Pipe the result of me to next poor guy.

            @param poor_guy:
                Who is the next poor guy?
                The guy will use my result queue as its task queue.
        '''
        # The next is None?????
        if not poor_guy:
            self.err('How Can I Transfer The Result To NONE?????')
            return self
        if not self.r_q and not poor_guy.t_q:
            # Generate a temprary queue
            tmp_queue = Queue.Queue()
            # Set the queue
            self.set_result_queue(tmp_queue)
            poor_guy.set_task_queue(tmp_queue)
        elif self.r_q:
            # Set target worker's task queue
            poor_guy.set_task_queue(self.r_q)
        else:
            # Set my result queue
            self.set_result_queue(poor_guy.t_q)
        return poor_guy

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
        util.err('[{0}]: {1}'.format(self.name, e))

