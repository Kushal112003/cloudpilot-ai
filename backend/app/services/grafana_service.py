import requests
import time

class GrafanaServiceCheck:
    
    def check(self):

        start = time.time()

        try:

            response = requests.get(
                "http://monitoring-grafana.observability.svc.cluster.local",
                timeout=5
            )

            latency = round(
                (time.time() - start) * 1000,
                2
            )

            return {
                "healthy": response.status_code == 200,
                "response_time_ms": latency,
                "message": "Grafana reachable",
                "details": {
                    "status_code": response.status_code
                }
            }
        except Exception as e:

            return {
                "healthy": False,
                "response_time_ms": 0,
                "message": str(e),
                "details": {}
            }