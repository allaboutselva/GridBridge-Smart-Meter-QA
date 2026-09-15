import mysql.connector
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_connection
from app.models import DeviceCreate, SearchRequest
from app.security import verify_token

router = APIRouter(prefix="/api/devices", tags=["Meters"])

def _fetch_device(serial_number: str):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM meters WHERE serial_number = %s", (serial_number,))
        return cursor.fetchone()
    finally:
        cursor.close(); connection.close()

@router.post("", status_code=201)
def create_device(device: DeviceCreate, _: str = Depends(verify_token)):
    connection = get_connection(); cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO meters (logical_name, serial_number, manufacturer, status) VALUES (%s,%s,%s,%s)",
                       (device.logical_name, device.serial_number, device.manufacturer, device.status))
        connection.commit()
        return {"message": "Device created successfully", "device_id": cursor.lastrowid, "device": device.model_dump()}
    except mysql.connector.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Device serial number already exists") from exc
    finally:
        cursor.close(); connection.close()

@router.post("/search")
def search_devices(request: SearchRequest, _: str = Depends(verify_token)):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM meters ORDER BY id LIMIT %s OFFSET %s", (request.filters.limit, request.filters.offset))
        rows = cursor.fetchall()
        return {"offset": request.filters.offset, "limit": request.filters.limit, "count": len(rows), "items": rows}
    finally:
        cursor.close(); connection.close()

@router.get("/{serial_number}")
def get_device(serial_number: str, _: str = Depends(verify_token)):
    device = _fetch_device(serial_number)
    if not device: raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.get("/{serial_number}/state")
def get_device_state(serial_number: str, _: str = Depends(verify_token)):
    device = _fetch_device(serial_number)
    if not device: raise HTTPException(status_code=404, detail="Device not found")
    return {"serial_number": device["serial_number"], "state": device["status"]}
