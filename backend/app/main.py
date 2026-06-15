from fastapi import FastAPI 
from app.routes.health import (
    router as health_router )

from app.routes.logs import (
    router as logs_router
)

from app.routes.metrics import (
    router as metrics_router
)

app = FastAPI()
app.include_router(health_router)
app.include_router(logs_router)
app.include_router(metrics_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CloudPilot AI!"} 