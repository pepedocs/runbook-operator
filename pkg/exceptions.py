
class MissingStepParamError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class RunnableError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class PodStatusPhaseFailedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class PodDeletedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)