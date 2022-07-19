class Result:
    def __init__(self):
        self._status: bool = False
        self._error: str = None

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def error(self) -> str:
        return self._Error

    @status.setter
    def error(self, value: str):
        self._error = value


class StrategyResult(Result):
    def __init__(self):
        super().__init__()
        self._resolved_status: bool = None

    @property
    def resolved_status(self):
        return self._resolved_status

    @resolved_status.setter
    def resolved_status(self, value: bool):
        self._resolved_status = value


class RunnableResult(Result):
    def __init__(self):
        super().__init__()