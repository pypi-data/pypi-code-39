# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 21:59:00 2019

@author: Reuben
"""

import weakref

class SignalContainer(dict):
    ''' Holds a collection of signals '''
    
    def signal(self, name=None, **kwargs):
        name = len(self) if name is None else name
        s = Signal(name=name, **kwargs)
        self[name] = s
        return s
    
    def mute_all(self):
        for key, signal in self.items():
            signal.mute()

    def unmute_all(self):
        for key, signal in self.items():
            signal.unmute()

    def reset_all(self):
        for key, signal in self.items():
            signal.reset()
    
    
default_container = SignalContainer()
signal = default_container.signal

    
class Signal():
    ''' The core signal class '''
    
    def __init__(self, name=None, doc=None, receiver_limit=None, condition=None):
        self.reset()
        self._name = name
        self._doc = doc
        self._receiver_limit = receiver_limit
        if condition is not None:
            self.add_condition(condition)
    
    def add_condition(self, condition):
        ''' Add a condition that the signal must pass to be received '''
        self._conditions[condition.name] = condition
        self.emit = self._conditioned_emit
        return True
        
    def remove_condition(self, name):
        ''' Remove a condition that the signal must pass to be received '''
        try:
            del self._conditions[name]
        except KeyError:
            pass
        if len(self._conditions) == 0:
            self.emit = self._emit
    
    def connect(self, receiver, **receiver_kwargs):
        ''' Store weakref of receiver function or method to call '''
        if self.n == self._receiver_limit:
            raise KeyError('Limit of receivers (or suppliers) reached.')
        receiver_id = self._next_id
        if hasattr(receiver, '__self__') and hasattr(receiver, '__func__'):
            ref = weakref.WeakMethod(receiver)
            obj = receiver.__self__
        else:
            ref = weakref.ref(receiver)
            obj = receiver
        self._receivers[receiver_id] = ref
        self._receiver_kwargs[receiver_id] = receiver_kwargs
        weakref.finalize(obj, self.disconnect, receiver_id)
        self._next_id += 1
        return receiver_id
    
    @property
    def n(self):
        ''' Number of recievers '''
        return len(self._receivers)

    @property
    def receivers_present(self):
        ''' A boolean check if receivers are present '''
        return len(self._receivers) > 0
    
    @property
    def name(self):
        ''' The signal name '''
        return self._name
    
    def disconnect(self, receiver_id):
        ''' Disconnect a receiver '''
        try:
            del self._receivers[receiver_id]
            del self._receiver_kwargs[receiver_id]
        except KeyError:
            pass
        return True

    def _emit(self, **kwargs):
        ''' The standard emit method 
        
        Note: The 'emit' method is set to this method normally.
        '''
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            receiver(**kwargs)    
            
    def _conditioned_emit(self, **kwargs):
        ''' A conditioned emit method '''
        for receiver_id, ref in self._receivers.items():
            condition_pass = True
            for condition_name, condition in self._conditions.items():
                rec_kwargs = self._receiver_kwargs[receiver_id]
                all_kwargs = {**rec_kwargs, **kwargs}
                condition_pass &= condition.check(**all_kwargs)
            if condition_pass:
                self._emit(**kwargs)

    def _muted(self, **kwargs):
        pass
            
    def mute(self):
        self._prev_emit = self.emit
        self.emit = self._muted

    def unmute(self):
        self.emit = self._prev_emit
        del self._prev_emit
    
    def fetch(self, **kwargs):
        ''' Get a return value from a single supplier '''
        if self._receiver_limit != 1:
            raise KeyError('Signal must be set to have only 1 supplier.')
        if self.n == 0:
            raise KeyError('No suppliers')
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            return receiver(**kwargs)

    def fetch_all(self, **kwargs):
        ''' Get a return value from a single supplier '''
        if self.n == 0:
            raise KeyError('No suppliers')
        ret = []
        for receiver_id, ref in self._receivers.items():
            receiver = ref()
            ret.append(receiver(**kwargs))
        return ret

    def reset(self):
        self._receivers = {}
        self._receiver_kwargs = {}
        self._next_id = 0
        self._conditions = {}
        self.emit = self._emit


class Condition():
    ''' A template for a signal condition '''
    name = 'default'
    def check(self, **kwargs):
        ''' The main check call - must return a boolean '''
        raise NotImplementedError()


class Wired():
    def __new__(cls, *args, **kwargs):
        ''' Called at instance creation '''
        def register_signals(inst):
            try:
                sigs = inst.__getattribute__('_connected_signals')
                for name, s, receiver_kwargs in sigs:
                    s.connect(inst.__getattribute__(name), **receiver_kwargs)
            except AttributeError:
                pass
        
        inst = super().__new__(cls, *args, **kwargs)
        register_signals(inst)
        return inst
        

def receive(s, **receiver_kwargs):
    ''' A decorator to connect functions and methods automatically '''
    if not isinstance(s, list):
        s = [s]
        
    class Decorator():
        # See https://stackoverflow.com/questions/2366713/can-a-python-decorator-of-an-instance-method-access-the-class
        def __init__(self, fn):
            self.fn = fn
    
        def __set_name__(self, owner, name):
            # Called at class creation
            if not hasattr(owner, '_connected_signals'):
                owner._connected_signals = []
            cs = owner._connected_signals
            for signal in s:
                cs.append([name, signal, receiver_kwargs])
            setattr(owner, name, self.fn) # Replace decorator with original function
        
    return Decorator


def supply(s, **receiver_kwargs):
    ''' A special case of reciever where there must be only one source '''
    if s._receiver_limit != 1:
        raise KeyError('Signal must be set to have only 1 supplier.')
    return receive(s, **receiver_kwargs)


def fn_receive(s, **receiver_kwargs):
    ''' For functions '''
    if not isinstance(s, list):
        s = [s]
    def decorator(fn):
        for signal in s:
            signal.connect(fn, **receiver_kwargs)
        return fn
    return decorator


def fn_supply(s, **receiver_kwargs):
    if s._receiver_limit != 1:
        raise KeyError('Signal must be set to have only 1 supplier.')
    return fn_receive(s, **receiver_kwargs)
