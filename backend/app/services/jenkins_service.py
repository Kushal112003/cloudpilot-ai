import time 
import requests

class JenkinsServiceCheck:

    def check(self):

        start = time.time()

        try:

            response = requests.get(
                "http://172.31.21.212:8080/login",
                timeout=5
            )

            latency = round(
                (time.time() - start) * 1000,
                2
            )

            return {
                "healthy": response.status_code == 200,
                "response_time_ms": latency,
                "message": "Jenkins reachable",
                "details": {
                    "status_code": response.status_code,
                    "version": response.headers.get(
                        "X-Jenkins",
                        "unknown"
                    )
                }
            }
        except Exception as e:

            return {
                "healthy": False,
                "response_time_ms": 0,
                "message": str(e),
                "details": {}
            }

