
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(title="Student Management API")

# GET request - Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to my first API",
        "developer": "Python Backend Learner"
    }

# GET request - About route
@app.get("/about")
def about():
    return {
        "framework": "FastAPI",
        "language": "Python",
        "purpose": "Backend Development"
    }

# GET request - Path parameter
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {
        "student_id": student_id,
        "name": "Ali"
    }

# POST request
@app.post("/students")
def create_student():
    return {"message": "Student created successfully"}

# PUT request
@app.put("/students/{student_id}")
def update_student(student_id: int):
    return {
        "message": "Student updated",
        "student_id": student_id
    }

# DELETE request
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    return {
        "message": "Student deleted",
        "student_id": student_id
    }
