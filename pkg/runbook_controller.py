from datetime import datetime as dt

from pkg.runbook_handler import RunbookHandler
from pkg.mixins import KubernetesMixin
from pkg.runbook_strategy import DefaultRunbookStrategy
from pkg.step import Step


class RunbookController(KubernetesMixin, RunbookHandler):
    def __init__(self):
        super().__init__("runbook-controller")

    @classmethod
    def get_instance(cls) -> RunbookHandler:
        return RunbookController()

    def create(self,
               runbook_spec: dict,
               name: str,
               namespace: str,
               **kwargs: dict):
        runnables = []

        for step_spec in runbook_spec["steps"]:
            kwargs = dict(
                namespace=namespace,
                volumes=runbook_spec["volumes"]
            )
            step = Step(step_spec,
                        name,
                        **kwargs)
            runnables.append(step)

        strategy = DefaultRunbookStrategy(runnables)

        self.log.info((f"Running runbook strategy with "
                       f"{len(runnables)} runnables. "))

        result = strategy.run()

        status = "Succeeded" if result.resolved_status else "Failed"
        patch = {
            "status": {
                "status": status,
            },
        }

        self.log.info(f"Patching runbooks status: {status}")

        self.patch_namespaced_custom_object(
            "runbook.beastduck.com",
            "v1",
            "runbooks",
            name,
            namespace,
            patch
        )

