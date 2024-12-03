# import psycopg
# from passlib.context import CryptContext

# DATABASE_URL = "dbname=dreamseller user=postgres password=Madhur1997"
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Define dummy user data
# dummy_users = [
#     {"shop_name": "shop_name1", "username": "test1", "password": "pass1"},
#     {"shop_name": "shop_name2", "username": "test2", "password": "pass2"}
# ]

# with psycopg.connect(DATABASE_URL) as conn:
#     with conn.cursor() as cur:
#         for user in dummy_users:
#             hashed_password = pwd_context.hash(user["password"])
#             cur.execute("""
#             INSERT INTO users (shop_name, username, hashed_password)
#             VALUES (%s, %s, %s)
#             ON CONFLICT (username) DO NOTHING;
#             """, (user["shop_name"], user["username"], hashed_password))
#         conn.commit()

#########################################################################


import psycopg
import pandas as pd
from datetime import datetime, timezone

# Replace these with your actual database credentials
DATABASE_URL = "dbname=dreamseller user=postgres password=Madhur1997"

# Load the CSV data into a DataFrame
df = pd.read_csv("dummy.csv")

# Connect to the PostgreSQL database
with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # Insert data from DataFrame into the `customers` table
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO customers (loyalty_id, phone, date_joined, loyalty, birthday, email, is_active, shop_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['loyalty_id'],
                row['phone'],
                datetime.strptime(row['date_joined'], '%Y-%m-%d').date(),
                row['loyalty'],
                datetime.strptime(row['birthday'], '%Y-%m-%d').date(),
                row['email'],
                row['is_active'],
                row['shop_id']
            ))
        conn.commit()

