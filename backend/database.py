import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- SUPABASE POSTGRES CONNECTION ---
SUPABASE_PASSWORD_RAW = os.getenv("SUPABASE_PASSWORD", "Vansh@ww22iixxzz")
SUPABASE_PASSWORD = urllib.parse.quote_plus(SUPABASE_PASSWORD_RAW)

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql://postgres.zipaybqpbzdtpuwlufbp:{SUPABASE_PASSWORD}@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
)

# Connect arguments (options) for PostgreSQL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()