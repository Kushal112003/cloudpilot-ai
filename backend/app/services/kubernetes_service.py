import time

from kubernetes import client
from kubernetes import config


class KubernetesServiceCheck:

    def check(self):

        start = time.time()

        try:

            config.load_incluster_config()

            v1 = client.CoreV1Api()

            nodes = v1.list_node().items
            pods = v1.list_pod_for_all_namespaces().items

            ready_nodes = 0

            for node in nodes:

                for condition in node.status.conditions:

                    if (
                        condition.type == "Ready"
                        and condition.status == "True"
                    ):
                        ready_nodes += 1

            latency = round(
                (time.time() - start) * 1000,
                2
            )

            return {
                "healthy": ready_nodes > 0,
                "response_time_ms": latency,
                "message": "Kubernetes API reachable",
                "details": {
                    "nodes_total": len(nodes),
                    "nodes_ready": ready_nodes,
                    "pods_total": len(pods)
                }
            }

        except Exception as e:

            return {
                "healthy": False,
                "response_time_ms": 0,
                "message": str(e),
                "details": {}
            }