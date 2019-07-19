import threading
import time
import datetime as dt
from threading import Semaphore,Timer
import queue
import math
import sys
import os


class loopi:
    def __init__(self,**kwargs):
        
        self.__kwargs=kwargs
        def _nslice(s, n, truncate=False, reverse=False):
            """Splits s into n-sized chunks, optionally reversing the chunks."""
            assert n > 0
            while len(s) >= n:
                if reverse: yield s[:n][::-1]
                else: yield s[:n]
                s = s[n:]
            if len(s) and not truncate:
                yield (s)
        self._loop=False
        self.print_it=False
        self._start_time=0
        self._input=[0]
        if(('target' in self.__kwargs) and (self.__kwargs['target'] is not None)):
            if(('n_splits' in self.__kwargs) and (self.__kwargs['n_splits'] is not None)):
                self._input=_nslice(self.__kwargs['target'],self.__kwargs['n_splits'])
        else:
            self._input=[0]
        self.sequence = queue.Queue()
        self._minutes=0
        self._seconds=0
        self._hours=0
        self._total_seconds=0
        self._timedelta=dt.timedelta(hours=0,minutes=0,seconds=0,milliseconds=0 ,microseconds=0)
        self._strftime=0
        self._activeEvent=False
        self._lock = threading.Lock() 
        self._timerEnd=threading.Event()
        self._killit=threading.Event()
        self._keep_alive=False
        self._target_function=None
        self.pause=0
        self._kwargs=None
        self._timer_thread=None
        self._running_thread=None
        self.counter=0
        self.start_time=0
        self.now=0
        self.elapsed=dt.timedelta(hours=0,minutes=0,seconds=0,milliseconds=0 ,microseconds=0)
        self.total_seconds=0
        #put slices in queue
        for item in self._input:
            self.sequence.put(item)
        if(not any([key in self.__dict__ for key in self.__kwargs.keys()])):
            self.__dict__.update(kwargs)
        else:
            raise ValueError('naming conflict detected', [ key for key in kwargs.keys() if(key in self.__dict__)])
        
        
    def apply_to(self,function,**kwargs):
        self._target_function=function
        self._kwargs=kwargs
        
    def s_print(self,*a, **b):
        with (self._lock):
            print(*a, **b)
            
        
    def _trigger(self,):
        self._timerEnd.clear()
        while (not self.sequence.empty()):
            
            if(not self._loop):
                self._loop=False
                self._timerEnd.set()
                break
            else:
                time.sleep(1)
                td=dt.datetime.now()-self._start_time
                self._timedelta=td
                self._hours, remainder = divmod(td.seconds, 3600)
                self._minutes, self._seconds = divmod(remainder, 60)
                self._total_seconds=td.total_seconds()
                self._strftime="{:0>2}:{:0>2}:{:0>2}".format(int(self._hours),int(self._minutes),int(self._seconds))
                if (self.print_it): 
                    self.s_print(self._strftime,end='\r')
        if (self.print_it):
            self.s_print('\r')
        self._loop=False
        self._timerEnd.set()
        

    def _start(self,print_it=False):
        if(not self._loop):
            self.print_it=print_it
            self._start_time=dt.datetime.now()

            main_trigger=threading.Thread(target=self._trigger)
            main_trigger.setDaemon(True)
            self._loop=True
            self._timer_thread=main_trigger
            main_trigger.start()  
        
    def stop(self,):
        self._loop=False
    
    def get(self,):
        return(self.sequence.get())
    
    def kill(self,):
        while (self._keep_alive):
            self._keep_alive=False
            if(self._loop):
                self._loop=False
    
    def _eventTrigger(self,total_seconds):
        while (not self.sequence.empty()):
            if(self._total_seconds>=total_seconds):
#                 self.s_print('triggered',self._loop)
                self.stop()
                break

    def addTimeEvent(self,total_seconds=None): 
        event_trigger=threading.Thread(target=self._eventTrigger,args=(total_seconds,))
        event_trigger.setDaemon(True)
        event_trigger.start() 

    def _simpleloopTrigger(self,every):
        while (not self.sequence.empty()):
            if(not self._keep_alive):
                break
            else:
                time.sleep(every)
                if(self._target_function and self._keep_alive):
                    self._target_function(self,**self._kwargs)
                else:
                    break
    def _loop_timer(self,):
        while (not self.sequence.empty()):
            if(not self._keep_alive):
                break
            else:
                if(self._target_function and self._keep_alive):
                    self.now=dt.datetime.now()
                    self.elapsed=self.now-self.start_time
                    self.total_seconds=self.elapsed.total_seconds()
                else:
                    break        
        
    def startSimpleLoop(self,every=None):
        loop_trigger=threading.Thread(target=self._simpleloopTrigger,args=(every,))
        loop_trigger.setDaemon(True)
        self._keep_alive=True
        self._running_thread=loop_trigger
        loop_trigger.start() 
        
    def _timedloopTrigger(self,every):
        while (not self.sequence.empty()):
            if(not self._keep_alive):
                break
            else:
                time.sleep(every)
                if(self.pause>0):
                    self.s_print("Process suspended for ", self.pause," seconds")
                    self._start(True)
                    time.sleep(self.pause)
                    self.pause=0
                    self.stop()
                    self._timerEnd.wait()
                if(self._target_function and self._keep_alive):
                    if(self.pause>0 and not self._timerEnd.isSet()):
                        continue
                    elif(self.pause==0):
                        self.counter=self.counter+1
                        self._target_function(self,**self._kwargs)
                else:
                    break
        
    def startTimedLoop(self,every=None):
        loop_trigger=threading.Thread(target=self._timedloopTrigger,args=(every,))
        loop_trigger.setDaemon(True)
        loop_timer_trigger=threading.Thread(target=self._loop_timer,args=())
        loop_timer_trigger.setDaemon(True)
        self._keep_alive=True
        self.counter=0
        self._running_thread=loop_trigger
        self.start_time=dt.datetime.now()
        loop_trigger.start() 
        loop_timer_trigger.start()
        loop_trigger.join()
        
        
class loopimer:
    def __init__(self, *args,**kwargs):
        self.kwargs=kwargs
        self.ltimer=loopi(**self.kwargs)
    def __call__(self, func):
        def wrapper(*args,**kwargs):
            self.ltimer.apply_to(func,**kwargs)
            self.ltimer.startTimedLoop(self.kwargs['every'])
            return

        return wrapper
