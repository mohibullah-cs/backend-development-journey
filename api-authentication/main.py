from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pwdlib import PasswordHash

app = FastAPI(title="Authentication API")

# JWT settings
SECRET_KEY = "replace-with-a-long-random-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
password_hash = PasswordHash.recommended()

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Demo user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "hashed_password": password_hash.hash("admin123"),
    }
}


# Verify password
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


# Authenticate user
def authenticate_user(username, password):
    user = fake_users_db.get(username)

    if not user:
        return False

    if not verify_password(password, user["hashed_password"]):
        return False

    return user


# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Login endpoint
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Get current authenticated user
def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = fake_users_db.get(username)

    if user is None:
        raise credentials_exception

    return user


# Protected route
@app.get("/users/me")
def read_users_me(
    current_user: dict = Depends(get_current_user)
):
    return {
        "username": current_user["username"],
        "full_name": current_user["full_name"]
    }


# Home route
@app.get("/")
def home():
    return {
        "message": "Authentication API is running"
    }
