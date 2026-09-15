from fastapi import APIRouter, Depends
from app.security import verify_token

router = APIRouter(tags=["System"])

@router.get("/")
def home():
    return {"message": "GridBridge Meter QA API is running"}

@router.get("/api/system")
def system_info(username: str = Depends(verify_token)):
    return {"system": "GridBridge Meter QA API", "status": "running", "version": "2.0", "authenticated_user": username}
