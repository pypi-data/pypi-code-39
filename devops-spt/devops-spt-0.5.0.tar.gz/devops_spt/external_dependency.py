"""External dependency management module"""
from abc import ABC, abstractmethod


class ExternalDependency(ABC):
    """Define interface for managing external dependencies"""

    @abstractmethod
    def existing(self):
        """
        Return installed version
        OR, set existing = None in subclass if only update is desired
        """

    @abstractmethod
    def latest(self):
        """
        Return latest version available
        OR, set latest = None in subclass if only update is desired
        """

    @abstractmethod
    def update(self, verbose=False):
        """Update installed version to latest if necessary"""
