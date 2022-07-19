from __future__ import annotations
from abc import ABCMeta, abstractmethod

import pkg.logger as logger


class RunbookHandler(metaclass=ABCMeta):
    _instance: RunbookHandler = None

    def __init__(self, logger_name: str = __name__):
        self.log = logger.Logger.get_logger(logger_name)

    @classmethod
    def kopfhandler(cls) -> RunbookHandler:
        if cls._instance is None:
            cls._instance = cls.get_instance()
        return cls._instance

    @classmethod
    @abstractmethod
    def get_instance(cls) -> RunbookHandler:
        ...

    @abstractmethod
    def create(cls):
        ...
