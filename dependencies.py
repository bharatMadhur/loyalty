# backend/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# JWT and Password Hashing Configuration
SECRET_KEY = "mysecretkey"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # Token expires after 24 hours

# OAuth2 token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Master user credentials (hardcoded for simplicity)
MASTER_USER = {
    "username": "dreamseller",
    "password": "dreamseller"  # Ensure case sensitivity
}

# Helper functions

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the provided plaintext password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token."""
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


def get_current_shop_id(token: str = Depends(oauth2_scheme)) -> str:
    """Extracts the shop ID from the provided JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token to extract the shop_id
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        shop_id: str = payload.get("sub")  # Assuming 'sub' holds the shop ID
        if shop_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return shop_id


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Extract the current user details from the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        shop_name = payload.get("shop_name")
        if not user_id or not shop_name:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"user_id": user_id, "shop_name": shop_name}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


# Master user validation
def verify_master_user(username: str, password: str) -> bool:
    """Verify if the given credentials match the master user credentials."""
    return username == MASTER_USER["username"] and password == MASTER_USER["password"]
