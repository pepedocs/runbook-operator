create-kind:
	kind create cluster --name $(name) && \
	kubectl cluster-info --context kind-$(name)

destroy-kind:
	kind delete cluster --name $(name)

install-tests:
	kubectl create namespace ro-tests > /dev/null 2>&1 || true && \
	kubectl apply -f crds/runbook.yaml -n ro-tests && \
	kubectl apply -f tests/kind/mysql/logs-pvc.yml -n ro-tests && \
	kubectl apply -f tests/kind/mysql/mysql-pod.yaml -n ro-tests && \
	kubectl apply -f tests/kind/mysql/mysql-pod-missing-secret.yaml -n ro-tests && \
	kubectl apply -f tests/kind/runbooks/rbac.yaml -n ro-tests

run:
	PYTHONPATH=./ kopf run main.py
