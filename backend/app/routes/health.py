"""
====================================================================
CloudPilot AI - Health Route

FILE:
    backend/app/routes/health.py

PURPOSE:
    This route acts as the central infrastructure health endpoint.

WHY IT EXISTS:
    Instead of the dashboard calling every infrastructure service
    individually, the dashboard calls only:

        GET /health

    This route then:
        1. Calls all infrastructure health services
        2. Aggregates results
        3. Calculates overall platform health
        4. Returns a unified JSON response

CURRENT SERVICES MONITORED:
    - AI Engine
    - Jenkins
    - Loki
    - Prometheus
    - Telemetry Service

FUTURE SERVICES:
    - Kubernetes
    - Grafana
    - Security Scanner
    - Cost Optimization Engine

ARCHITECTURE FLOW:

    Dashboard
        ↓
    GET /health
        ↓
    health.py
        ↓
    AI Service
    Jenkins Service
    Loki Service
    Prometheus Service
    Telemetry Service
        ↓
    Aggregation Logic
        ↓
    Unified Health Response

EXAMPLE RESPONSE:

{
    "timestamp": "2026-06-01 10:15:30",
    "overall_health": true,
    "services": {
        "ai_service": {
            "healthy": true,
            "message": "AI service is working"
        }
    }
}

====================================================================
"""

import time
import logging 
from fastapi import APIRouter
from app.services.ai_service import AIServiceCheck
from app.services.grafana_service import GrafanaServiceCheck
from app.services.jenkins_service import JenkinsServiceCheck
from app.services.kubernetes_service import KubernetesServiceCheck
from app.services.loki_service import LokiServiceCheck
from app.services.prometheus_service import PrometheusServiceCheck
from app.services.security_service import SecurityServiceCheck
from app.services.telemetry_service import TelemetryServiceCheck 
from app.utils.logger import logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_health():
    """
    Execute all infrastructure health checks.

    Returns:
        dict: Unified health response containing:
              - timestamp
              - overall platform health
              - individual service health
    """

    # Generate fresh timestamp for every request
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # Execute individual service health checks
    try:
        ai_result = AIServiceCheck().check()
    except Exception:
        logging.error("AI service health check failed", exc_info=True)
        ai_status = False

    try:
        grafana_result = GrafanaServiceCheck().check()
    except Exception:
        logging.error("Grafana service health check failed", exc_info=True)
        grafana_status = False

    try:
        jenkins_result = JenkinsServiceCheck().check()
    except Exception:
        logging.error("Jenkins service health check failed", exc_info=True) 
        jenkins_status = False

    try:
        kubernetes_result = KubernetesServiceCheck().check()
    except Exception:
        logging.error("Kubernetes service health check failed", exc_info=True)
        kubernetes_status = False

    try:
        loki_result = LokiServiceCheck().check()
    except Exception:
        logging.error("Loki service health check failed", exc_info=True)
        loki_result = False

    try:
        prometheus_result = PrometheusServiceCheck().check()
    except Exception:
        logging.error("Prometheus service health check failed", exc_info=True)
        prometheus_result = False

    try:
        security_result = SecurityServiceCheck().check()
    except Exception:
        logging.error("Security service health check failed", exc_info=True)
        security_status = False
    try:        
        telemetry_result = TelemetryServiceCheck().check()
    except Exception:
        logging.error("Telemetry service health check failed", exc_info=True)
        telemetry_status = False

    # Calculate overall platform health
    # If ANY service is unhealthy,
    # overall platform health becomes False
    overall_health = all([
        ai_result["healthy"],
        grafana_result["healthy"], 
        jenkins_result["healthy"],
        kubernetes_result["healthy"],
        loki_result["healthy"],
        prometheus_result["healthy"],
        security_result["healthy"],
        telemetry_result["healthy"]
    ])

    # Final aggregated response
    health_response = {
        "timestamp": current_time,

        "overall_health": overall_health,
        "overall_status": ("healthy" if overall_health else "unhealthy"),

        "services": {

            "ai_service": ai_result,

             "grafana_service": grafana_result,

            "jenkins_service": jenkins_result,

            "kubernetes_service": kubernetes_result,

            "loki_service": loki_result,

            "prometheus_service": prometheus_result,

            "security_service": security_result,

            "telemetry_service": telemetry_result

        
    }
}
    logger.info(
        f"Health Check Executed | overall_health={overall_health}"
    )

    return health_response


router = APIRouter()

@router.get(
    "/health",
    tags=["Health"],
    summary="Infrastructure Health Check"
)
def get_health():
    return check_health()