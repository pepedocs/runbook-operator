from __future__ import annotations

import pkg.logger as logger

from abc import ABCMeta, abstractmethod

from pkg.result import StrategyResult
from pkg.exceptions import RunnableError


class RunbookStrategy(metaclass=ABCMeta):
    def __init__(self, runnables, logger_name=__name__):
        self.log = logger.Logger.get_logger(logger_name)
        self._runnables = runnables

    @abstractmethod
    def run(self) -> StrategyResult:
        ...


class DefaultRunbookStrategy(RunbookStrategy):
    """A runbook strategy for running runbook steps serially."""

    def __init__(self, runnables):
        super().__init__(runnables, "default-runbook-strategy")

    def run(self) -> StrategyResult:
        result = StrategyResult()

        for runnable in self._runnables:
            runnable_result = runnable.run(wait=True)

            if not runnable_result.status:
                raise RunnableError(result.error)

        result.resolved_status = runnable_result.status
        return result