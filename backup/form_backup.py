from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from database import get_db
import jwt
import json

router = APIRouter()
SECRET_KEY = "mysecretkey"  # Replace with a secure key
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class FormData(BaseModel):
    questions: dict  # Dictionary for all preset questions and answers
    additional_questions: list = []  # List for additional custom questions

@router.get("/previous-form")
async def get_previous_form(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """Retrieve the most recent form response for a regular user."""

    # Decode the JWT token to get the user ID
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # Assuming "sub" holds the user ID
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch the most recent form data for the user
    with db.cursor() as cur:
        cur.execute("""
            SELECT response_data
            FROM form_responses
            WHERE shop_id = %s
            ORDER BY timestamp DESC
            LIMIT 1;
        """, (user_id,))
        result = cur.fetchone()

    if result:
        # Check if result[0] is already a dictionary
        response_data = result[0] if isinstance(result[0], dict) else json.loads(result[0])
        return response_data
    else:
        raise HTTPException(status_code=404, detail="Previous form data not found.")

@router.post("/submit-form")
async def submit_form(data: FormData, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """Submit form data and save it in the database."""
    
    # Decode the JWT token to get the user ID
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Prepare the data to store in the database
    response_data = {
        "questions": data.questions,
        "additional_questions": data.additional_questions,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Insert the form data into the database
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO form_responses (shop_id, response_data, timestamp)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (user_id, json.dumps(response_data), datetime.utcnow())
        )
        form_response_id = cur.fetchone()[0]
        db.commit()

    return {"message": "Form submitted successfully", "form_response_id": form_response_id}
