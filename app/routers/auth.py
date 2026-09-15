import secrets
from fastapi import APIRouter, HTTPException
from app.models import LoginRequest
from app.security import create_access_token
from config.settings import settings

router = APIRouter(tags=["Authentication"])

@router.post("/api/session")
def login(user: LoginRequest):
    valid_user = secrets.compare_digest(user.username, settings.api_username)
    valid_password = secrets.compare_digest(user.password, settings.api_password)
    if not (valid_user and valid_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}
