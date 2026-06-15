from fastapi import APIRouter

from app.services.prometheus_service import (
    PrometheusMetricsService
)
router = APIRouter()

@router.get(
    "/metrics",
    tags=["Metrics"],
    summary="Cluster Metrics"

)

def get_metrics():

    return (
        PrometheusMetricsService().get_metrics()
    )

    