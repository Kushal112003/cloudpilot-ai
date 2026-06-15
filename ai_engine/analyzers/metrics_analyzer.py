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
                }
            )
        elif cpu > 60:

            findings.append(
                {
                    "id": "ELEVATED_CPU",
                    "severity": "warning",
                    "category": "cpu",
                    "issue": f"Elevated CPU usage ({cpu}%)",
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
                }
            )
        elif memory > 70:

            findings.append(
                {
                    "id": "ELEVATED_MEMORY",
                    "severity": "warning",
                    "category": "memory",
                    "issue": f"Elevated memory usage ({memory}%)",
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
                }
            )

        return {"total_findings": len(findings), "findings": findings}
