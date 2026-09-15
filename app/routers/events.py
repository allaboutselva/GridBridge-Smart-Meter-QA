from fastapi import APIRouter, Depends, HTTPException
from app.database import get_connection
from app.models import SearchRequest
from app.security import verify_token

router = APIRouter(tags=["Events / Alarms"])

@router.get("/api/devices/{serial_number}/events")
def device_events(serial_number: str, _: str = Depends(verify_token)):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""SELECT m.serial_number,e.event_type,e.event_time
                          FROM meters m JOIN meter_events e ON m.id=e.meter_id
                          WHERE m.serial_number=%s ORDER BY e.event_time DESC""", (serial_number,))
        rows = cursor.fetchall()
        if not rows: raise HTTPException(status_code=404, detail="No device events found")
        return {"device_serial": serial_number, "events": rows}
    finally:
        cursor.close(); connection.close()

@router.post("/api/events/search")
def search_events(request: SearchRequest, _: str = Depends(verify_token)):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""SELECT m.serial_number,e.event_type,e.event_time FROM meter_events e
                          JOIN meters m ON m.id=e.meter_id ORDER BY e.event_time DESC LIMIT %s OFFSET %s""",
                       (request.filters.limit, request.filters.offset))
        rows=cursor.fetchall(); return {"count":len(rows),"items":rows}
    finally:
        cursor.close(); connection.close()
