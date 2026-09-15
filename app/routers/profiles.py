from fastapi import APIRouter, Depends, HTTPException
from app.database import get_connection
from app.security import verify_token

router = APIRouter(prefix="/api/devices", tags=["Profiles / OBIS"])

@router.get("/{serial_number}/measurements")
def measurements(serial_number: str, _: str = Depends(verify_token)):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""SELECT m.serial_number,r.obis_code,r.value,r.unit,r.reading_time
                          FROM meters m JOIN meter_readings r ON m.id=r.meter_id
                          WHERE m.serial_number=%s ORDER BY r.reading_time DESC""", (serial_number,))
        rows = cursor.fetchall()
        if not rows: raise HTTPException(status_code=404, detail="No measurement data found")
        return {"device_serial": serial_number, "measurements": rows}
    finally:
        cursor.close(); connection.close()
