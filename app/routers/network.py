import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.security import verify_token


router = APIRouter(
    prefix="/api/network",
    tags=["Network Configuration"],
)

DEVICE_ID_PATTERN = re.compile(r"^GB-DEVICE-\d{4}$")

SECURITY_KEYS: dict[str, str] = {}


class SecurityKey(BaseModel):
    device_id: str
    key: str = Field(min_length=32, max_length=32)


@router.post("/security-keys", status_code=201)
def add_security_key(
    item: SecurityKey,
    _: str = Depends(verify_token),
):
    if not DEVICE_ID_PATTERN.fullmatch(item.device_id):
        raise HTTPException(
            status_code=422,
            detail="Invalid device ID",
        )

    if not re.fullmatch(r"[0-9A-Fa-f]{32}", item.key):
        raise HTTPException(
            status_code=422,
            detail="Key must contain 32 hexadecimal characters",
        )

    SECURITY_KEYS[item.device_id] = item.key

    return {
        "device_id": item.device_id,
        "key": "*" * 24 + item.key[-8:],
    }


@router.get("/security-keys")
def list_security_keys(
    _: str = Depends(verify_token),
):
    return [
        {
            "device_id": device_id,
            "key": "*" * 24 + key[-8:],
        }
        for device_id, key in SECURITY_KEYS.items()
    ]