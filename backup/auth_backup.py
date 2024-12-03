from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from database import get_db

# JWT and Password Hashing Configuration
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # Token expires after 24 hours

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Initialize the router
router = APIRouter()

# Master user credentials (hardcoded for simplicity)
MASTER_USER = {
    "username": "dreamseller",
    "password": "dreamseller"  # Ensure case sensitivity
}

# auth.py
def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def authenticate_user(db, shop_name: str, username: str, password: str):
    """Fetch and verify a regular user from the database."""
    with db.cursor() as cur:
        cur.execute(
            "SELECT id, shop_name, hashed_password, login_count FROM users WHERE shop_name = %s AND username = %s",
            (shop_name, username)
        )
        user = cur.fetchone()
    
    if user and verify_password(password, user[2]):
        return {"id": user[0], "shop_name": user[1], "login_count": user[3]}
    return None

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """Regular user login endpoint."""
    try:
        shop_name, username = form_data.username.split("|")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username format. Use shop_name|username."
        )

    # Authenticate as a regular user
    user = authenticate_user(db, shop_name, username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Increment login count for the regular user
    with db.cursor() as cur:
        cur.execute("UPDATE users SET login_count = login_count + 1 WHERE username = %s", (username,))
        db.commit()
    
    # Create access token for the regular user
    access_token = create_access_token(data={"sub": user["id"], "shop_name": shop_name})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/master-login")
def master_login(username: str = Form(...), password: str = Form(...)):
    """Master user login endpoint without JWT generation."""
    if username == MASTER_USER["username"] and password == MASTER_USER["password"]:
        return {"message": "Master login successful"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid master credentials")

@router.get("/api/check-master-user")
async def check_master_user(username: str = Form(...), password: str = Form(...)):
    """Endpoint to check if the current user is the master user."""
    is_master_user = (username == MASTER_USER["username"] and password == MASTER_USER["password"])
    return {"is_master_user": is_master_user}

@router.get("/api/validate-token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": "Token is valid"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_current_shop_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        shop_id = payload.get("sub")  # Retrieve shop_id from 'sub'
        if shop_id is None:
            raise HTTPException(status_code=403, detail="Shop ID not found")
        return shop_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

