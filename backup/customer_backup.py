from fastapi import APIRouter, Depends
from auth import get_current_shop_id
from database import get_db

router = APIRouter()

@router.get("/customer_over")
def get_customer_over():
    # Dummy data for example purposes
    return {"score": "Marketing Score", "insights": "Some marketing insights"}



@router.get("/customers")
def get_customers(shop_id: int = Depends(get_current_shop_id), db=Depends(get_db)):
    # Retrieve only customers belonging to the authenticated shop_id
    with db.cursor() as cur:
        cur.execute("""
            SELECT loyalty_id, phone, date_joined, loyalty, birthday, email, is_active 
            FROM customers 
            WHERE shop_id = %s
        """, (shop_id,))
        
        customers = cur.fetchall()
        
    # Format and return customer data as a list of dictionaries
    return {"customers": [
        {"loyalty_id": customer[0], "phone": customer[1], "date_joined": customer[2],
         "loyalty": customer[3], "birthday": customer[4], "email": customer[5], 
         "is_active": customer[6]} 
        for customer in customers
    ]}
