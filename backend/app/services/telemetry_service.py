class TelemetryServiceCheck:

    def check(self):
#dummy not implementing real stats
        return{
            "healthy": True,
            "response_time_ms": 0,
            "message": "Telemetry service working",
            "details": {}

        }