class LokiServiceCheck:
    def check(self) -> bool:
        try:
            return True  # Simulate a successful health check
                    # Future requests call
        except Exception:
            return False