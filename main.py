import logging

import kopf

from pkg.logger import Logger
from pkg.runbook_controller import RunbookController


log = Logger("debug").get_logger("main")

def ctl():
    return RunbookController.kopfhandler()


@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    settings.posting.level = logging.INFO

    log.info("Starting operator.")


@kopf.on.create("runbook")
def on_create(spec: dict,
              name: str,
              namespace: str ,
              **kwargs: dict):
    ctl().create(spec, name, namespace, **kwargs)
