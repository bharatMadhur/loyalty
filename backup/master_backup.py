# In your master.py file

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import get_db
from auth import pwd_context  # Import pwd_context for password hashing

router = APIRouter()

# User models for API requests
class NewUser(BaseModel):
    shop_name: str
    username: str
    password: str

class UpdateUser(BaseModel):
    user_id: int
    shop_name: str
    username: str
    password: str

def hash_password(password: str) -> str:
    """Helper function to hash the password."""
    return pwd_context.hash(password)

# Add user endpoint
@router.post("/api/master/add-user")
def add_user(user: NewUser, db=Depends(get_db)):
    hashed_password = hash_password(user.password)
    with db.cursor() as cur:
        cur.execute("INSERT INTO users (shop_name, username, hashed_password) VALUES (%s, %s, %s)",
                    (user.shop_name, user.username, hashed_password))
        db.commit()
    return {"message": "User added successfully"}

# Update user endpoint
@router.put("/api/master/update-user")
def update_user(user: UpdateUser, db=Depends(get_db)):
    # print("Received update payload:", user.dict())  # Debug log for incoming data
    hashed_password = hash_password(user.password)
    with db.cursor() as cur:
        cur.execute(
            "UPDATE users SET shop_name = %s, username = %s, hashed_password = %s WHERE id = %s",
            (user.shop_name, user.username, hashed_password, user.user_id)
        )
        db.commit()
    return {"message": "User updated successfully"}

@router.get("/api/master-dashboard")
def get_master_dashboard_data(db=Depends(get_db)):
    """Get data for the master dashboard, including contact submissions and user login counts."""
    with db.cursor() as cur:
        # Fetch contact submissions
        cur.execute("SELECT * FROM contact_submissions ORDER BY timestamp DESC;")
        contacts = cur.fetchall()
        
        # Fetch user logins and associated data
        cur.execute("SELECT id, shop_name, username, login_count FROM users;")
        user_logins = cur.fetchall()
        
    # Format and return data
    return {
        "contacts": [
            {"name": contact[1], "email": contact[2], "message": contact[3], "timestamp": contact[4]} 
            for contact in contacts
        ],
        "user_logins": [
            {"user_id": login[0], "shop_name": login[1], "username": login[2], "login_count": login[3]} 
            for login in user_logins
        ]
    }


