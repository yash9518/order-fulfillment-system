from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import jwt
from datetime import datetime, timedelta, timezone

from app.database import Base, engine, get_db
from app.models import User, Product, Order
from app.schemas import UserRegister, UserOut, Token, ProductCreate, ProductOut, OrderCreate, OrderOut
from app.security import hash_password, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order & Inventory Service")

SECRET_KEY = "dev_secret_key_change_in_production"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# --- AUTH ENDPOINTS ---
@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# --- PRODUCT ENDPOINTS ---
@app.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_product = Product(name=product.name, price=product.price, stock=product.stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# --- ORDER CREATION WITH ROW-LEVEL LOCKING ---
@app.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def place_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Row-level lock: with_for_update() ensures atomic inventory decrement
    product = db.query(Product).filter(Product.id == order_data.product_id).with_for_update().first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < order_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock available")
    
    # Deduct stock and commit atomically
    product.stock -= order_data.quantity
    
    total = product.price * order_data.quantity
    new_order = Order(
        user_id=current_user.id,
        product_id=product.id,
        quantity=order_data.quantity,
        total_price=total,
        status="CONFIRMED"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/orders", response_model=List[OrderOut])
def get_user_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()