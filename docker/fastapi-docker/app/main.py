from fastapi import FastAPI

app = FastAPI(
    title="Dockerized FastAPI Application",
    description="A backend API containerized using Docker.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to my Dockerized FastAPI Application!",
        "developer": "Mohib",
        "status": "Running successfully",
        "technology": "Python, FastAPI and Docker"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "backend-api"
    }


@app.get("/about")
def about():
    return {
        "project": "FastAPI Docker Project",
        "purpose": "Learning Docker containerization",
        "version": "1.0.0"
    }
