from database import engine, SessionLocal, Base
from models import User, AttendanceRecord, SurplusPost, MessProfile, NGOProfile
from werkzeug.security import generate_password_hash

# 1. Create all tables in the database
print("Creating tables in MySQL...")

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

# 2. Create a Database Session
db = SessionLocal()

# 3. Add Default Users (if they don't exist)
def create_dummy_users():
    # Check if Admin exists
    admin_email = "admin@example.com"
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    if not existing_admin:
        admin_user = User(
            email=admin_email,
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Create Mess Profile
        profile = MessProfile(
            user_id=admin_user.id,
            admin_name="Vansh Sharma",
            org_name="University Mess Hostel 4",
            org_type="Hostel Mess",
            capacity=500,
            contact_phone="9876543210",
            location="Campus Center"
        )
        db.add(profile)
        print(f"Created Admin User: email='{admin_email}', password='admin123'")

    # Check if NGO exists
    ngo_email = "ngo@example.com"
    existing_ngo = db.query(User).filter(User.email == ngo_email).first()
    if not existing_ngo:
        ngo_user = User(
            email=ngo_email,
            password=generate_password_hash("ngo123"),
            role="ngo"
        )
        db.add(ngo_user)
        db.commit()
        db.refresh(ngo_user)
        
        # Create NGO Profile
        profile = NGOProfile(
            user_id=ngo_user.id,
            ngo_name="Hope Foundation",
            contact_phone="1234567890",
            location="City Center (5km away)",
            service_radius=10.0,
            description="Helping students and community with surplus food."
        )
        db.add(profile)
        print(f"Created NGO User: email='{ngo_email}', password='ngo123'")
    
    db.commit()

try:
    create_dummy_users()
    print("Database setup complete! You are ready to go.")
except Exception as e:
    print(f"Error during setup: {e}")
finally:
    db.close()