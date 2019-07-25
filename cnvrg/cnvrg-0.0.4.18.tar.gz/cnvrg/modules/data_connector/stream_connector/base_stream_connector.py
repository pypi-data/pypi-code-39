from cnvrg.modules.data_connector.base_connector import BaseConnector
from multiprocessing import Process
class BaseStreamConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        ## topic => [callbacks]
        self.subs = {}
        ## topic => Proccess
        self.proccess = {}
        super(BaseStreamConnector, self).__init__(*args, **kwargs)

    def producer(self):
        raise Exception("Not Implemented")

    def consumer(self, *topics, **kwargs):
        raise Exception("Not Implemented")


    def __init_sub(self, topic, **kwargs):
        def __subscription(stream_connector, topic, **kwargs):
            _consumer = stream_connector.consumer(topic, **kwargs)
            for msg in _consumer:
                for cb in stream_connector.subs.get(topic):
                    cb(msg)

        t = Process(target=__subscription, args=(self, topic), kwargs=kwargs)
        t.start()
        self.proccess[topic] = t

    def subscribe(self, topic, callback, **kwargs):
        if topic not in self.subs:
            self.__init_sub(topic, **kwargs)
            self.subs[topic] = []
        self.subs[topic].append(callback)


    def unsubscribe(self, topic):
        if topic not in self.proccess:
            return
        self.proccess[topic].terminate()
        self.subs[topic] = None

    def send(self, topic, **kwargs):
        """
        Send a specific **kwargs to a topic
        :param topic: topic to send to
        :return: Future
        """
        return self.producer().send(topic, **kwargs)
