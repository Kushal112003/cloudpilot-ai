from metrics_analyzer import MetricsAnalyzer

sample = {
    "resources": {
        "cpu_usage_percent": 92,
        "memory_usage_percent": 87
    },
    "pods": {
        "failed": 2,
        "pending": 1
    },
    "deployment_health": {
        "availability_percent": 75
    },
    "restart_analysis": {
        "restart_risk": "high"
    }
}

result = MetricsAnalyzer().analyze(sample)

print(result)