from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel

# Database connection
DATABASE_URL = "sqlite:///./students.db"

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


# Student database model
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


# Pydantic schemas
class StudentCreate(BaseModel):
    name: str
    age: int
    course: str


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    course: str | None = None


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Student Management API")


@app.get("/")
def home():
    return {"message": "Welcome to Student Management API"}


# CREATE student
@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# READ all students
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# READ student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# UPDATE student
@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


# DELETE student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
