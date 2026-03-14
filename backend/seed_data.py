import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import AttendanceRecord, Base
import os

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Get the admin user ID to link records
    from models import User
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        print("❌ Admin user not found! Run init_db.py first.")
        db.close()
        return
    
    admin_id = admin.id

    # Path to your CSV (adjusted for running from root)
    csv_path = os.path.join(os.getcwd(), "data", "mess_data_10000.csv")
    
    if not os.path.exists(csv_path):
        # Alternative path if running from backend folder
        csv_path = os.path.join(os.getcwd(), "..", "data", "mess_data_10000.csv")
        if not os.path.exists(csv_path):
            print(f"File not found: {csv_path}")
            db.close()
            return

    print("Reading CSV file...")
    df = pd.read_csv(csv_path)
    
    # Take the last 500 records to keep it efficient but substantial
    df = df.tail(500) 

    print(f"Inserting {len(df)} records into Supabase...")
    
    count = 0
    for index, row in df.iterrows():
        # Calculate waste data
        prepared = row['expected_students'] * 0.25
        actual = row['actual_attendance']
        waste = max(0, prepared - (actual * 0.25))

        record = AttendanceRecord(
            mess_id=admin_id,
            date=str(row['date']),
            day_of_week=row['day'],
            meal_type=row['meal_type'],
            expected_students=row['expected_students'],
            actual_attendance=actual,
            prepared_qty=prepared,
            wasted_qty=waste
        )
        db.add(record)
        count += 1
        
        if count % 100 == 0:
            print(f"   Processed {count} rows...")

    db.commit()
    db.close()
    print("Success! Data has been transferred to Supabase 'attendance_records' table.")

if __name__ == "__main__":
    seed_data()