import psycopg
from datetime import datetime, timezone

# Replace these with your actual database credentials
DATABASE_URL = "dbname=dreamseller user=postgres password=Madhur1997"

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # Create users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
        loyalty_id VARCHAR(10) PRIMARY KEY,
        phone VARCHAR(15),
        date_joined DATE,
        loyalty BOOLEAN DEFAULT FALSE,
        birthday DATE,
        email VARCHAR(50),
        is_active BOOLEAN DEFAULT TRUE,
        shop_id INTEGER REFERENCES users(id) ON DELETE CASCADE  -- Associate with a specific shop
        );
        """)
        conn.commit()


