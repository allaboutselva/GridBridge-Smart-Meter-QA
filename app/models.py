from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class DeviceCreate(BaseModel):
    logical_name: str = Field(min_length=5)
    serial_number: str = Field(min_length=5)
    manufacturer: str = Field(min_length=2)
    status: Literal["ONLINE", "OFFLINE"]


class SearchFilters(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)
    order: str = ""
    where: dict = Field(default_factory=dict)
    fields: list[str] = Field(default_factory=list)


class SearchRequest(BaseModel):
    filters: SearchFilters = Field(default_factory=SearchFilters)


class MeterCommandRequest(BaseModel):
    meters: list[str]
    description: str = "Meter command"
    priority: int = Field(default=5, ge=1, le=10)
    timeout: int = Field(default=3600, ge=1)
    retries: int = Field(default=0, ge=0)
    run_at: datetime | None = None


class ClockTaskRequest(BaseModel):
    meters: list[str]
    description: str = "Clock synchronization"
    priority: int = 5
    timeout: int = 3600
    retries: int = 0
    synchronize_clock: bool = True
    daylight_savings_enabled: bool = True
    time_zone: str = "00:00"