import kubernetes
import json

from datetime import datetime as dt

from jinja2 import Template

from pkg.exceptions import PodStatusPhaseFailedError
from pkg.exceptions import PodDeletedError


class Mixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class JinjaMixin(Mixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def apply_params_str(self, source: str, params: dict) -> dict:
        result = Template(source).render(params)
        return json.loads(result)


class KubernetesMixin(Mixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cli = kubernetes.client
        self._core_v1_api = self._cli.CoreV1Api()
        self._watch = kubernetes.watch.Watch()
        self._custom_objects_api = self._cli.CustomObjectsApi()

    def create_namespaced_pod(self,
                              image: str,
                              name: str,
                              command: str,
                              command_args: list,
                              service_account_name: str,
                              namespace: str,
                              volume_mounts: list = None,
                              volumes: list = None,
                              wait=True,
                              timeout_seconds=60):

        pod = self._cli.V1Pod(
            metadata=self._cli.V1ObjectMeta(name=name))

        volume_mounts = volume_mounts or []
        vms = []
        if volume_mounts is not None:
            for vm in volume_mounts:
               _vm = self._cli.V1VolumeMount(
                   name=vm["name"],
                   mount_path=vm["mountPath"]
               )
               vms.append(_vm)
        container = self._cli.V1Container(
            name=name,
            image=image,
            command=command,
            args=command_args,
            volume_mounts=vms
        )

        vols = []
        if volumes is not None:
            for vol in volumes:
                pvc = self._cli.V1PersistentVolumeClaimVolumeSource(
                    claim_name=vol["persistentVolumeClaim"]["claimName"]
                )
                volume = self._cli.V1Volume(
                    name=vol["name"],
                    persistent_volume_claim=pvc
                )
                vols.append(volume)

        pod.spec = self._cli.V1PodSpec(
            containers=[container],
            volumes=vols,
            service_account_name=service_account_name,
            restart_policy="Never"
        )
        pod.metadata = self._cli.V1ObjectMeta(
            name=name,
            labels={
                "name": name,
            },
        )

        resp = self._core_v1_api.create_namespaced_pod(
                namespace,
                pod
            )

        if not wait:
            return resp

        self.log.debug(f"Waiting for events: {wait}")

        for event in self._watch.stream(func=self._core_v1_api.list_namespaced_pod,
                                        namespace=namespace,
                                        label_selector=f"name={name}",
                                        timeout_seconds=timeout_seconds):

            self.log.debug(f"Got event from watch: {event}")

            if event["object"].status.phase == "Failed":
                raise PodStatusPhaseFailedError(f"Pod failed: {name}")

            elif event["object"].status.phase == "Succeeded":
                break

            elif event["type"] == "DELETED":
                raise PodDeletedError(f"Pod was already deleted: {name}")

    def patch_runbook_status(self,
                             name: str,
                             namespace: str,
                             patch: dict):

        date_str = dt.utcnow().isoformat()
        patch.update({"lastTransitionTime": date_str})
        status = {"status": patch}

        return self._custom_objects_api.patch_namespaced_custom_object(
            "runbook.beastduck.com",
            "v1",
            namespace,
            "runbooks",
            name,
            status
        )

