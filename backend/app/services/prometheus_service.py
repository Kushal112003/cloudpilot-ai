import time
import requests
from datetime import datetime


class PrometheusServiceCheck:

    def check(self):

        start = time.time()

        try:

            response = requests.get(
                "http://monitoring-kube-prometheus-prometheus.observability.svc.cluster.local:9090/api/v1/query",
                params={"query": "up"},
                timeout=5,
            )

            latency = round((time.time() - start) * 1000, 2)

            data = response.json()

            targets = len(data["data"]["result"])

            return {
                "healthy": response.status_code == 200,
                "response_time_ms": latency,
                "message": "Prometheus reachable",
                "details": {"targets_up": targets},
            }
        except Exception as e:

            latency = round((time.time() - start) * 1000, 2)

            return {
                "healthy": False,
                "response_time_ms": latency,
                "message": str(e),
                "details": {},
            }


class PrometheusMetricsService:

    PROMETHEUS_URL = (
        "http://monitoring-kube-prometheus-prometheus."
        "observability.svc.cluster.local:9090"
    )

    def query(self, promql):

        response = requests.get(
            f"{self.PROMETHEUS_URL}/api/v1/query", params={"query": promql}, timeout=10
        )

        response.raise_for_status()

        return response.json()

    def get_metrics(self):

        try:

            up_data = self.query("up")

            node_data = self.query(
                'kube_node_status_condition{condition="Ready",status="true"}'
            )

            pod_data = self.query('kube_pod_status_phase{phase="Running"}')

            memory_total = self.query("node_memory_MemTotal_bytes")
            memory_available = self.query("node_memory_MemAvailable_bytes")
            restart_data = self.query("kube_pod_container_status_restarts_total")
            deployment_data = self.query("kube_deployment_status_replicas")
            daemonset_data = self.query("kube_daemonset_status_number_ready")
            job_data = self.query("kube_job_status_active")
            termination_data = self.query(
                "kube_pod_container_status_last_terminated_reason"
            )

            # Termination analysis logic !
            termination_analysis = []

            for item in termination_data["data"]["result"]:

                reason = item["metric"].get("reason", "unknown")

                if float(item["value"][1]) == 1:

                    termination_analysis.append(
                        {"pod": item["metric"].get("pod", "unknown"), "reason": reason}
                    )

            service_status = []
            seen_jobs = set()

            for item in up_data["data"]["result"]:
                job_name = item["metric"].get("job", "unknown")

                if job_name not in seen_jobs:

                    seen_jobs.add(job_name)

                    service_status.append(
                        {
                            "job": job_name,
                            "status": "up" if float(item["value"][1]) == 1 else "down",
                        }
                    )
            down_services = [
                s for s in service_status
                if s["status"] == "down"
            ]
            cpu_data = self.query(
                '100-(avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))*100)'
            )
            top_cpu_data = self.query(
                "topk(5,sum(rate(container_cpu_usage_seconds_total[5m])) by (pod))"
            )

            top_cpu_pods = []

            for item in top_cpu_data["data"]["result"]:
                pod_name = item["metric"].get("pod", "unknown")
                cpu_usage = round(float(item["value"][1]), 4)
                top_cpu_pods.append({"pod": pod_name, "cpu": cpu_usage})

            namespace_data = self.query(
                'count by(namespace)(kube_pod_status_phase{phase="Running"})'
            )
            namespace_health = []
            for item in namespace_data["data"]["result"]:
                namespace_health.append(
                    {
                        "namespace": item["metric"].get("namespace", "unknown"),
                        "running_pods": int(float(item["value"][1])),
                    }
                )
            failed_data = self.query('kube_pod_status_phase{phase="Failed"}')
            failed_pod_names = []

            for item in failed_data["data"]["result"]:
                if float(item["value"][1]) == 1:
                    failed_pod_names.append(item["metric"].get("pod", "unknown"))

            deployment_available_data = self.query(
                "kube_deployment_status_replicas_available"
            )
            desired_deployments = len(deployment_data["data"]["result"])
            pending_data = self.query('kube_pod_status_phase{phase="Pending"}')

            # deployment issus
            available_lookup = {}
            for item in deployment_available_data["data"]["result"]:

                deployment_name = item["metric"].get(
                    "deployment",
                    "unknown"
                )
                available_lookup[deployment_name] = int(
                    float(item["value"][1])
                )
            deployment_inventory = []

            for item in deployment_data["data"]["result"]:

                deployment_name = item["metric"].get("deployment", "unknown")
                desired = int(float(item["value"][1]))

                available = available_lookup.get(
                    deployment_name,
                    0 
                )
                status = (
                    "healthy"
                    if available >= desired
                    else "degraded"
                )
                deployment_inventory.append(
                    {"deployment": deployment_name, 
                     "desired": desired,
                     "available": available,
                     "status": status
                     }
                )

            # calculating CPU usage

            cpu_usage_percent = (
                round(float(cpu_data["data"]["result"][0]["value"][1]), 2)
                if cpu_data["data"]["result"]
                else 0
            )

            # calculating failed pods

            failed_pods = sum(
                int(float(item["value"][1])) for item in failed_data["data"]["result"]
            )

            # calculating deployment availability

            available_deployments = len(deployment_available_data["data"]["result"])
            # calculating memory usage

            total_memory = float(memory_total["data"]["result"][0]["value"][1])

            available_memory = float(memory_available["data"]["result"][0]["value"][1])

            memory_usage_percent = round(
                ((total_memory - available_memory) / total_memory) * 100, 2
            )

            top_memory_data = self.query(
                "topk(5,sum(container_memory_working_set_bytes) by (pod))"
            )

            top_memory_pods = []

            for item in top_memory_data["data"]["result"]:

                pod_name = item["metric"].get("pod", "unknown")
                memory_mb = round(float(item["value"][1]) / (1024 * 1024), 2)
                top_memory_pods.append({"pod": pod_name, "memory_mb": memory_mb})

            # calculating availability percentage

            availability_percent = (
                round((available_deployments / desired_deployments) * 100, 2)
                if desired_deployments > 0
                else 0
            )

            # calculating pod restarts

            total_restarts = sum(
                float(item["value"][1]) for item in restart_data["data"]["result"]
            )

            pending_pods = sum(
                int(float(item["value"][1])) for item in pending_data["data"]["result"]
            )

            pending_pod_names = []

            for item in pending_data["data"]["result"]:

                if float(item["value"][1]) == 1:

                    pending_pod_names.append(item["metric"].get("pod", "unknown"))

            restarting_pods = []

            for item in restart_data["data"]["result"]:

                restart_count = int(float(item["value"][1]))
                pod_name = item["metric"].get("pod", "unknown")
                if restart_count > 0:
                    restarting_pods.append({"pod": pod_name, "restarts": restart_count})

            top_restarting_pods = sorted(
                restarting_pods, key=lambda x: x["restarts"], reverse=True
            )[:5]

            highest_restart = (
                top_restarting_pods[0]["restarts"] if top_restarting_pods else 0
            )

            score = 100

            if failed_pods > 0:
                score -= 20

            if availability_percent < 100:
                score -= 20

            if memory_usage_percent > 80:
                score -= 10

            if cpu_usage_percent > 80:
                score -= 10

            if total_restarts > 20:
                score -= 10

            score = max(score, 0)

            cluster_status = (
                "healthy" if score >= 80 else "warning" if score >= 50 else "critical"
            )

            # Node Load
            node_load_data = self.query("node_load1")

            node_load = (
                round(float(node_load_data["data"]["result"][0]["value"][1]), 2)
                if node_load_data["data"]["result"]
                else 0
            )

            # disk health

            disk_data = self.query('node_filesystem_avail_bytes{mountpoint="/"}')

            root_disk_free_gb = 0

            if disk_data["data"]["result"]:

                root_disk_free_gb = round(
                    float(disk_data["data"]["result"][0]["value"][1]) / (1024**3), 2
                )
            disk_risk = (
                "critical"
                if root_disk_free_gb < 2
                else "warning" if root_disk_free_gb < 5 else "healthy"
            )

            root_cause_candidates = []

            if top_cpu_pods:
                root_cause_candidates.append(
                    {
                        "type": "cpu",
                        "resource": top_cpu_pods[0]["pod"],
                        "value": top_cpu_pods[0]["cpu"],
                    }
                )
            if top_memory_pods:

                root_cause_candidates.append(
                    {
                        "type": "memory",
                        "resource": top_memory_pods[0]["pod"],
                        "value": top_memory_pods[0]["memory_mb"],
                    }
                )
            if top_restarting_pods:

                root_cause_candidates.append(
                    {
                        "type": "restart",
                        "resource": top_restarting_pods[0]["pod"],
                        "value": top_restarting_pods[0]["restarts"],
                    }
                )
            root_cause_candidates.sort(key=lambda x: x["value"], reverse=True)

            # Resource Alert
            resource_alerts = []

            if cpu_usage_percent > 80:

                resource_alerts.append(
                    {
                        "severity": "critical",
                        "resource": "cpu",
                        "message": f"CPU usage is {cpu_usage_percent} %",
                    }
                )
            elif cpu_usage_percent > 60:

                resource_alerts.append(
                    {
                        "severity": "warning",
                        "resource": "cpu",
                        "message": f"CPU usage is {cpu_usage_percent} %",
                    }
                )
            if memory_usage_percent > 85:

                resource_alerts.append(
                    {
                        "severity": "critical",
                        "resource": "memory",
                        "message": f"Memory usage is {memory_usage_percent} %",
                    }
                )
            if failed_pods > 0:

                resource_alerts.append(
                    {
                        "severity": "critical",
                        "resource": "pods",
                        "message": f"{failed_pods} failed pods detected",
                    }
                )
            if availability_percent < 100:

                resource_alerts.append(
                    {
                        "severity": "critical",
                        "resource": "deployment",
                        "message": f"Deployment availability is {availability_percent}%",
                    }
                )
            
            incident_summary = []
            if failed_pods > 0:
                incident_summary.append(
                    f"{failed_pods} failed pods"
                )
            if pending_pods > 0:
                incident_summary.append(
                    f"{pending_pods} pending pods"
                )
            if availability_percent < 100:
                incident_summary.append(
                    "deployment degradation"
                )
            if total_restarts > 20:
                incident_summary.append(
                    "high restart activity"
                )

            primary_suspect = (
                root_cause_candidates[0]
                if root_cause_candidates
                else None
            )

            # Infrastuture Risk 

            risk_factors = []
            if cpu_usage_percent > 80:
                risk_factors.append("cpu")
            if memory_usage_percent > 80:
                risk_factors.append("memory")
            if disk_risk != "healthy":
                risk_factors.append("disk")
            if failed_pods > 0:
                risk_factors.append("pods")
            if availability_percent < 100:
                risk_factors.append("deployment")


            return {
                "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "cluster_status": cluster_status,
                "cluster": {
                    "nodes_total": len(node_data["data"]["result"]),
                    "nodes_ready": len(node_data["data"]["result"]),
                },
                "root_cause_candidates": root_cause_candidates,
                "service_health": {
                "total" : len(service_status),
                "down" : len(down_services),
                "down_services": down_services
                },
                "namespace_health": namespace_health,
                "termination_analysis": termination_analysis,
                "node_pressure": {"load_average": node_load},
                "pods": {
                    "running": len(pod_data["data"]["result"]),
                    "failed": failed_pods,
                    "failed_pod_names": failed_pod_names,
                    "pending": pending_pods,
                    "pending_pod_names": pending_pod_names,
                    "restarts": int(total_restarts),
                },
                "resources": {
                    "cpu_usage_percent": cpu_usage_percent,
                    "memory_usage_percent": memory_usage_percent,
                },
                "storage": {
                    "root_disk_free_gb": root_disk_free_gb,
                    "disk_risk": disk_risk,
                },
                "resource_hotspots": {
                    "top_cpu_pods": top_cpu_pods,
                    "top_memory_pods": top_memory_pods,
                },
                "workloads": {
                    "deployments": len(deployment_data["data"]["result"]),
                    "daemonsets": len(daemonset_data["data"]["result"]),
                    "jobs": len(job_data["data"]["result"]),
                },
                "restart_analysis": {
                    "total_restarts": int(total_restarts),
                    "top_restarting_pods": top_restarting_pods,
                    "restart_risk": (
                        "high"
                        if total_restarts > 50 and highest_restart > 20
                        else (
                            "medium"
                            if total_restarts > 20 and highest_restart > 5
                            else "low"
                        )
                    ),
                },
                "deployment_health": {
                    "available": available_deployments,
                    "desired": desired_deployments,
                    "availability_percent": availability_percent,
                    "deployment_inventory": deployment_inventory,
                },
                "primary_suspect": primary_suspect,
                "resource_alerts": resource_alerts,
                "health_score": score,
                "infrastructure_risk": {
                    "count": len(risk_factors),
                    "factors": risk_factors
                },

                "prometheus": {"targets_up": len(up_data["data"]["result"])},
                "incident_summary": incident_summary
            }
        except Exception as e:

            return {"cluster_status": "error", "error": str(e)}
