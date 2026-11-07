from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, ConfigDict

# Database connection
DATABASE_URL = "sqlite:///./cookies_orm.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Database model
class Cookie(Base):
    __tablename__ = "cookies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

# Pydantic schema
class CookieCreate(BaseModel):
    name: str
    price: float
    quantity: int

class CookieResponse(CookieCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI application
app = FastAPI(title="Cookie CRUD API")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/cookies/", response_model=CookieResponse)
def create_cookie(
    cookie: CookieCreate,
    db: Session = Depends(get_db)
):
    new_cookie = Cookie(**cookie.model_dump())

    db.add(new_cookie)
    db.commit()
    db.refresh(new_cookie)

    return new_cookie

# READ ALL
@app.get("/cookies/")
def get_cookies(db: Session = Depends(get_db)):
    return db.query(Cookie).all()

# READ ONE
@app.get("/cookies/{cookie_id}")
def get_cookie(
    cookie_id: int,
    db: Session = Depends(get_db)
):
    cookie = db.query(Cookie).filter(
        Cookie.id == cookie_id
    ).first()

    if not cookie:
        raise HTTPException(404, "Cookie not found")

    return cookie

# UPDATE
@app.put("/cookies/{cookie_id}")
def update_cookie(
    cookie_id: int,
    updated_data: CookieCreate,
    db: Session = Depends(get_db)
):
    cookie = db.query(Cookie).filter(
        Cookie.id == cookie_id
    ).first()

    if not cookie:
        raise HTTPException(404, "Cookie not found")

    for key, value in updated_data.model_dump().items():
        setattr(cookie, key, value)

    db.commit()
    db.refresh(cookie)

    return cookie

# DELETE
@app.delete("/cookies/{cookie_id}")
def delete_cookie(
    cookie_id: int,
    db: Session = Depends(get_db)
):
    cookie = db.query(Cookie).filter(
        Cookie.id == cookie_id
    ).first()

    if not cookie:
        raise HTTPException(404, "Cookie not found")

    db.delete(cookie)
    db.commit()

    return {"message": "Cookie deleted successfully"}
