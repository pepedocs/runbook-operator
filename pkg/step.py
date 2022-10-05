import json
import uuid

from pkg.exceptions import MissingStepParamError
from pkg.exceptions import PodDeletedError
from pkg.exceptions import PodStatusPhaseFailedError
from pkg.runnable import Runnable
from pkg.mixins import KubernetesMixin
from pkg.mixins import JinjaMixin
from pkg.result import RunnableResult


class Step(JinjaMixin, KubernetesMixin, Runnable):
    def __init__(self, step_spec: dict,
                 managed_by: str,
                 **kwargs: dict):
        super().__init__(managed_by, "step", "step")

        # Evaluate parameter values
        self._spec = self.apply_params_str(
            json.dumps(step_spec),
            step_spec.get("params", {})
        )

        for kw in ["namespace", "volumes"]:
            if kwargs.get(kw) is None:
                raise MissingStepParamError(
                    f"Step parameter '{kw}' is missing.")

        self._ns = kwargs["namespace"]
        self._volumes = kwargs.get("volumes")
        self._service_account_name = kwargs["service_account_name"]

    def run(self, wait: bool = True) -> RunnableResult:

        suffix = str(uuid.uuid4())[:6]
        spec_name = f"{self._managed_by}-{self._spec['name']}-step-{suffix}"

        self.log.info(f"Running step: {spec_name}")

        runnable_result = RunnableResult(name=spec_name)

        try:
            self.create_namespaced_pod(
                self._spec["image"],
                spec_name,
                self._spec["command"],
                self._spec.get("args", []),
                self._service_account_name,
                self._ns,
                self._spec.get("volumeMounts", []),
                self._volumes,
                wait=wait,
                timeout_seconds=60
            )
            runnable_result.status = True
        except (PodStatusPhaseFailedError, PodDeletedError) as e:
            runnable_result.status = False
            runnable_result.error = e.msg

        return runnable_result







