from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_db
import json
import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from master import router as master_router
from auth import router as auth_router
from marketing import router as marketing_router
from operations import router as operations_router
from customer import router as customer_router
from form import router as form_router

# Include the master router


app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update to production frontend URL when needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the authentication router
app.include_router(auth_router)
app.include_router(master_router)
app.include_router(marketing_router, prefix="/api")
app.include_router(operations_router, prefix="/api")
app.include_router(customer_router, prefix="/api")
app.include_router(form_router, prefix="/api")

SECRET_KEY = "mysecretkey"  # Replace with a secure key
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic model for form data validation
class FormData(BaseModel):
    question1: str
    question2: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Dreamseller.io API"}

# @app.post("/api/submit-form")
# def submit_form(data: FormData, db=Depends(get_db)):
#     """Submit form data and save it in the database."""
#     response_data = {"question1": data.question1, "question2": data.question2}

#     with db.cursor() as cur:
#         cur.execute(
#             """
#             INSERT INTO form_responses (response_data, timestamp)
#             VALUES (%s, %s)
#             RETURNING id;
#             """,
#             (json.dumps(response_data), datetime.utcnow())
#         )
#         form_response_id = cur.fetchone()[0]
#         db.commit()

#     return {"message": "Form submitted successfully", "form_response_id": form_response_id}

@app.post("/api/contact-us")
def submit_contact_form(name: str = Form(...), email: str = Form(...), message: str = Form(...), db=Depends(get_db)):
    """Submit contact form data and save it in the database."""
    with db.cursor() as cur:
        cur.execute("""
            INSERT INTO contact_submissions (name, email, message, timestamp)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (name, email, message, datetime.utcnow()))
        contact_id = cur.fetchone()[0]
        db.commit()
    return {"message": "Contact form submitted successfully", "contact_id": contact_id}

# @app.get("/api/previous-form")
# def get_previous_form(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     """Retrieve the most recent form response for a regular user."""

#     # Decode the JWT token to get the user ID
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")  # Assuming "sub" holds the user ID
#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except jwt.JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     # Fetch the most recent form data for the user
#     with db.cursor() as cur:
#         cur.execute("""
#             SELECT response_data
#             FROM form_responses
#             WHERE shop_id = %s
#             ORDER BY timestamp DESC
#             LIMIT 1;
#         """, (user_id,))
#         result = cur.fetchone()

#     if result:
#         return result[0]
#     else:
#         raise HTTPException(status_code=404, detail="Previous form data not found.")


@app.get("/api/dashboard-data")
def get_dashboard_data(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    # Decode the JWT token
    try:
        print("HELLO")
        print("Received token:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        shop_id = payload.get("sub")
        shop_name = payload.get("shop_name")
        
        if not shop_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    # Retrieve data for the shop from the database
    with db.cursor() as cur:
        cur.execute("""
            SELECT response_data, timestamp
            FROM form_responses
            WHERE shop_id = %s
            ORDER BY timestamp DESC;
        """, (shop_id,))
        responses = cur.fetchall()

    # Structure the response
    return {
        "shop_name": shop_name,
        "responses": [{"data": response[0], "timestamp": response[1]} for response in responses],
        "message": "Protected data loaded successfully"
    }
