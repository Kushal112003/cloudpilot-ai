import time
import re
import requests
from datetime import datetime


class LokiServiceCheck:

    def check(self):

        start = time.time()

        try:
            response = requests.get(
                "http://loki.observability.svc.cluster.local:3100/ready", timeout=5
            )

            latency = round((time.time() - start) * 1000, 2)

            return {
                "healthy": response.status_code == 200,
                "response_time_ms": latency,
                "message": "Loki is ready",
                "details": {"status_code": response.status_code},
            }

        except Exception as e:

            latency = round((time.time() - start) * 1000, 2)

            return {
                "healthy": False,
                "response_time_ms": latency,
                "message": str(e),
                "details": {},
            }


class LokiLogService:

    LOKI_URL = "http://loki.observability.svc.cluster.local:3100"

    def get_logs(self, namespace: str = "cloudpilot", limit: int = 50, search: str | None = None):

        try:

            query = f'{{namespace="{namespace}"}}'

            if search:
                query += f' |= "{search}"'

            response = requests.get(
                f"{self.LOKI_URL}/loki/api/v1/query_range",
                params={"query": query, "limit": limit, "direction": "backward"},
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            logs = []

            error_count = 0
            warning_count = 0
            info_count = 0

            for stream in data["data"]["result"]:

                for value in stream["values"]:
                    timestamp_ns = int(value[0])
                    log_message = value[1]
                    log_upper = log_message.upper()

                    if re.match(r"^ERROR", log_upper):
                        error_count += 1

                    elif re.match(r"^WARNING", log_upper):
                        warning_count += 1

                    elif re.match(r"^INFO", log_upper):
                        info_count += 1

                    timestamp = datetime.utcfromtimestamp(
                        timestamp_ns / 1_000_000_000
                    ).strftime("%Y-%m-%d %H:%M:%S")

                    logs.append({"timestamp": timestamp, "log": log_message})

            return {"namespace": namespace, 
                    "count": len(logs), 
                    "summary": {
                        "errors": error_count,
                        "warnings": warning_count,
                        "info": info_count
                        },
                    
                    "logs": logs
                    }

        except Exception as e:

            return {"namespace": namespace,
                    "count": 0,
                    "summary": {
                        "errors": 0,
                        "warnings": 0,
                        "info": 0
                    },
                    "logs": [], 
                    "error": str(e)}
