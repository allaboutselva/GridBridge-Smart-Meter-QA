from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response

from app.models import MeterCommandRequest, ClockTaskRequest
from app.security import verify_token


router = APIRouter(
    prefix="/api/operations",
    tags=["Operations"],
)

OPERATIONS: dict[str, dict] = {}


def _create_operation(operation_type: str, payload: dict):
    operation_id = str(uuid4())

    operation = {
        "id": operation_id,
        "type": operation_type,
        "status": "QUEUED",
        "created_on": datetime.now(timezone.utc),
        "request": payload,
    }

    OPERATIONS[operation_id] = operation

    return operation


@router.post("/meter-command", status_code=201)
def meter_command(
    request: MeterCommandRequest,
    _: str = Depends(verify_token),
):
    return _create_operation(
        "METER_COMMAND",
        request.model_dump(),
    )


@router.post("/set-meter-clock", status_code=201)
def set_meter_clock(
    request: ClockTaskRequest,
    _: str = Depends(verify_token),
):
    return _create_operation(
        "SET_METER_CLOCK",
        request.model_dump(),
    )


@router.get("")
def list_operations(
    _: str = Depends(verify_token),
):
    return {
        "count": len(OPERATIONS),
        "items": list(OPERATIONS.values()),
    }


@router.post("/{operation_id}/stop", status_code=204)
def stop_operation(
    operation_id: str,
    _: str = Depends(verify_token),
):
    if operation_id not in OPERATIONS:
        raise HTTPException(
            status_code=404,
            detail="Operation not found",
        )

    OPERATIONS[operation_id]["status"] = "STOPPED"

    return Response(status_code=204)