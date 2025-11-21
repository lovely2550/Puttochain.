from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# ดึง URL การเชื่อมต่อจาก .env (เช่น postgresql://user:pass@host:port/db)
# ถ้าไม่พบ จะใช้ SQLite สำหรับ Development
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./puttochain.db")

# 1. สร้าง Engine
# สำหรับ SQLite ต้องตั้งค่า connect_args เพื่อให้ทำงานร่วมกับ FastAPI ได้
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} 
)

# 2. สร้าง SessionLocal (Class สำหรับสร้าง Session เชื่อมต่อ DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base Class สำหรับการประกาศ Model
Base = declarative_base()

# Dependency Injection: สำหรับให้ FastAPI Endpoint เรียกใช้ Session ได้
def get_db():
    """ฟังก์ชันที่จะถูกเรียกใช้เพื่อรับ DB Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
