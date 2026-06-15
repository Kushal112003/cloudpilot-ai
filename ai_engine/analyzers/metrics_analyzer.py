class MetricsAnalyzer:

    def analyze(self, metrics):

        findings = []

        # cpu analysis

        cpu = metrics["resources"]["cpu_usage_percent"]

        if cpu > 80:

            findings.append(
                {
                    "id": "CPU_HIGH",
                    "severity": "critical",
                    "category": "cpu",
                    "issue": f"High CPU usage ({cpu}%)",
                    "affected_resource": "cluster",
                    "recommendation": "Investigate CPU intensive workloads"
                }
            )
        elif cpu > 60:

            findings.append(
                {
                    "id": "ELEVATED_CPU",
                    "severity": "warning",
                    "category": "cpu",
                    "issue": f"Elevated CPU usage ({cpu}%)",
                    "affected_resource": "cluster",
                    "recommendation": "Investigate CPU intensive workloads"

                }
            )
        
        top_cpu = metrics["resource_hotspots"]["top_cpu_pods"]
        if top_cpu:
            hotspot = top_cpu[0]
            findings.append(
                {
                    "id": "CPU_HOTSPOT",
                    "severity": "warning",
                    "category": "resources",
                    "issue": (
                        f"Pod {hotspot['pod']}"
                        f"is currently the highest CPU consumer"
                    ),
                    "affected_resource": hotspot["pod"],
                    "recommendation": "Review workload efficiency"
                }
            )
        # memory Analysis

        memory = metrics["resources"]["memory_usage_percent"]

        if memory > 85:

            findings.append(
                {
                    "id": "HIGH_MEMORY",
                    "severity": "critical",
                    "category": "memory",
                    "issue": f"High memory usage ({memory}%)",
                    "affected_resource": "cluster",
                    "recommendation": "Investigate Memory consuming workloads"
                }
            )
        elif memory > 70:

            findings.append(
                {
                    "id": "ELEVATED_MEMORY",
                    "severity": "warning",
                    "category": "memory",
                    "issue": f"Elevated memory usage ({memory}%)",
                    "affected_resource": "cluster",
                    "recommendation": "Investigate memory consuming workloads"
                }
            )
        top_memory = metrics["resource_hotspots"]["top_memory_pods"]

        if top_memory:
            hotspot = top_memory[0]
            if hotspot["memory_mb"] > 500:

                findings.append(
                    {
                        "id": "MEMORY_HOTSPOT",
                        "severity": "warning",
                        "category": "resources",
                        "issue": (
                            f"Pod{hotspot['pod']}"
                            f"is consuming {hotspot['memory_mb']} MB memory"
                        ),
                        "affected_resource": hotspot["pod"],
                        "recommendation": "Review memory usage and limits"
                    }
                )
        service_health = metrics["service_health"]
        if service_health["down"] > 0:

            findings.append(
                {
                    "id": "SERVICE_DOWN",
                    "severity": "critical",
                    "category": "availability",
                    "issue": (
                        f"{service_health['down']} services are down"
                    ),
                    "affected_resource": service_health["down_services"],
                    "recommendation": "Restore affected services immediately"
                }
            )

            # Pod Failures

        failed = metrics["pods"]["failed"]

        if failed > 0:

            findings.append(
                {
                    "id": "POD_FAILURE",
                    "severity": "critical",
                    "category": "pods",
                    "issue": f"{failed} failed pods detected",
                    "affected_resource": "cluster",
                    "recommendation": "Investigate CPU intensive workloads"
                }
            )

        # Pending Pods

        pending = metrics["pods"]["pending"]

        if pending > 0:

            findings.append(
                {
                    "id": "POD_PENDING",
                    "severity": "warning",
                    "category": "pods",
                    "issue": f"{pending} pending pods detected",
                    "affected_resource": "cluster",
                    "recommendation": "Investigate CPU intensive workloads"
                }
            )

        # Deployment Availability

        availability = metrics["deployment_health"]["availability_percent"]

        if availability < 100:

            findings.append(
                {
                    "id": "DEPLOYMENT_LOW",
                    "severity": "critical",
                    "category": "deployment",
                    "issue": (f"Deployment availability " f"is {availability}%"),
                    "affected_resource": "cluster",
                    "recommendation": "Investigate CPU intensive workloads"
                }
            )
        deployment_inventory = metrics["deployment_health"]["deployment_inventory"]
        for deployment in deployment_inventory:
            if deployment["status"] == "degraded":
                findings.append(
                    {
                        "id": "DEPLOYMENT_DEGRADED",
                        "severity": "critical",
                        "category": "deployment",
                        "issue": (
                            f"{deployment['deployment']}"
                            f"deployment is degraded"
                        ),
                        "affected_resource": deployment["deployment"],
                        "recommendation": "Check replica availability"
                    }
                )
        # Infrastructure risk 

        risk = metrics["infrastructure_risk"]
        if risk["count"] > 0:

            findings.append(
                {
                    "id": "INFRASTRUCTURE_RISK",
                    "severity": "warning",
                    "category": "infrastructure",
                    "issue": "Infrastructure risk factors detected",
                    "affected_resource": risk["factors"],
                    "recommendation": "Review node and storage health"
                }
            )
        # Restart Risk

        restart_risk = metrics["restart_analysis"]["restart_risk"]

        if restart_risk == "high":

            findings.append(
                {
                    "id": "RESTART_RISK",
                    "severity": "warning",
                    "category": "restarts",
                    "issue": ("High restart activity detected"),
                    "affected_resource": "cluster",
                    "recommendation": "Investigate CPU intensive workloads"
                }
            )
        
        #root cause candidate

        primary = metrics["primary_suspect"]

        if primary:

            findings.append(
                {
                    "id": "PRIMARY_SUSPECT",
                    "severity": "warning",
                    "category": "root_cause",
                    "issue": (
                        f"{primary['resource']} identified"
                        f"as primary suspect"
                    ),
                    "affected_resource": primary["resource"],
                    "recommendation": "Investigate this component first"
                }
            )
        
        critical_count = len(
            [
                f 
                for f in findings
                if f["severity"] == "critical"
            ]
        )
        warning_count = len(
            [
                f
                for f in findings
                if f["severity"] == "warning"
            ]
        )

        if critical_count > 0:
            overall_severity = "critical"
        elif warning_count > 0:
            overall_severity = "warning"
        else:
            overall_severity = "healthy"

        return {
    "overall_severity": overall_severity,
    "critical_findings": critical_count,
    "warning_findings": warning_count,
    "total_findings": len(findings),
    "findings": findings
}