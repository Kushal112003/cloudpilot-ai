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
        ai_status = AIServiceCheck().check()
    except Exception:
        logging.error("AI service health check failed", exc_info=True)
        ai_status = False

    try:
        grafana_status = GrafanaServiceCheck().check()
    except Exception:
        logging.error("Grafana service health check failed", exc_info=True)
        grafana_status = False

    try:
        jenkins_status = JenkinsServiceCheck().check()
    except Exception:
        logging.error("Jenkins service health check failed", exc_info=True) 
        jenkins_status = False

    try:
        kubernetes_status = KubernetesServiceCheck().check()
    except Exception:
        logging.error("Kubernetes service health check failed", exc_info=True)
        kubernetes_status = False

    try:
        loki_status = LokiServiceCheck().check()
    except Exception:
        logging.error("Loki service health check failed", exc_info=True)
        loki_status = False

    try:
        prometheus_status = PrometheusServiceCheck().check()
    except Exception:
        logging.error("Prometheus service health check failed", exc_info=True)
        prometheus_status = False

    try:
        security_status = SecurityServiceCheck().check()
    except Exception:
        logging.error("Security service health check failed", exc_info=True)
        security_status = False
    try:        
        telemetry_status = TelemetryServiceCheck().check()
    except Exception:
        logging.error("Telemetry service health check failed", exc_info=True)
        telemetry_status = False

    # Calculate overall platform health
    # If ANY service is unhealthy,
    # overall platform health becomes False
    overall_health = all([
        ai_status,
        grafana_status, 
        jenkins_status,
        kubernetes_status,
        loki_status,
        prometheus_status,
        security_status,
        telemetry_status
    ])

    # Final aggregated response
    health_response = {
        "timestamp": current_time,

        "overall_health": overall_health,
        "overall_status": ("healthy" if overall_health else "unhealthy"),

        "services": {

            "ai_service": {
                "healthy": ai_status,
                "message": (
                    "AI service is working"
                    if ai_status
                    else "AI service is down"
                )
            },

             "grafana_service": {
                "healthy": grafana_status,
                "message": (
                    "Grafana service is working"
                    if grafana_status
                    else "Grafana service is down"
                )
            },

            "jenkins_service": {
                "healthy": jenkins_status,
                "message": (
                    "Jenkins service is working"
                    if jenkins_status
                    else "Jenkins service is down"
                )
            },

            "kubernetes_service": {
                "healthy": kubernetes_status,
                "message": (
                    "Kubernetes service is working"
                    if kubernetes_status
                    else "Kubernetes service is down"
                )
            },

            "loki_service": {
                "healthy": loki_status,
                "message": (
                    "Loki service is working"
                    if loki_status
                    else "Loki service is down"
                )
            },

            "prometheus_service": {
                "healthy": prometheus_status,
                "message": (
                    "Prometheus service is working"
                    if prometheus_status
                    else "Prometheus service is down"
                )
            },

             "security_service": {
                "healthy": security_status,
                "message": (
                    "Security service is working"
                    if security_status
                    else "Security service is down"
                )
            },

            "telemetry_service": {
                "healthy": telemetry_status,
                "message": (
                    "Telemetry service is working"
                    if telemetry_status
                    else "Telemetry service is down"
                )
            }
        }
    }

    return health_response


router = APIRouter()

@router.get(
    "/health",
    tags=["Health"],
    summary="Infrastructure Health Check"
)
def get_health():
    return check_health()