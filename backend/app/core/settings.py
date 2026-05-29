"""
CloudPilot AI - Central Platform Configuration

Stores platform-level configuration only.

User-managed credentials are stored separately
through the Configuration Dashboard.
"""


class Settings:

    # ==================================================
    # Application
    # ==================================================
    APP_NAME = "CloudPilot AI"
    APP_VERSION = "1.0.0"
    ENVIRONMENT = "development"

    BACKEND_HOST = "0.0.0.0"
    BACKEND_PORT = 8000

    # ==================================================
    # Dashboard
    # ==================================================
    DASHBOARD_HOST = "0.0.0.0"
    DASHBOARD_PORT = 8501

    # ==================================================
    # API
    # ==================================================
    API_PREFIX = "/api/v1"

    # ==================================================
    # Monitoring Stack
    # ==================================================
    PROMETHEUS_URL = "http://localhost:9090"
    PROMETHEUS_HEALTH_ENDPOINT = "/-/healthy"

    LOKI_URL = "http://localhost:3100"
    LOKI_HEALTH_ENDPOINT = "/ready"

    GRAFANA_URL = "http://localhost:3000"
    GRAFANA_HEALTH_ENDPOINT = "/api/health"

    # ==================================================
    # CI/CD
    # ==================================================
    JENKINS_URL = "http://localhost:8080"
    JENKINS_TIMEOUT = 5

    # ==================================================
    # Kubernetes
    # ==================================================
    KUBERNETES_API_URL = "http://localhost:8001"

    # ==================================================
    # AI Engine
    # ==================================================
    AI_ENGINE_URL = "http://localhost:8002"

    # ==================================================
    # Security
    # ==================================================
    TRIVY_REPORT_PATH = "security/reports"
    SECURITY_SCAN_TIMEOUT = 30

    # ==================================================
    # Health Checks
    # ==================================================
    HEALTH_CHECK_TIMEOUT = 5

    # ==================================================
    # Logging
    # ==================================================
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    # ==================================================
    # User Configuration Storage
    # ==================================================
    USER_CONFIG_FILE = "config/user_config.json"


settings = Settings()