import abc
import time
from typing import Any

from .exceptions import EmptyQueueException


class Queue(metaclass=abc.ABCMeta):
    def __init__(self, name: str):
        """Make this be a new queue.

        Args:
            name: the name of the queue

        Requires:
            name is not None

        """
        self.__name = name

    @property
    def name(self):
        """Name of the queue.

        Returns:
            The name of the queue

        """
        return self.__name

    def __len__(self):  # noqa: D105
        raise NotImplementedError()

    def put(self, element: Any, serializer: callable = None) -> None:
        """Put an element in the queue.

        Args:
            element: the element to be added
            serializer: an optionnal serializer for the element


        Requires:
            element is not None
            if given serializer is a callable with one parameter

        Effects:
            Serialize the element and put it in the queue

        """
        raise NotImplementedError()

    def get(self, deserializer: callable = None, timeout=5) -> Any:
        """Get an element from the queue.

        Args:
            deserializer: an optionnal deserializer for the element
            timeout: a timeout for the element to be given

        Requires:
            if given, deserializer is a callable with one parameter

        Raise:
            EmptyQueueException is the queue is empty after the timeout

        Returns:
            the deserialized element

        """
        raise NotImplementedError()


class InMemoryQueue(Queue):
    def __init__(self, name):  # noqa: D107
        super().__init__(name)
        self.__queue = []

    def __len__(self):  # noqa: D105
        return len(self.__queue)

    def put(
        self, element: Any, serializer: callable = None
    ) -> None:  # noqa: D102
        if serializer is not None:
            element = serializer(element)
        self.__queue.insert(0, element)

    def get(
        self, deserializer: callable = None, timeout=5
    ) -> Any:  # noqa: D102
        for _ in range(timeout):
            try:
                element = self.__queue.pop()
                if deserializer is not None:
                    element = deserializer(element)
                return element
            except IndexError:
                time.sleep(1)
        raise EmptyQueueException()
