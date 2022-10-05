import unittest
import time
import signal

from tests.test_util import TestUtilMixin


class TestRunbookOperator(TestUtilMixin, unittest.TestCase):

    def __init__(self, *args, **kwargs):
        kwargs["log_level"] = "debug"
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        delete_these = [
            "gather-mysql-pod-logs",
        ]
        for item in delete_these:
            self.run_pipe(["kubectl",
                            "delete",
                            "runbook",
                            item,
                            "-n",
                            "ro-tests"],
                            check=False)

        self.kopf_proc = self.run_script_non_blocking(["kopf",
                                                       "run",
                                                       "main.py"])
        time.sleep(3)

    def tearDown(self) -> None:
        self.kopf_proc.send_signal(signal.SIGINT)
        rc = self.kopf_proc.wait()
        self.assertEqual(rc, 0)


    def test_runbook_gather_mysql_pod_logs(self):
        self.run_pipe(["kubectl",
                       "apply",
                       "-f",
                       "tests/kind/runbooks/gather-mysql-pod-logs.yaml",
                       "-n",
                       "ro-tests"
                       ])




if __name__ == "__main__":
    unittest.main()
