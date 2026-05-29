from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


# ==========================================================
# HEALTH SCHEMAS
# ==========================================================

class ServiceStatus(BaseModel):
    healthy: bool
    message: str


class HealthResponse(BaseModel):
    timestamp: datetime
    overall_health: bool
    overall_status: str
    services: Dict[str, ServiceStatus]


# ==========================================================
# METRICS SCHEMAS
# ==========================================================

class MetricData(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_usage: float


class MetricsResponse(BaseModel):
    timestamp: datetime
    metrics: MetricData


# ==========================================================
# LOG SCHEMAS
# ==========================================================

class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    source: str
    message: str


class LogsResponse(BaseModel):
    logs: List[LogEntry]


# ==========================================================
# AI INSIGHTS SCHEMAS
# ==========================================================

class AIRecommendation(BaseModel):
    severity: str
    recommendation: str


class AIResponse(BaseModel):
    timestamp: datetime
    analysis: str
    recommendations: List[AIRecommendation]


# ==========================================================
# CONFIGURATION SCHEMAS
# ==========================================================

class AWSConfigStatus(BaseModel):
    configured: bool
    region: Optional[str] = None


class OpenAIConfigStatus(BaseModel):
    configured: bool


class DatabaseConfigStatus(BaseModel):
    configured: bool


class RedisConfigStatus(BaseModel):
    configured: bool


class SMTPConfigStatus(BaseModel):
    configured: bool


class ConfigurationResponse(BaseModel):
    aws: AWSConfigStatus
    openai: OpenAIConfigStatus
    database: DatabaseConfigStatus
    redis: RedisConfigStatus
    smtp: SMTPConfigStatus


# ==========================================================
# CONFIGURATION REQUEST SCHEMAS
# ==========================================================

class AWSConfigRequest(BaseModel):
    access_key: str
    secret_key: str
    region: str


class OpenAIConfigRequest(BaseModel):
    api_key: str


class DatabaseConfigRequest(BaseModel):
    database_url: str


class RedisConfigRequest(BaseModel):
    redis_url: str


class SMTPConfigRequest(BaseModel):
    host: str
    port: int
    username: str
    password: str


# ==========================================================
# AUTHENTICATION SCHEMAS
# ==========================================================

class LoginRequest(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    role: str


class LoginResponse(BaseModel):
    success: bool
    access_token: str
    token_type: str
    user: UserInfo


# ==========================================================
# COMMON RESPONSE SCHEMAS
# ==========================================================

class SuccessResponse(BaseModel):
    success: bool
    message: str


class ErrorResponse(BaseModel):
    success: bool
    error: str