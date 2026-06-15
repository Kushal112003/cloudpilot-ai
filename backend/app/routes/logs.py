from fastapi import APIRouter
from app.services.loki_service import (
    LokiLogService
)

router = APIRouter()

@router.get(
    "/logs",
    tags=["Logs"],
    summary="Fetch Logs From Loki"
)

def get_logs(

    namespace: str = "cloudpilot",
    limit: int = 50,
    search: str | None = None
):
    
    return LokiLogService().get_logs(
        namespace=namespace,
        limit=limit,
        search=search
    )