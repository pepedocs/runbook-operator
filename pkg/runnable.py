from __future__ import annotations
from abc import ABCMeta, abstractmethod

from pkg.result import RunnableResult


import pkg.logger as logger

class Runnable(metaclass=ABCMeta):
    def __init__(self, managed_by: str , type: str, logger_name: str = __name__):
        self.log = logger.Logger.get_logger(logger_name)
        self._type = type
        self._managed_by = managed_by

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def managed_by(self) -> str:
        return self._managed_by

    @abstractmethod
    def run(self, wait: bool = True) -> RunnableResult:
        ...