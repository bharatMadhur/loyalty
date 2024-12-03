from fastapi import HTTPException, status

MASTER_USER = {
    "username": "admin",
    "password": "password123"
}

def master_login_required(username: str, password: str):
    if username != MASTER_USER["username"] or password != MASTER_USER["password"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
