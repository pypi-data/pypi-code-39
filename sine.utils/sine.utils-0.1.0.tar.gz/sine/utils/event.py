# encoding: UTF-8
import logging
from threading import Thread
from queue import Queue, Empty
from .threads import ReStartableThread


class EventManager:
    '''
    以 key 为键标识每个事件，对一个 key 可以添加或移除多个监听器。
    发布事件时传入 key 和数据 data ，后者将会传给监听器。

    可指定 logger 记录日志，否则默认使用 __name__ 的 logger 。
    '''

    def __init__(self, logger=None, eventBlockTime=0.1):
        self._eventQueue = Queue()
        self._listenThread = ReStartableThread(target=self._run)
        # 保存对应的事件的响应函数，每个键对应一个集合
        self._map = {}
        self.eventBlockTime = eventBlockTime
        self.logger = logger if logger else logging.getLogger(__name__)

    def _run(self, stop_event):
        while not stop_event.is_set():
            try:
                event = self._eventQueue.get(block=True, timeout=self.eventBlockTime)
                if stop_event.is_set():
                    return
                self.logger.info('process event. key=%s' %
                                  (str(event[0])))
                self._process(event)
            except Empty:
                pass

    def _process(self, event):
        try:
            for listener in self._map[event[0]]:
                def sub(listener=listener):
                    try:
                        listener(event[0], *event[1], **event[2])
                    except Exception as e:
                        self.logger.warn('listener exception. listener=%s, exception=%s, event_key=%s' %
                                         (str(listener), str(e), str(event[0])))
                        raise
                Thread(target=sub).start()
        except KeyError:
            pass

    def start(self):
        '''开始事件监听。'''
        self._listenThread.start()
        self.logger.info('listen start')

    def stop(self):
        '''停止事件监听。'''
        self._listenThread.stop()
        self._listenThread.join(1)
        self.logger.info('listen stop')

    def clear(self):
        '''清空事件。'''
        self._eventQueue.queue.clear()

    def addListener(self, key, listener):
        self.logger.info('add listener. key=%s, listener=%s' %
                          (str(key), str(listener)))
        self._map.setdefault(key, set()).add(listener)

    def removeListener(self, key, listener):
        try:
            self._map[key].remove(listener)
            self.logger.info('removed listener. key=%s, listener=%s' % (
                str(key), str(listener)))
        except KeyError:
            pass

    def sendEvent(self, key, *args, **kwargs):
        '''发布事件。以 key 标识；data 为数据，将会传给监听器。'''
        self.logger.info('send event. key=%s' %
                          (str(key)))
        self._eventQueue.put((key, args, kwargs))


__all__ = ['EventManager']
