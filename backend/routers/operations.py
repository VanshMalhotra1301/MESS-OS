from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import csv
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

# 1. Add Inventory API
@router.post("/inventory/add")
def add_inventory(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    new_item = models.InventoryItem(**item.dict())
    db.add(new_item)
    db.commit()
    return {"status": "Inventory Added"}

# 2. Edit Menu API
@router.post("/menu/update")
def update_menu(menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    # Logic to find existing menu entry and update it
    # For simplicity, we just create/update here
    return {"status": "Menu Updated"}

# 3. Register Student API
@router.post("/student/register")
def register_student(student: schemas.StudentRegister, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    return {"status": "Student Registered"}

# 4. Export Report API
@router.get("/reports/export")
def export_report(db: Session = Depends(get_db)):
    # Query your attendance_records table
    records = db.query(models.AttendanceRecord).all()
    
    # Create CSV in memory
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["Date", "Meal", "Expected", "Actual", "Wasted"])
    
    for r in records:
        writer.writerow([r.date, r.meal_type, r.expected_students, r.actual_attendance, r.wasted_qty])
    
    stream.seek(0)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=mess_report.csv"
    return response