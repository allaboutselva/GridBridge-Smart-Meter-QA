from fastapi import FastAPI

from app.routers import (
    auth,
    events,
    meters,
    network,
    operations,
    profiles,
    system,
)


app = FastAPI(
    title="GridBridge Meter QA API",
    description="Independent smart-meter API and QA automation learning project",
    version="2.0",
)


for router in (
    auth.router,
    system.router,
    meters.router,
    profiles.router,
    events.router,
    operations.router,
    network.router,
):
    app.include_router(router)