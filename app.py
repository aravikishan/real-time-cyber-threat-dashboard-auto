from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext
from datetime import datetime
import uvicorn

# Database setup
DATABASE_URL = "sqlite:///./cyber_threat_dashboard.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    url = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(Integer, ForeignKey('threats.id'))
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    threat = relationship("Threat")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data():
    db = SessionLocal()
    if not db.query(User).first():
        user = User(username="admin", password_hash=pwd_context.hash("admin"), role="admin")
        db.add(user)
        db.commit()
    if not db.query(Threat).first():
        threat = Threat(ip_address="192.168.1.1", url="http://malicious.com", severity="high")
        db.add(threat)
        db.commit()
    db.close()

seed_data()

# FastAPI app
app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard():
    with open("templates/dashboard.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/alerts", response_class=HTMLResponse)
async def read_alerts():
    with open("templates/alerts.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/reports", response_class=HTMLResponse)
async def read_reports():
    with open("templates/reports.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/settings", response_class=HTMLResponse)
async def read_settings():
    with open("templates/settings.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/login", response_class=HTMLResponse)
async def read_login():
    with open("templates/login.html") as f:
        return HTMLResponse(content=f.read())

# API Endpoints
@app.get("/api/threats")
async def get_threats():
    db = SessionLocal()
    threats = db.query(Threat).all()
    db.close()
    return threats

@app.post("/api/alerts")
async def create_alert(threat_id: int, description: str):
    db = SessionLocal()
    alert = Alert(threat_id=threat_id, description=description, status="new")
    db.add(alert)
    db.commit()
    db.close()
    return {"message": "Alert created"}

@app.get("/api/reports")
async def get_reports():
    # Mock implementation
    return {"report": "This is a mock report."}

@app.post("/api/auth/login")
async def login(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and pwd_context.verify(password, user.password_hash):
        return {"token": "mock-token"}
    raise HTTPException(status_code=400, detail="Invalid credentials")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
