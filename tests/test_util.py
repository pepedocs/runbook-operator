import subprocess as sp
import os
import logging


class Mixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TestUtilMixin(Mixin):
    def __init__(self, *args, log_level="debug", **kwargs):

        log_level = kwargs.get("log_level", "debug")
        if log_level == "debug":
            logging.basicConfig(level=logging.DEBUG)
        elif log_level == "info":
            logging.basicConfig(level=logging.INFO)
        elif log_level == "warning":
            logging.basicConfig(level=logging.WARNING)
        elif log_level == "error":
            logging.basicConfig(level=logging.ERROR)
        else:
            logging.basicConfig(level=logging.DEBUG)

        self.logger = logging.getLogger("tests")

        super().__init__(*args, **kwargs)

    def run_pipe(self, cmd, check=True, input=None, cwd=None):
        self.logger.debug(f"Running command: {cmd}")

        if input is not None:
            res = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, check=check, input=input)
        else:
            res = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, check=check)

        stdout = res.stdout.decode('utf-8')
        stderr = res.stderr.decode('utf-8')
        return res.returncode, stdout, stderr

    def run_script_non_blocking(self, script_cmd, check=True, env=None):
        self.logger.debug(f"Running command: {script_cmd}")

        all_env = os.environ.copy()

        if env is not None:
            all_env.update(env)

        return sp.Popen(script_cmd, start_new_session=True, env=all_env)

    def run_shell(self, cmd, check=True, cwd=None):
        self.logger.debug(f"Running command: {cmd}")

        res = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, check=check, shell=True)
        stdout = res.stdout.decode('utf-8')
        stderr = res.stderr.decode('utf-8')
        return res.returncode, stdout, stderr

