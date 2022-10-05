
class MissingStepParamError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class RunnableError(Exception):
    def __init__(self, runnable_result, msg: str):
        super().__init__(msg)
        self._runnable_result = runnable_result
        self._msg = msg

    @property
    def runnable_result(self):
        return self._runnable_result

    @property
    def msg(self):
        return self._msg


class PodStatusPhaseFailedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class PodDeletedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class MissingRunbookStep(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)