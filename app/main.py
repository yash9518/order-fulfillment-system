from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone

app = FastAPI(title="Order & Inventory Service")

SECRET_KEY = "dev_secret_key_change_in_production"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return {"user_id": user_id, "role": payload.get("role", "customer")}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

# Public route: Login (Generates JWT)
@app.post("/login")
def login():
    # Mocking successful credentials validation for now
    token = create_access_token(data={"sub": "user_101", "role": "customer"})
    return {"access_token": token, "token_type": "bearer"}

# Protected route: Requires valid JWT in Authorization header
@app.get("/orders")
def get_orders(user: dict = Depends(get_current_user)):
    return {"message": f"Fetching orders for {user['user_id']}", "role": user["role"]}