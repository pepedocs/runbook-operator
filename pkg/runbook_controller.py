from pkg.exceptions import RunnableError
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
                volumes=runbook_spec["volumes"],
                service_account_name=runbook_spec["serviceAccountName"]
            )
            step = Step(step_spec,
                        name,
                        **kwargs)
            runnables.append(step)

        strategy = DefaultRunbookStrategy(runnables)

        self.log.info((f"Running runbook strategy with "
                       f"{len(runnables)} runnables. "))

        try:
            result = strategy.run()
            patch = dict(
                reason="RunbookCompleted",
                status=result.resolved_status
            )
        except RunnableError as e:
            patch = dict(
                reason="StepCompleted",
                error=e.msg,
                status=False
            )

        self.patch_runbook_status(
            name,
            namespace,
            patch
        )

