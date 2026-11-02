from fastapi import FastAPI

app = FastAPI(title="Student Management API")

@app.get("/")
def home():
    return {"message": "Welcome to my first API"}

@app.get("/about")
def about():
    return {
        "framework": "FastAPI",
        "language": "Python"
    }

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {
        "student_id": student_id,
        "name": "Ali"
    }

@app.post("/students")
def create_student():
    return {"message": "Student created"}

@app.put("/students/{student_id}")
def update_student(student_id: int):
    return {"message": "Student updated"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    return {"message": "Student deleted"}
