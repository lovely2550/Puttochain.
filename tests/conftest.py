import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from puttochain.database import Base
from main import app, get_db

# ใช้ SQLite In-memory สำหรับการทดสอบที่รวดเร็ว
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    return create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

@pytest.fixture(scope="session")
def setup_db(engine):
    """สร้างตารางในฐานข้อมูลสำหรับทดสอบ"""
    Base.metadata.create_all(bind=engine)
    yield
    # ไม่ต้อง drop_all เพราะใช้ :memory: (จะถูกลบเมื่อปิด session)

@pytest.fixture(scope="function")
def db_session(engine, setup_db):
    """สร้าง Session ใหม่สำหรับแต่ละ Test (เพื่อให้ Test เป็นอิสระจากกัน)"""
    connection = engine.connect()
    transaction = connection.begin()
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionTesting()
    
    yield session
    
    session.close()
    transaction.rollback() # Rollback ทุกอย่างหลังจบ Test

@pytest.fixture(scope="function")
def client(db_session):
    """Override get_db dependency และสร้าง TestClient"""
    
    def override_get_db():
        """Dependency Injection ที่ใช้ Session ของ Test"""
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # Override get_current_user_wallet ให้ใช้ Mockup User สำหรับการทดสอบ Auth
    async def override_get_current_user_wallet():
        from puttochain.models import User # ต้อง Import ภายใน
        return db_session.query(User).first()
    app.dependency_overrides[get_current_user_wallet] = override_get_current_user_wallet
    
    with TestClient(app) as client:
        yield client
        
    app.dependency_overrides.clear() # ล้าง overrides หลังจบ Test
